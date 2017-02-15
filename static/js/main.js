var showFlashMessage = function(message, status){
      console.log("From Flash Message")
      var flash = "<div id='jquery-flash' class='messages'><div class='col-sm-3 pull-right'><div class='alert alert-"+status+"'>"+
        "<button type='button' class='close' data-dismiss='alert' aria-label='Close'><span aria-hidden='true'>&times;</span></button>"+
        message +
        "</div></div></div>";

      $('body').append(flash);
      $('#jquery-flash').fadeIn();

      setTimeout(function () {
        $('#jquery-flash').fadeOut()
      }, 3000)
    }


$("#django-flash").fadeIn();
setTimeout(function(){
  $("#django-flash").fadeOut();
}, 3000)
