//$(document).ready(function(){
    //var navbar_site = $("#navbar").offset().top;
    //$(window).scroll(function(){
        //var window_top_site = $(this).scrollTop();
        //if(navbar_site <= window_top_site){
            //$("#navbar").css({ "position":"fixed", "top":"0", "opacity":"0.3" });
        //}
        //else{
            //$("#navbar").css({"position":"static", "opacity":"1"});
        //}
    //})
//})
//
$(document).ready(function(){
    var need_remove_circle = true;
    var window_width = $(window).width();

    $(".nav-mobile").click(function(){
        if(need_remove_circle){
            $(".nav-mobile").removeClass("glyphicon-menu-hamburger");
            $(".nav-mobile").addClass("glyphicon-remove-circle");
            need_remove_circle = false;
        }
        else{
            $(".nav-mobile").removeClass("glyphicon-remove-circle");
            $(".nav-mobile").addClass("glyphicon-menu-hamburger");
            need_remove_circle = true;
        }
    });

    $(window).resize(function(){
        now_window_width = $(window).width();
        if(now_window_width <= 768 && window_width > 768 && $('#title').attr("class") != "full-title"){
            $("#title").addClass("mobile-left-title").removeClass("left-title");
            window_width = now_window_width;
        }
        else if( now_window_width> 768 && window_width <= 768 && $('#title').attr("class") != "full-title"){
            $('#title').addClass("left-title").removeClass("mobile-left-title");
            window_width = now_window_width;
        }
    });

    $(".go-index").click(function(){
        if( $(window).width() >= 768 && $('#title').attr("class") == "full-title"){
            $("#title").animate({ width:'25%'},'normal',function(){
                $("#title").addClass("left-title").removeClass("full-title").removeAttr("style");
            });
            $('.index-content').css("display","block");
        }
        else{
            $("#title").animate({ height:'20%' }, 'normal', function(){
                 $("#title").addClass("mobile-left-title").removeClass("full-title").removeAttr("style");
            });
            $('.index-content').css("display","block");

        }
    });
})


