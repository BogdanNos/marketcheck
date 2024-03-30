let currentUrl = location.href;
let isRunning = false;
let rule = {"wildberries.ru" : {"tag" : "detail", "selector" : 'h1[class="product-page__title"]'},
            "megamarket.ru" : {"tag" : "details", "selector" : 'h1[itemprop="name"]'},
            "ozon.ru" : {"tag" : "product", "selector" : 'div[data-widget="webProductHeading"]'},
            "market.yandex.ru" : {"tag" : "product", "selector" : 'h1[data-additional-zone="title"]'}};
let domain = window.location.hostname.replace("www.","");

window.addEventListener("load", function(){
    if (currentUrl.includes(rule[domain]["tag"]) && currentUrl.includes(domain)){
        runExtension();
    }
    else
    {
        setInterval(() => {
            if (location.href !== currentUrl) 
            {   
                currentUrl = location.href;

                if (document.querySelector("#market-check-extension")){
                    document.getElementById("market-check-extension").remove();
                }

                if (currentUrl.includes(rule[domain]["tag"])){
                    console.log("PREANADNSDNAS");
                    runExtension();
                } 
            }
        }, 500);
    }
});

function runExtension(){
    const body = document.body;
    const location = window.location.href;
    let name = "";
    if (location.includes(domain) && location.includes(rule[domain]["tag"])){
        isRunning = true;
        onElementAvailable(rule[domain]["selector"], () => {
            name = document.querySelector(rule[domain]["selector"]).textContent;
            body.insertAdjacentHTML('afterbegin', generateHtml(name));
        });
    }
}

//Функция ожидания загрузки элемента
function onElementAvailable(selector, callback) {
    const observer = new MutationObserver(mutations => {
      if (document.querySelector(selector)) {
        observer.disconnect();
        callback();
      }
    });
    observer.observe(document.body, { childList: true, subtree: true });
}
function getStyles(){
    return `
    #market-check-extension {
        background-color:white;
        width: 400px;
        
        z-index:999999;
        position:fixed;
        right:0; 
    }

    #market-check-extension header{
        display: flex;
        justify-content: space-between;
        padding: 5px 40px 5px 40px;
        background-color:#058ED9
    }

    #market-check-extension main{
        padding-left:40px;
        padding-right:40px;
    }

    #market-check-extension header h1 {
        font-family: 'Roboto';
        font-weight: bold;
        font-size: 20px;
      }
    #market-check-extension main h2 {
        font-family: 'Roboto';
        font-size: 14px;
      }
    
    .form_toggle {
        display: inline-block;
        overflow: hidden;
    }
    .form_toggle-item {
        float: left;
        display: inline-block;
    }
    .form_toggle-item input[type=radio] {
        display: none;
    }
    .form_toggle-item label {
        display: inline-block;
        padding: 0px 15px;   
        line-height: 34px;    
        border: 1px solid #999;
        border-right: none;
        cursor: pointer;
        user-select: none;   
    }
     
    .form_toggle .item-1 label {
        border-radius: 6px 0 0 6px;
    }
    .form_toggle .item-2 label {
        border-radius: 0 6px 6px 0;
        border-right: 1px solid #999;
    }
     
    .form_toggle .item-1 input[type=radio]:checked + label {
        background: #D9D9D9;
    }
    .form_toggle .item-2 input[type=radio]:checked + label {
        background: #D9D9D9;
    }  
      
    `
}
function generateHtml(name){
    style = getStyles()
    return `
    <style>
    ${style}
    </style>
    <div id="market-check-extension">
        <header>
            <h1>МАРКЕТЧЕК</h1>
            <button></button>
        </header>
        <main >
            <section class="best-offers">
                <h2>${name}</h2>
                <h2>Лучшие предложения</h2>
                <div class="form_toggle">
                    <div class="form_toggle-item item-1">
                        <input id="fid-1" type="radio" name="radio"  checked>
                        <label for="fid-1">По возрастанию</label>
                    </div>
                    <div class="form_toggle-item item-2">
                        <input id="fid-2" type="radio" name="radio">
                        <label for="fid-2">По популярности</label>
                    </div>
                </div>
            </section>
        </main>
    </div>
    `
}
