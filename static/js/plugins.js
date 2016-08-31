/*! Backstretch - v2.0.4 - 2013-06-19
* http://srobbin.com/jquery-plugins/backstretch/
* Copyright (c) 2013 Scott Robbin; Licensed MIT */
(function(a,d,p){a.fn.backstretch=function(c,b){(c===p||0===c.length)&&a.error("No images were supplied for Backstretch");0===a(d).scrollTop()&&d.scrollTo(0,0);return this.each(function(){var d=a(this),g=d.data("backstretch");if(g){if("string"==typeof c&&"function"==typeof g[c]){g[c](b);return}b=a.extend(g.options,b);g.destroy(!0)}g=new q(this,c,b);d.data("backstretch",g)})};a.backstretch=function(c,b){return a("body").backstretch(c,b).data("backstretch")};a.expr[":"].backstretch=function(c){return a(c).data("backstretch")!==p};a.fn.backstretch.defaults={centeredX:!0,centeredY:!0,duration:5E3,fade:0};var r={left:0,top:0,overflow:"hidden",margin:0,padding:0,height:"100%",width:"100%",zIndex:-999999},s={position:"absolute",display:"none",margin:0,padding:0,border:"none",width:"auto",height:"auto",maxHeight:"none",maxWidth:"none",zIndex:-999999},q=function(c,b,e){this.options=a.extend({},a.fn.backstretch.defaults,e||{});this.images=a.isArray(b)?b:[b];a.each(this.images,function(){a("<img />")[0].src=this});this.isBody=c===document.body;this.$container=a(c);this.$root=this.isBody?l?a(d):a(document):this.$container;c=this.$container.children(".backstretch").first();this.$wrap=c.length?c:a('<div class="backstretch"></div>').css(r).appendTo(this.$container);this.isBody||(c=this.$container.css("position"),b=this.$container.css("zIndex"),this.$container.css({position:"static"===c?"relative":c,zIndex:"auto"===b?0:b,background:"none"}),this.$wrap.css({zIndex:-999998}));this.$wrap.css({position:this.isBody&&l?"fixed":"absolute"});this.index=0;this.show(this.index);a(d).on("resize.backstretch",a.proxy(this.resize,this)).on("orientationchange.backstretch",a.proxy(function(){this.isBody&&0===d.pageYOffset&&(d.scrollTo(0,1),this.resize())},this))};q.prototype={resize:function(){try{var a={left:0,top:0},b=this.isBody?this.$root.width():this.$root.innerWidth(),e=b,g=this.isBody?d.innerHeight?d.innerHeight:this.$root.height():this.$root.innerHeight(),j=e/this.$img.data("ratio"),f;j>=g?(f=(j-g)/2,this.options.centeredY&&(a.top="-"+f+"px")):(j=g,e=j*this.$img.data("ratio"),f=(e-b)/2,this.options.centeredX&&(a.left="-"+f+"px"));this.$wrap.css({width:b,height:g}).find("img:not(.deleteable)").css({width:e,height:j}).css(a)}catch(h){}return this},show:function(c){if(!(Math.abs(c)>this.images.length-1)){var b=this,e=b.$wrap.find("img").addClass("deleteable"),d={relatedTarget:b.$container[0]};b.$container.trigger(a.Event("backstretch.before",d),[b,c]);this.index=c;clearInterval(b.interval);b.$img=a("<img />").css(s).bind("load",function(f){var h=this.width||a(f.target).width();f=this.height||a(f.target).height();a(this).data("ratio",h/f);a(this).fadeIn(b.options.speed||b.options.fade,function(){e.remove();b.paused||b.cycle();a(["after","show"]).each(function(){b.$container.trigger(a.Event("backstretch."+this,d),[b,c])})});b.resize()}).appendTo(b.$wrap);b.$img.attr("src",b.images[c]);return b}},next:function(){return this.show(this.index<this.images.length-1?this.index+1:0)},prev:function(){return this.show(0===this.index?this.images.length-1:this.index-1)},pause:function(){this.paused=!0;return this},resume:function(){this.paused=!1;this.next();return this},cycle:function(){1<this.images.length&&(clearInterval(this.interval),this.interval=setInterval(a.proxy(function(){this.paused||this.next()},this),this.options.duration));return this},destroy:function(c){a(d).off("resize.backstretch orientationchange.backstretch");clearInterval(this.interval);c||this.$wrap.remove();this.$container.removeData("backstretch")}};var l,f=navigator.userAgent,m=navigator.platform,e=f.match(/AppleWebKit\/([0-9]+)/),e=!!e&&e[1],h=f.match(/Fennec\/([0-9]+)/),h=!!h&&h[1],n=f.match(/Opera Mobi\/([0-9]+)/),t=!!n&&n[1],k=f.match(/MSIE ([0-9]+)/),k=!!k&&k[1];l=!((-1<m.indexOf("iPhone")||-1<m.indexOf("iPad")||-1<m.indexOf("iPod"))&&e&&534>e||d.operamini&&"[object OperaMini]"==={}.toString.call(d.operamini)||n&&7458>t||-1<f.indexOf("Android")&&e&&533>e||h&&6>h||"palmGetResource"in d&&e&&534>e||-1<f.indexOf("MeeGo")&&-1<f.indexOf("NokiaBrowser/8.5.0")||k&&6>=k)})(jQuery,window);

