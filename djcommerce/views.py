from django.shortcuts import render, redirect, reverse
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from products.models import Product


def index(request):
    featured_product = Product.objects.filter(is_featured=True).order_by("?").first()
    context = {
        'featured': featured_product
    }
    return render(request, 'index.html', context)


def login_view(request):
    # login_form = LoginForm(request.POST or None)
    login_form = AuthenticationForm(data=request.POST or None)
    next_url = request.GET.get('next')

    if next_url is None:
        next_url = reverse('home_page')

    print('******* ', request.POST)

    if login_form.is_valid():
        username = login_form.cleaned_data.get('username')
        password = login_form.cleaned_data.get('password')
        next_url = request.POST.get('next')
        user = authenticate(username=username, password=password)
        if not user:
            messages.error(request, 'Please enter a correct username and password.')
        else:
            login(request, user)
            messages.success(request, 'You are successfully logged in.')
            return redirect(next_url)

    return render(request, 'login.html', {'form':login_form, 'next': next_url})


def logout_view(request):
    logout(request)
    return redirect(reverse('home_page'))


def register_view(request):
    # register_form = RegisterForm(request.POST or None)
    register_form = UserCreationForm(data=request.POST or None)
    if register_form.is_valid():
        new_user = register_form.save(commit=False)
        new_user.first_name = request.POST.get('first_name')
        new_user.last_name = request.POST.get('last_name')
        new_user.set_password(register_form.cleaned_data.get('password1'))
        new_user.save()
        print(new_user)
        login(request, new_user)
        messages.success(request, 'User Saved')
        return redirect(reverse('home_page'))

    return render(request, 'register.html', {'form': register_form})
