window.apiDomain   = "/rest/";
window.pageNumber  = 0 ;
window.agencyId    = 0 ;

$(document).ready(function(){

    loadLastNews();
    loadLastPrice();
    $(".agency-menu .agency-li").on("click",function(){
        window.pageNumber = 1 ;
        window.agencyId   = $(this).data("id");
        callServerForNews(window.pageNumber,agencyId,"refresh")
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
    function callServerForBookmark(newsId,token,object){
        var url           = window.apiDomain + 'bookmark/';
        var sendingObject = {
            news_id : newsId ,
            csrfmiddlewaretoken : token
        };
        $.post(url,sendingObject,function(data){
            data = JSON.parse(data);
            if (data.message = 'Bookmark saved')
               $(object).toggleClass('btn-inverse btn-default');
            else
               $(object).toggleClass('btn-default btn-inverse');
        })
    }
    function callServerForLike(newsId,token,object){
        var url           = window.apiDomain + 'like/';
        var sendingObject = {
            news_id : newsId ,
            csrfmiddlewaretoken : token
        };
        $.post(url,sendingObject,function(data){
            data = JSON.parse(data);
            if (data.message = 'Like removed')
               $(object).toggleClass('btn-inverse btn-default');
            else
               $(object).toggleClass('btn-default btn-inverse');
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
    function callServerForPrice(){
        var url = window.apiDomain + 'price/' ;
        var sendingObject = null;
        $.get(url,sendingObject,function(data){
            if (data == "{}") return false;
            var price = JSON.parse(data);
            price.forEach(function(object,b){
                $("#"+object.item).text(numberWithCommas(object.price));
            })

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
         attachHandler();
    }
    function appendTemplate(){
         $(".agency-box").append(htmlNews);
         attachHandler();
    }
    function loadLastNews(){
        callServerForNews(1,0,"refresh");
    }
    function attachHandler(){
        var token = $("#csrfmiddlewaretoken").val();
        $(".not-like-bind").on("click",function(){
            var newsId = $(this).data("id");
            callServerForLike(newsId,token,this);

        }).toggleClass('not-like-bind is-bind');

        $(".not-bookmark-bind").on("click",function(){
            var newsId = $(this).data("id");
            callServerForBookmark(newsId,token,this);
        }).toggleClass('not-bookmark-bind is-bind');
    }
    function loadLastPrice(){
        callServerForPrice();
    }
    function numberWithCommas(number) {
        return number.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    }
});
