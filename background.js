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

function generateHtml(name){
    return `
    <div id="market-check-extension" style="background-color:white; width: 300px; height:600px; z-index:999999; position:fixed; right:0;">
        <header>
            <h1>МАРКЕТЧЕК</h1>
        </header>
        <main>
            <section class="best-offers">
                <h2>${name}</h2>
                <h2>Лучшие предложения</h2>
                <p>
                    <a href="#">По возрастанию цены</a> (от 126.000 рублей)
                </p>
                <p>
                    <a href="#">По популярности на WB</a> (от 26.000 рублей)
                </p>
            </section>
        </main>
    </div>
    `
}
