$(function(){
    
    chrome.storage.sync.get('headline',function(obj){
        $('#headline').text(obj.headline);

        var xmlhttp = new XMLHttpRequest();

        xmlhttp.onreadystatechange = function() {
            if (xmlhttp.readyState == XMLHttpRequest.DONE) {
                console.log(xmlhttp.status);
                if (xmlhttp.status == 200) {
                    let articles = JSON.parse(xmlhttp.responseText);
                    generateTemplate(articles);
                } else {
                    document.getElementById('error').style.display = "block"
                }
            }
        };

        // Place your api key which you get from https://newsapi.org/
        query = obj.headline;
        query = query.replace("%20"," ")
        // console.log(query);
        // var punctuationless = query.replace(/[.,\/#!$%\^&\*;:{}=\-_`~()]/g,"");
        // query = punctuationless.replace(/\s{2,}/g," ");
        
        url = 'http://127.0.0.1:5000/news/'+query
        // url = `https://gnews.io/api/v4/search?q=${query}&lang=en&token=1cd6508cc51c3072bbd892ca2d30f886`
        xmlhttp.open("GET", url, true);
        xmlhttp.send();

        // Generating only 5 news at a time
        function generateTemplate(newsArray) {
            
            let template = '';
            for (let i = 0; i < 10; i++) {
                let current = newsArray[i];
                template += `<br><div class="news row">
                                <div class="col-md-12">
                                    <h3>${current['title']}</h3>
                                    <p>${current['desc']}</p>
                                    <h6> <a href=${current['link']}>Link to full article</a></h6>
                                    <h6> Source: ${current['media']} </h6>
                                    <h6> Published ${current['date']} </h6>
                                </div>
                                </div><hr>`
            }
            document.getElementById('newsData').innerHTML = template;
        }
    })

    
    
//     // $('#typed').click(function(){
//     //     chrome.storage.sync.get('typedHeadline', function(obj){
            
//     //         var news = $('#typedHeadline').val();

//     //         chrome.storage.sync.set({'headline': news}, function(){               
//     //             if (news != ""){
//     //                 var notifOptions = {
//     //                     type: "basic",
//     //                     iconUrl: "logo.png",
//     //                     title: "Timeline Found!",
//     //                     message: "We got a perfect timeline for you. Hope You Enjoy:))"
//     //                 };
//     //                 chrome.notifications.create('Found' + Date.now().toString(), notifOptions);
//     //             }
//     //         });

//     //         $('#typedHeadline').text(news);
//     //     })
//     // })


});