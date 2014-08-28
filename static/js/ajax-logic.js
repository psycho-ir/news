window.apiDomain            = "/rest/";
window.pageNumber           = 0 ;
window.bookmarkPageNumber   = 0 ;
window.categoryPageNumber   = 0 ;
window.agencyId             = 0 ;
window.categoryId           = 0 ;
window.activeTab            = "#tab-1";
window.activeRole           = "last-news"; // last-news - category - agency
$(document).ready(function(){

    loadLastNews();
    loadLastPrice();
    loadLastBookmark();
    loadCategories();
    loadDate();
    $(".agency-menu .agency-li").on("click",function(){
        window.pageNumber = 1 ;
        window.activeRole = 'agency';
        window.agencyId   = $(this).data("id");
        callServerForNews(window.pageNumber,agencyId,"refresh")
    });

    $(".tab-list li").on("click",function(){
        var a = $(this).find("a");
        window.activeTab = a.attr("href");
    })
    $(window).scroll(function() {
        if($(window).scrollTop() == $(document).height() - $(window).height()) {
            var activeTab  = window.activeTab;
            var activeRole = window.activeRole;
            var notLoading = true;
            if( activeTab == '#tab-1'){

                if(activeRole == "last-news"){
                    window.pageNumber+= 1;

                    callServerForNews(window.pageNumber,0,"append",notLoading);
                }
                else if ( activeRole == "category" ){
                    window.categoryPageNumber+= 1;

                    callServerForCategoryNews(window.categoryPageNumber,window.categoryId,"append",notLoading);
                }
                else {
                    window.pageNumber+= 1;
                    callServerForNews(window.pageNumber,window.agencyId,"append",notLoading);
                }

                /*if (window.agencyId == 0){
                    callServerForNews(window.pageNumber,0,"append");
                }
                else {
                    callServerForNews(window.pageNumber,window.agencyId,"append");
                }*/
            }
            else if ( activeTab == '#tab-4' ){
                window.bookmarkPageNumber+= 1;
                callServerForBookmarkList(window.bookmarkPageNumber,notLoading);
            }

        }
    });
    function callServerForBookmark(newsId,token,object){
        var url           = window.apiDomain + 'bookmark/';
        var sendingObject = {
            news_id : newsId ,
            csrfmiddlewaretoken : token
        };
        activatePreLoader();
        $.post(url,sendingObject,function(data){
            data = JSON.parse(data);
            if (data.message = 'Bookmark saved')
               $(object).toggleClass('btn-inverse btn-default');
            else
               $(object).toggleClass('btn-default btn-inverse');
            $('.bookmark-box').html('');
            window.bookmarkPageNumber = 1;
            callServerForBookmarkList(window.bookmarkPageNumber);
            inactivatePreLoader();
        })
    }
    function callServerForBookmarkList(pageNumber,notLoading){
        var url           = window.apiDomain + 'list_bookmark/';
        sendingObject = {
               page_number : pageNumber
            }
        if (!notLoading) activatePreLoader();
         $.get(url,sendingObject,function(data){
            if (data == "{}" || data == '[]'){
                 inactivatePreLoader();
                 return false;
            }
            news     = JSON.parse(data);
            htmlNews = createNews(news);
            appendTemplate(htmlNews,".bookmark-box");
            if (!notLoading) inactivatePreLoader();
        })

    }
    function callServerForLike(newsId,token,object){
        var url           = window.apiDomain + 'like/';
        var sendingObject = {
            news_id : newsId ,
            csrfmiddlewaretoken : token
        };
        activatePreLoader();
        $.post(url,sendingObject,function(data){
            data = JSON.parse(data);
            if (data.message = 'Like removed')
               $(object).toggleClass('btn-inverse btn-default');
            else
               $(object).toggleClass('btn-default btn-inverse');
            inactivatePreLoader();
        })
    }
    function callServerForNews(pageNumber,agencyId,type,notLoading){
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
         if (!notLoading) activatePreLoader();
        $.get(url,sendingObject,function(data){
            if ( data == "{}" || data == "[]") {
                 inactivatePreLoader();
                 return false;
            }

            news     = JSON.parse(data);
            htmlNews = createNews(news);
            if (type == "refresh")
                setTemplate(htmlNews,'.agency-box');
            else
                appendTemplate(htmlNews,'.agency-box');
            if (!notLoading) inactivatePreLoader();
        })
    }
    function callServerForPrice(){
        var url = window.apiDomain + 'price/' ;
        var sendingObject = null;
        $.get(url,sendingObject,function(data){
            if (data == "{}" || data =="[]"){
                inactivatePreLoader();
                return false;
            }
            var price = JSON.parse(data);
            price.forEach(function(object,b){
                $("#"+object.item).text(numberWithCommas(object.price));
            })
        })
    }
    function callServerForCategory(){
        var url = window.apiDomain + 'all_categories/' ;
        var sendingObject = null;
        $.get(url,sendingObject,function(data){
            if (data == "{}" || data =="[]") return false;
            var html = "";
            data.forEach(function(object,b){
                var li = $("<li></li>").attr('id',object.pk).text(object.fields.local_name);
                $(".category-menu").append(li).append('<li class="divider"></li>');
            })
            setHandlerForCategory();
        })
    }
    function callServerForCategoryNews(pageNumber,categoryId,type,notLoading){
        var url = window.apiDomain + 'latest/' ;
        var sendingObject = null;

            sendingObject = {
               page_number : pageNumber ,
               categories      : categoryId
            }
        if (!notLoading) activatePreLoader();
        $.get(url,sendingObject,function(data){
            if ( data == "{}" || data == "[]"){
                inactivatePreLoader();
                return false;
            }
            news     = JSON.parse(data);
            htmlNews = createNews(news);
            if (type == "refresh")
                setTemplate(htmlNews,'.agency-box');
            else
                appendTemplate(htmlNews,'.agency-box');
             if (!notLoading) inactivatePreLoader();
        })
    }
    function callServerForDate(){
        var url = window.apiDomain + 'date/' ;
        $.get(url,null,function(data){
            if ( data == "{}" || data == "[]") return false;
            date  = JSON.parse(data);
            $(".latest").text( 'تاریخ آخرین بروزرسانی :‌ ' + date.latest);
            $(".today").text( 'امروز - ' + date.today);
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
    function loadCategories(){
        callServerForCategory();
    }
    function setHandlerForCategory(){
        $(".category-menu li").on("click",function(){
            window.categoryPageNumber = 1 ;
            window.activeRole = 'category';
            window.categoryId   = $(this).attr("id");
            callServerForCategoryNews(window.categoryPageNumber,window.categoryId,"refresh")
        });
    }
    function loadDate(){
        callServerForDate();
    }
    function numberWithCommas(number) {
        return number.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    }
    function activatePreLoader(){
        $('#modal-preloader').modal("show");
    }
    function inactivatePreLoader(){
        $('#modal-preloader').modal("hide");
    }

});
