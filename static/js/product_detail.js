$(function(){

  function setPrice (){

    var price = $("#variation-select option:selected").attr("data-price");
    var salePrice = $("#variation-select option:selected").attr("data-sale-price");
    if (price){
      if (salePrice != '' && salePrice!='None' && salePrice!='0.00'){
        $("#price").text(salePrice+" EGP");
        $("#original-price").text(price+" EGP");
      } else{
        $("#price").text(price+" EGP");
        $("#original-price").text("");
      }
    } else {
      
    }

  }
  setPrice();

  // handle selection change
  $("#variation-select").change(function(){
    setPrice();
  });



  $('#submit-btn').click(function (e) {
    e.preventDefault();
    var formData = $('#add-form').serialize();

    $.ajax({
      type: 'GET',
      url: ajaxUrl,
      data: formData,
      success: function(res){
        var flashMsg="";
        if (res.created){
            flashMsg = "Succesfully add to cart";
          } else if (res.deleted){
            flashMsg = "Succesfully removed from cart"
          } else {
            flashMsg = "Succesfully update quantity"
          }
          showFlashMessage(flashMsg, "success");
          updateCartCount();
      },
      error: function(res, err){
        console.log(res, err)
      }

    })
  })
})
