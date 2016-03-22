
$(document).ready(function(){
    var window_height = $(window).height();

    $('.body').scroll(function(){
        // alert(window_height + '...'+$('#about').offset().top+"..."+$("#frame").offset().top);
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
    });

})