/*! device.js 0.1.58 */
(function(){var a,b,c,d,e,f,g,h,i,j;a=window.device,window.device={},c=window.document.documentElement,j=window.navigator.userAgent.toLowerCase(),device.ios=function(){return device.iphone()||device.ipod()||device.ipad()},device.iphone=function(){return d("iphone")},device.ipod=function(){return d("ipod")},device.ipad=function(){return d("ipad")},device.android=function(){return d("android")},device.androidPhone=function(){return device.android()&&d("mobile")},device.androidTablet=function(){return device.android()&&!d("mobile")},device.blackberry=function(){return d("blackberry")||d("bb10")||d("rim")},device.blackberryPhone=function(){return device.blackberry()&&!d("tablet")},device.blackberryTablet=function(){return device.blackberry()&&d("tablet")},device.windows=function(){return d("windows")},device.windowsPhone=function(){return device.windows()&&d("phone")},device.windowsTablet=function(){return device.windows()&&d("touch")},device.fxos=function(){return d("(mobile; rv:")||d("(tablet; rv:")},device.fxosPhone=function(){return device.fxos()&&d("mobile")},device.fxosTablet=function(){return device.fxos()&&d("tablet")},device.mobile=function(){return device.androidPhone()||device.iphone()||device.ipod()||device.windowsPhone()||device.blackberryPhone()||device.fxosPhone()},device.tablet=function(){return device.ipad()||device.androidTablet()||device.blackberryTablet()||device.windowsTablet()||device.fxosTablet()},device.portrait=function(){return 90!==Math.abs(window.orientation)},device.landscape=function(){return 90===Math.abs(window.orientation)},device.noConflict=function(){return window.device=a,this},d=function(a){return-1!==j.indexOf(a)},f=function(a){var b;return b=new RegExp(a,"i"),c.className.match(b)},b=function(a){return f(a)?void 0:c.className+=" "+a},h=function(a){return f(a)?c.className=c.className.replace(a,""):void 0},device.ios()?device.ipad()?b("ios ipad tablet"):device.iphone()?b("ios iphone mobile"):device.ipod()&&b("ios ipod mobile"):device.android()?device.androidTablet()?b("android tablet"):b("android mobile"):device.blackberry()?device.blackberryTablet()?b("blackberry tablet"):b("blackberry mobile"):device.windows()?device.windowsTablet()?b("windows tablet"):device.windowsPhone()?b("windows mobile"):b("desktop"):device.fxos()?device.fxosTablet()?b("fxos tablet"):b("fxos mobile"):b("desktop"),e=function(){return device.landscape()?(h("portrait"),b("landscape")):(h("landscape"),b("portrait"))},i="onorientationchange"in window,g=i?"orientationchange":"resize",window.addEventListener?window.addEventListener(g,e,!1):window.attachEvent?window.attachEvent(g,e):window[g]=e,e()}).call(this);

/**
 * downCount: Simple Countdown clock with offset
 * Author: Sonny T. <hi@sonnyt.com>, sonnyt.com
 */

(function ($) {

    $.fn.downCount = function (options, callback) {
        var settings = $.extend({
                date: null,
                offset: null
            }, options);

        // Throw error if date is not set
        if (!settings.date) {
            $.error('Date is not defined.');
        }

        // Throw error if date is set incorectly
        if (!Date.parse(settings.date)) {
            $.error('Incorrect date format, it should look like this, 12/24/2012 12:00:00.');
        }

        // Save container
        var container = this;

        /**
         * Change client's local date to match offset timezone
         * @return {Object} Fixed Date object.
         */
        var currentDate = function () {
            // get client's current date
            var date = new Date();

            // turn date to utc
            var utc = date.getTime() + (date.getTimezoneOffset() * 60000);

            // set new Date object
            var new_date = new Date(utc + (3600000*settings.offset))

            return new_date;
        };

        /**
         * Main downCount function that calculates everything
         */
        function countdown () {
            var target_date = new Date(settings.date), // set target date
                current_date = currentDate(); // get fixed current date

            // difference of dates
            var difference = current_date - target_date ;

            // if difference is negative than it's pass the target date
            if (difference < 0) {
                // stop timer
                clearInterval(interval);

                if (callback && typeof callback === 'function') callback();

                return;
            }

            // basic math variables
            var _second = 1000,
                _minute = _second * 60,
                _hour = _minute * 60,
                _day = _hour * 24;
                _week = _day * 7;

            // calculate dates
            var weeks = Math.floor(difference / _week),
                days = Math.floor((difference % _week) / _day),
                hours = Math.floor((difference % _day) / _hour),
                minutes = Math.floor((difference % _hour) / _minute),
                seconds = Math.floor((difference % _minute) / _second);

                // fix dates so that it will show two digets
                weeks = (String(weeks).length >= 2) ? weeks : '0' + weeks;
                days = (String(days).length >= 2) ? days : '0' + days;
                hours = (String(hours).length >= 2) ? hours : '0' + hours;
                minutes = (String(minutes).length >= 2) ? minutes : '0' + minutes;
                seconds = (String(seconds).length >= 2) ? seconds : '0' + seconds;

            // based on the date change the refrence wording
            var ref_weeks = (weeks === 1) ? 'week' : 'weeks',
                ref_days = (days === 1) ? 'day' : 'days',
                ref_hours = (hours === 1) ? 'hour' : 'hours',
                ref_minutes = (minutes === 1) ? 'minute' : 'minutes',
                ref_seconds = (seconds === 1) ? 'second' : 'seconds';

            // set to DOM
            container.find('#weeks').text(weeks);
            container.find('#days').text(days);
            container.find('#hours').text(hours);
            container.find('#minutes').text(minutes);
            container.find('#seconds').text(seconds);

            container.find('#weeks_text').text(ref_weeks);
            container.find('#days_text').text(ref_days);
            container.find('#hours_text').text(ref_hours);
            container.find('#minutes_text').text(ref_minutes);
            container.find('#seconds_text').text(ref_seconds);
        };

        // start
        var interval = setInterval(countdown, 1000);
    };

})(jQuery);

