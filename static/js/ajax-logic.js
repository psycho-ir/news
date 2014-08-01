window.domain = "http://localhost:8000/rest/latest/"
window.pageNumber = 0 ;
window.agencyId   = 0 ;
$(document).ready(function(){

    $(".agency-menu .agency-li").on("click",function(){
        window.pageNumber = 1 ;
        window.agencyId   = $(this).data("id");
        callServer(window.pageNumber,agencyId,"refresh")
    });

    $(window).scroll(function() {
        if($(window).scrollTop() == $(document).height() - $(window).height()) {
            window.pageNumber+= 1;
            if (window.agencyId == 0){
                callServer(window.pageNumber,0,"append");
            }
            else {
                callServer(window.pageNumber,window.agencyId,"append");
            }
        }
    });

    function callServer(pageNumber,agencyId,type){
        url      = window.domain ;
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



});
