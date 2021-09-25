var contextMenuItem = {
    "id": "See Timeline",
    "title": "See Timeline",
    "contexts": ["selection"]
};

chrome.contextMenus.create(contextMenuItem);


chrome.contextMenus.onClicked.addListener(function(clickData){   
    if (clickData.menuItemId == "See Timeline" && clickData.selectionText){    
                  
        chrome.storage.sync.get('headline', function(obj){

            var news = clickData.selectionText;
            chrome.storage.sync.set({'headline': news}, function(){               
                if (news != ""){
                    var notifOptions = {
                        type: "basic",
                        iconUrl: "logo.png",
                        title: "Timeline Found!",
                        message: "We got a perfect timeline for you. Hope You Enjoy:))"
                    };
                    chrome.notifications.create('FoundNotif' + Date.now().toString(), notifOptions);
                }
            });
        });
    }
});