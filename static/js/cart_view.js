$(function(){

    $(".item-qty").change(function(){

      /// Make ajax call

      var lineId = $(this).attr('line-id')
      var formData = $('#update-qty-form-'+lineId).serialize();
      console.log(formData)
      $.ajax({
        type: 'GET',
        url: ajaxUrl,
        data: formData,
        success: function(res){

          $("#line-total-"+lineId).text(res.line_total);
          $("#cart-subtotal").text(res.cart_subtotal);
          var flashMsg="";
          if (res.created){
            flashMsg = "Successfully add to cart";
          } else if (res.deleted){
            flashMsg = "Successfully removed from cart"
          } else {
            flashMsg = "Successfully update quantity"
          }
          showFlashMessage(flashMsg, "success");
        },
        error: function(res, err){
          console.log(res, err)
        }
      });
    });
})
