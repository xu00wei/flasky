$(document).ready(function(){
    var navbar_site = $("#navbar").offset().top;
    $(window).scroll(function(){
        var window_top_site = $(this).scrollTop();
        if(navbar_site <= window_top_site){
            $("#navbar").css({ "position":"fixed", "top":"0" });
        }
        else{
            $("#navbar").css("position","static");
        }
    })
})

