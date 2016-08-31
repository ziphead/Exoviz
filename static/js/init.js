

  function initialize() {
   /*Count Down Settings*/
   datetime='01/01/2016 12:00:00';
   /* Google MAP Settings*/
   lat= 55.7466874;  //Change the value with your address Latitude
   lng= 37.6273493;  //Change the value with your address Longitude
  }

  /*  Animation section home  */
  function startPage() {
    setTimeout ( function () {
		$(".logo").removeClass("Out").addClass("In fadeInDown");
		},200 );
    setTimeout ( function () {
		$(".diamond1").removeClass("Out").addClass("In fadeInUp");
		},1000 );
    setTimeout ( function () {
		$(".diamond2").removeClass("Out").addClass("In fadeInUp");
		},1000 );
    setTimeout ( function () {
		$(".diamond3").removeClass("Out").addClass("In fadeInUp");
		},1400 );
    setTimeout ( function () {
		$(".diamond4").removeClass("Out").addClass("In fadeInUp");
		},1400 );
    setTimeout ( function () {
		$(".diamond5").removeClass("Out").addClass("In fadeInUp");
		},1400 );
    setTimeout ( function () {
		$(".diamond6").removeClass("Out").addClass("In fadeInUp");
		},1800 );
    setTimeout ( function () {
		$(".diamond7").removeClass("Out").addClass("In fadeInUp");
		},1800 );
    setTimeout ( function () {
			$(".title_header").removeClass("Out").addClass("In fadeInUp");
		},2400 );
	} /*  End animation section home  */


  /*Onload function*/
  $(window).load(function(){
    initialize();
    $("#preload").css({ display: 'none'});
    $("body").removeClass("preload");
    startPage();
    $("html").niceScroll({
        cursorcolor: "#333",
        cursoropacitymin: 0.6,
        background: "#666",
        cursorborder: "0",
        autohidemode: true,
        cursorminheight: 30,
        zindex:9999999,
        horizrailenabled:false
    });
    $("#about-panel").niceScroll({
        cursorcolor: "#333",
        cursoropacitymin: 0.6,
        background: "#666",
        cursorborder: "0",
        autohidemode: true,
        touchbehavior:true,
        zindex:9999999,
        cursorminheight: 30
    });
    $("#contact-panel").niceScroll({
        cursorcolor: "#333",
        cursoropacitymin: 0.6,
        background: "#666",
        cursorborder: "0",
        autohidemode: true,
        touchbehavior:true,
        zindex:9999999,
        cursorminheight: 30
    });

    $("#about-panel").getNiceScroll().hide();
    $("#contact-panel").getNiceScroll().hide();

/**
* INITIALIZE COUNTDOWN SCRIPT
**/
     $('#countdown').downCount({
            date: datetime,
            offset: +10
        }, function () {
            alert('done!');
        });

  });


/*
Page panel
*/
    $('.about').click(function(e) {
     $("body").getNiceScroll().hide();
     $(".b-r").removeClass("In").addClass("Out");
     $.panelslider($('#about-panel'),{side: 'left', clickClose: false, duration: 400 });
     setTimeout ( function () {
		   $(".b-l").removeClass("In").addClass("Out");
		 },100 );
     setTimeout ( function () {
		   $(".full-width").removeClass("In").addClass("Out");
 		 },200 );
     setTimeout ( function () {
     $("#about-panel").getNiceScroll().show();
      },800 );
    });

   $('.contact').click(function(e) {
     e.preventDefault();
     $("body").getNiceScroll().hide();
     $(".b-l").removeClass("In").addClass("Out");
     $.panelslider($('#contact-panel'),{side: 'right', clickClose: false, duration: 400 } );

     var myMap = initializeMap();
     setTimeout(function() {
     google.maps.event.trigger(myMap, 'resize');
     $(".b-r").removeClass("In").addClass("Out");
     }, 100);
     setTimeout ( function () {
		   $(".full-width").removeClass("In").addClass("Out");
		 },200 );
     setTimeout ( function () {
     $("#contact-panel").getNiceScroll().show();
      },800 );
    });


    $('.close-panel').click(function() {
      $("#about-panel").getNiceScroll().hide();
      $("#contact-panel").getNiceScroll().hide();

      $.panelslider.close();
      setTimeout ( function () {
		   $(".full-width").removeClass("Out").addClass("In");
       $(".b-l").removeClass("Out").addClass("In");
       $(".b-r").removeClass("Out").addClass("In");
       $("body").getNiceScroll().show();
		 },100 );
    });

 /**
 * Subscribe Form
 */
	$('#subscribe-form').submit(function() {
		// update user interface
		$('#response').html('<div class="loading"><span class="bounce1"></span><span class="bounce2"></span><span class="bounce3"></span><span class="bounce4"></span></div>');

		// Prepare query string and send AJAX request
		$.ajax({
			url: 'js/inc/store-address.php',
			data: 'ajax=true&email=' + escape($('#subscribe_email').val()),
			success: function(msg) {
				$('#response').html(msg);
			}
		});

		return false;
	});

  function initializeMap() {
    initialize();
     var mapOptions = {
       center: new google.maps.LatLng(lat, lng),
       zoom: 16,
       mapTypeId: google.maps.MapTypeId.ROADMAP
     };
     var map = new google.maps.Map(document.getElementById("map"), mapOptions);
     var marker = new google.maps.Marker({
position: mapOptions['center'],
map: map,
});
     return map;
    }
/*Contact Form*/

$(document).ready(function() {
	var form = $('#contactForm'); // contact form
	var submit = $('#contactForm_submit');	// submit button
	var alert = $('.successMsg'); // alert div for show alert message
	// form submit event
	form.on('submit', function(e) {
		e.preventDefault(); // prevent default form submit
		// sending ajax request through jQuery
		$.ajax({
			url: 'js/inc/sendemail.php', // form action url
			type: 'POST', // form submit method get/post
			dataType: 'html', // request type html/json/xml
			data: form.serialize(), // serialize form data
			beforeSend: function() {
				alert.fadeOut();
				submit.html('Sending....'); // change submit button text
			},
			success: function(data) {
				form.fadeOut(300);
                alert.html(data).fadeIn(1000); // fade in response data
			},
			error: function(e) {
				console.log(e)
			}
		});
	});
});
