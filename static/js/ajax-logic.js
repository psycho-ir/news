window.apiDomain            = "/rest/";
window.pageNumber           = 0 ;
window.bookmarkPageNumber   = 0 ;
window.agencyId             = 0 ;
window.activeTab            = "#tab-1";
$(document).ready(function(){

    loadLastNews();
    loadLastPrice();
    loadLastBookmark();
    $(".agency-menu .agency-li").on("click",function(){
        window.pageNumber = 1 ;
        window.agencyId   = $(this).data("id");
        callServerForNews(window.pageNumber,agencyId,"refresh")
    });
    $(".tab-list li").on("click",function(){
        var a = $(this).find("a");
        window.activeTab = a.attr("href");
    })
    $(window).scroll(function() {
        if($(window).scrollTop() == $(document).height() - $(window).height()) {
            var activeTab = window.activeTab;
            if( activeTab == '#tab-1'){
                window.pageNumber+= 1;
                if (window.agencyId == 0){
                    callServerForNews(window.pageNumber,0,"append");
                }
                else {
                    callServerForNews(window.pageNumber,window.agencyId,"append");
                }
            }
            else if ( activeTab == '#tab-4' ){
                window.bookmarkPageNumber+= 1;
                callServerForBookmarkList(window.bookmarkPageNumber);
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

    function callServerForBookmarkList(pageNumber){
        var url           = window.apiDomain + 'list_bookmark/';
        sendingObject = {
               page_number : pageNumber
            }
         $.get(url,sendingObject,function(data){

            if (data == "{}" || data == '[]') return false;

            news     = JSON.parse(data);
            htmlNews = createNews(news);
            appendTemplate(htmlNews,".bookmark-box");

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
            if ( data == "{}" || data == "[]") return false;
            news     = JSON.parse(data);
            htmlNews = createNews(news);
            if (type == "refresh")
                setTemplate(htmlNews,'.agency-box');
            else
                appendTemplate(htmlNews,'.agency-box');
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
    function setTemplate(htmlNews,DOM){
         $(DOM).html(htmlNews);
         attachHandler();
    }
    function appendTemplate(htmlNews,DOM){
         $(DOM).append(htmlNews);
         attachHandler();
    }
    function loadLastNews(){
        window.pageNumber = 1 ;
        callServerForNews(window.pageNumber,0,"refresh");
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

    function loadLastBookmark(){
        window.bookmarkPageNumber = 1 ;
        callServerForBookmarkList(window.bookmarkPageNumber);
    }

    function numberWithCommas(number) {
        return number.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    }
});
