window.apiDomain = "http://localhost:8000/rest/"
window.pageNumber = 0 ;
window.agencyId   = 0 ;
$(document).ready(function(){

    $(".agency-menu .agency-li").on("click",function(){
        window.pageNumber = 1 ;
        window.agencyId   = $(this).data("id");
        callServerForNews(window.pageNumber,agencyId,"refresh")
    });

    $(".like-news").on("click",function(){
        var newsId = $(this).data("id");
        var token  = $(this).data("token");
        callServerForLike(newsId,token);
    });

    $(".bookmark-news").on("click",function(){
        var newsId = $(this).data("id");
        var token  = $(this).data("token");
        callServerForBookmark(newsId,token);
    });

    $(window).scroll(function() {
        if($(window).scrollTop() == $(document).height() - $(window).height()) {
            window.pageNumber+= 1;
            if (window.agencyId == 0){
                callServerForNews(window.pageNumber,0,"append");
            }
            else {
                callServerForNews(window.pageNumber,window.agencyId,"append");
            }
        }
    });

    function callServerForBookmark(newsId,token){
        var url           = window.apiDomain + 'bookmark/';
        var sendingObject = {
            news_id : newsId ,
            csrfmiddlewaretoken : token
        };
        $.post(url,sendingObject,function(data){

        })
    }

    function callServerForLike(newsId,token){
        var url           = window.apiDomain + 'like/';
        var sendingObject = {
            news_id : newsId ,
            csrfmiddlewaretoken : token
        };
        $.post(url,sendingObject,function(data){

        })
    }

    function callServerForNews(pageNumber,agencyId,type){
        var url = window.apiDomain + 'latest/' ;
        var sendingObject = null;
        if (agencyId == 0){
            sendingObject = {
               page_number : pageNumber
            }
        }else {
            sendingObject = {
               page_number : pageNumber ,
               agencies      : agencyId
            }
        }
        $.get(url,sendingObject,function(data){
            if (data == "{}") return false;
            news     = JSON.parse(data);
            htmlNews = createNews(news);
            if (type == "refresh")
                setTemplate(htmlNews);
            else
                appendTemplate(htmlNews);
        })
    }

    function createNews(news){
            var source       = $("#handlebar-news-box").html();
            var template     = Handlebars.compile(source);
            var html         = template({news : news });
            return html;
    }

    function setTemplate(htmlNews){
         $(".agency-box").html(htmlNews);
    }
    function appendTemplate(){
         $(".agency-box").append(htmlNews);
    }

    function likeNews(){

    }

});
