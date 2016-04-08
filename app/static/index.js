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
    var window_height = $(window).height();
    var posts_order_nav_activer = $(".order-nav .activeit");
    var page_nav_activer = $(".page-nav ul").children('li.active');

    function navIconChange(){
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
    };
    $(".nav-mobile").click(navIconChange);
    /*
     *  窗口调整监听
     */
    $(window).resize(function(){
        now_window_width = $(window).width();
        login_height = $(window).height() - 50;

        $('.login').css("height",login_height+"px");

        if(now_window_width <= 768 && window_width > 768 && $('#title').attr("class") != "full-title"){
            $("#title").addClass("mobile-left-title").removeClass("left-title");
            $("#index-content").addClass("mobile-index-content").removeClass("index-content");
            $(".index-font .font").css("display", "none");
            $(".index-font .long-line").css("display","none");

            window_width = now_window_width;
        }
        else if( now_window_width> 768 && window_width <= 768 && $('#title').attr("class") != "full-title"){
            $('#title').addClass("left-title").removeClass("mobile-left-title");
            $("#index-content").addClass("index-content").removeClass("mobile-index-content");
            $(".index-font .font").css("display","block");
            $(".index-font .long-line").css("display","block");
            window_width = now_window_width;
        }
    });
    /*
     *  首页点击事件
     */
    $(".go-index").click(function(){
        if ( $('#title').attr("class") != "full-title" )    return;

        if( $(window).width() >= 768 ){
            $("#title").animate({ width:'25%'},'normal',function(){
                $("#title").addClass("left-title").removeClass("full-title").removeAttr("style");
                $('.dropdown').css("display","block");
                $('#index-content').css("display","block");
                $('.index-bgcolor').css("background-position","-500px 0px");
            });
        }
        else{
            $(".nav-mobile").click();
            $(".index-font .font").css("display", "none");
            $(".index-font .long-line").css("display","none");
            $("#title").animate({ height:'140px' }, 'normal', function(){
                $('#nav-head').css("display","none");
                $('.dropdown').css("display","block");
                $("#title").addClass("mobile-left-title").removeClass("full-title").removeAttr("style");
                $('#index-content').addClass("mobile-index-content").removeClass("index-content").css("display","block");
            });

        }
    });


    /**
     *  最新，最热，随便看的文章序列导航条点击事件
     */
    $(".order-nav li").click(function(){
        posts_order_nav_activer.removeClass("activeit");
        posts_order_nav_activer = $(this);
        posts_order_nav_activer.addClass("activeit");
    });

    /**
     *  千絮，时光，留香的页面导航条点击事件
     */
    $(".page-nav li").click(function(){
        page_nav_activer.removeClass("active");
        page_nav_activer = $(this);
        page_nav_activer.addClass("active");
    })
})


