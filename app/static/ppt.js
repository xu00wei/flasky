
$(document).ready(function(){
    var window_height = $(window).height();

    $('#title .center .line').animate({width:"0px"}, '5000', function(){
        $('#title .up').css({"position":"fixed", "top":"0"});
        $('#title .down').css({"position":"fixed", "bottom":"0"});
        $('#title .up, #title .down').css("height","50%");
        $('#title .center').animate({width:"0px", height:"0px"}, '5000', function(){
            $('#title .up, #title .down').animate({height:"0px"}, 'slow');
        });
        $("#title .title").css("display","inline");
    });

    $('.circle').mousemove(function(){
        $(this).css("background","rgba(255,255,255,0.3)");
    });

    $('.circle').mouseleave(function(){
        $(this).css("background","rgba(255,255,255,0.6)");
    })

    $('.body').scroll(function(){
        // alert(window_height + '...'+$('#title').offset().top+"..."+$("#frame").offset().top);
        var active_li = $('#navbar-vertical ul .active');
        var div_id = active_li.children().attr("href");
        var now_div = $(div_id);
        //alert(div_id+":"+now_div.offset().top);

        if ( now_div.offset().top > 0 ){
                       active_li.removeClass("active").animate( {} ,'speed', function(){
                active_li.prev().addClass("active").animate( {} , 'speed', function(){
                    active_li.prev().children()[0].click();
                });
            });
        }
        else if( now_div.offset().top < 0 ){
                       active_li.removeClass("active").animate( {} ,'speed', function(){
                active_li.next().addClass("active").animate( {} , 'speed', function(){
                    active_li.next().children()[0].click();
                });
            });
        }
        else return;
    });

})
