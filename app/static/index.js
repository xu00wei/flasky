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
})

