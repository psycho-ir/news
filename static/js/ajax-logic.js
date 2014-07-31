window.domain = "http://localhost:8000/rest/latest/"
$(document).ready(function(){

    $(".agency-menu .agency-li").on("click",function(){
        agencyID = $(this).data("id");
        url      = window.domain ;
        $.get(url,{
            page_number : 1 ,
            agencies      : agencyID
        },function(data){
            news     = JSON.parse(data);
            htmlNews = createNews(news);
            setTemplate(htmlNews);
        })

    });

    function createNews(news){
            var source       = $("#handlebar-news-box").html();
            var template     = Handlebars.compile(source);
            var html         = template({news : news});
            return html;
    }

    function setTemplate(htmlNews){
         $(".agency-box").html(htmlNews);
    }

});
