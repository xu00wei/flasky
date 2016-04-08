$(document).ready(function(){
    /*function myfun(){*/
        //window_height = $(window).height();
        ////window_width = $(window).width();
        ////input_width = window_width - 250;
        ////post_contaiter_height = window_height - 50;
        //post_text_height = window_height - 160;

        ////$('.head-input input').css("width",input_width+"px");
        ////$('.post-container').css("height",post_contaiter_height+"px");
        //$('form .post-text').css("height", post_text_height+"px");
    //}
    /*myfun();*/
    if ($(window).width() <= 768){
            $("#post_submit").attr("value","发表");
    }
    else{ $("#post_submit").attr("value","发表文章"); }

    //$(window).resize(myfun);
    $(window).resize(function(){
        if ($(window).width() <= 768){
            $("#post_submit").attr("value","发表");
        }
        else{ $("#post_submit").attr("value","发表文章"); }
    })

    /*$(".bold").click(function(){*/
        ////select_font = document.selection.createRange();
        //select_font = window.getSelection();
        //alert(select_font);
        //select_font.execCommand("Bold");
    /*})*/
    $(".close-preview").click(function(){
        $('#flask-pagedown-body-preview').css("display","none");
        $('.flask-pagedown').css("width","100%");
        $(this).css("display","none");
        $(".open-preview").css("display","block");
    })

    $(".open-preview").click(function(){
        $(".flask-pagedown").css("width","45%");
        $("#flask-pagedown-body-preview").css("display","block");
        $(this).css("display","none");
        $(".close-preview").css("display","block");
    })
})