/*
 * jQuery Panel Slider plugin v0.0.1
 * https://github.com/eduardomb/jquery-panelslider
*/
(function($) {
  'use strict';

  var $body = $('body'),
      _sliding = false;

  function _slideIn(panel, options) {
    var panelWidth = panel.outerWidth(true),
        bodyAnimation = {},
        panelAnimation = {};

    if(panel.is(':visible') || _sliding) {
      return;
    }

    _sliding = true;
    panel.addClass('ps-active-panel').css({
      position: 'fixed',
      top: 0,
      height: '100%',
      'z-index': 999999
    });
    panel.data(options);
    switch (options.side) {
      case 'left':
        panel.css({
          left: '-' + panelWidth + 'px',
          right: 'auto'
        });
        bodyAnimation['margin-left'] = '+=' + panelWidth;
        panelAnimation.left = '+=' + panelWidth;
        break;

      case 'right':
        panel.css({
          left: 'auto',
          right: '-' + panelWidth + 'px'
        });
        var mainInner = $('.full-width');
    		mainInner.animate({ opacity: 0 }, 300);
        bodyAnimation['margin-left'] = '-=' + panelWidth;
        panelAnimation.right = '+=' + panelWidth;
        break;
    }

    $body.animate(bodyAnimation, options.duration);
    panel.show().animate(panelAnimation, options.duration, function() {
      _sliding = false;
    });
  }

  $.panelslider = function(element, options) {
    var active = $('.ps-active-panel');
    var defaults = {
      side: 'left', // panel side: left or right
      duration: 200, // Transition duration in miliseconds
      clickClose: true // If true closes panel when clicking outside it
    };

    options = $.extend({}, defaults, options);

    // If another panel is opened, close it before opening the new one
    if(active.is(':visible') && active[0] != element[0]) {
      $.panelslider.close(function() {
        _slideIn(element, options);
      });
    } else if(!active.length || active.is(':hidden')) {
      _slideIn(element, options);
    }
  };

  $.panelslider.close = function(callback) {
    var active = $('.ps-active-panel'),
        duration = active.data('duration'),
        panelWidth = $(window).width(), //active.outerWidth(true),
        bodyAnimation = {},
        panelAnimation = {};

    if(!active.length || active.is(':hidden') || _sliding) {
      return;
    }

    _sliding = true;

    switch(active.data('side')) {
      case 'left':
        bodyAnimation['margin-left'] = '-=' + panelWidth;
        panelAnimation.left = '-=' + panelWidth;
        break;

      case 'right':
        bodyAnimation['margin-left'] = '0';
        panelAnimation.right = '-=' + panelWidth;
        var mainInner = $('.full-width');
    		mainInner.animate({ opacity: 1 }, 300);
        break;
    }

    active.animate(panelAnimation, duration);
    $body.animate(bodyAnimation, duration, function() {
      active.hide();
      active.removeClass('ps-active-panel');
      _sliding = false;

      if(callback) {
        callback();
      }
    });
  };

  // Bind click outside panel and ESC key to close panel if clickClose is true
  $(document).bind('click keyup', function(e) {
    var active = $('.ps-active-panel');

    if(e.type == 'keyup' && e.keyCode != 27) {
      return;
    }

    if(active.is(':visible') && active.data('clickClose')) {
      $.panelslider.close();
    }
  });

  // Prevent click on panel to close it
  $(document).on('click', '.ps-active-panel', function(e) {
    e.stopPropagation();
  });

  $.fn.panelslider = function(options) {
    this.click(function(e) {
      var active = $('.ps-active-panel'),
          panel = $(this.getAttribute('href'));

      // Close panel if it is already opened otherwise open it
      if (active.is(':visible') && panel[0] == active[0]) {
        $.panelslider.close();
      } else {
        $.panelslider(panel, options);
      }

      e.preventDefault();
      e.stopPropagation();
    });

    return this;
  };
})(jQuery);
