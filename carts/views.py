from django.http import Http404, JsonResponse
from django.views.generic import View
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic.detail import SingleObjectMixin, DetailView
from carts.models import Cart, CartItem
from products.models import Variation
from django.shortcuts import render, redirect, reverse, get_object_or_404


class ItemCountView(View):

    def get(self, request, *args, **kwargs):

        if request.is_ajax():
            cart_id = request.session.get("cart_id")
            if cart_id == None:
                count = 0
            else:
                cart = Cart.objects.get(id=cart_id)
                count = cart.items.count()

            request.session['cart_item_count'] = count
            return JsonResponse({
                "count": count
            })
        else:
            raise Http404


class CartView(SingleObjectMixin, View):
    model = Cart
    template_name = 'carts/view.html'

    def get_object(self, *args, **kwargs):
        self.request.session.set_expiry(0)  # close the session when browser close
        cart_id = self.request.session.get('cart_id')
        if cart_id is None:
            cart = Cart()
            cart.save()
            cart_id = cart.id
            self.request.session['cart_id'] = cart_id

        cart = Cart.objects.get(id=cart_id)
        if self.request.user.is_authenticated():
            cart.user = self.request.user
            cart.save()

        return cart

    def get(self, request, *args, **kwargs):
        cart = self.get_object()
        qty = request.GET.get('qty', 1)
        item_id = request.GET.get('item')
        is_delete = request.GET.get('del')

        if item_id:
            item_instance = get_object_or_404(Variation, id=item_id)

            try:
                if int(qty) < 1:
                    is_delete = True
            except:
                raise Http404

            cart_item, is_created = CartItem.objects.get_or_create(cart=cart, item=item_instance)
            if is_delete:
                print("Deleting item")
                cart_item.delete()
            else:
                cart_item.quantity = qty
                # cart_item.line_total = qty*cart_item.item.get_price()
                cart_item.save()
        if request.is_ajax():
            cart.update_subtotal()
            return JsonResponse({
                'created': is_created,
                'deleted': is_delete,
                'line_total': cart_item.line_total,
                'cart_subtotal': cart.subtotal,
                'cart_total_tax': cart.total_tax,
                'cart_total_price': cart.total_price
            })

        context = {
            "cart": self.get_object()
        }
        return render(request, self.template_name, context)


class CheckoutView(DetailView):
    model = Cart
    template_name = 'carts/checkout_view.html'

    def get_object(self, *args, **kwargs):
        cart_id = self.request.session.get('cart_id')
        if not cart_id:
            return redirect(reverse('cart'))

        cart = Cart.objects.get(id=cart_id)
        return cart

    def get_context_data(self, **kwargs):
        context = super(CheckoutView, self).get_context_data(**kwargs)
        context['login_form'] = AuthenticationForm()
        context['next_url'] = self.request.build_absolute_uri
        return context
