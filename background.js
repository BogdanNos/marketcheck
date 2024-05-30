let currentUrl = location.href;
let isRunning = false;
let rule = {"wildberries.ru" : {"tag" : "detail", "selector" : 'h1[class="product-page__title"]'},
            "megamarket.ru" : {"tag" : "details", "selector" : 'h1[itemprop="name"]'},
            "ozon.ru" : {"tag" : "product", "selector" : 'div[data-widget="webProductHeading"]'},
            "market.yandex.ru" : {"tag" : "product", "selector" : 'h1[data-additional-zone="title"]'}};
let domain = window.location.hostname.replace("www.","");
function GetMPImage(name){
    switch(name) {
      case 'megamarket':
        return 'https://i.postimg.cc/SK6xKjqS/e-Zoe-Heox-Ou-Q.jpg'
      case "wildberries":
        return "https://i.postimg.cc/hvqwtPDB/Coy-DKec-S6g-M.jpg"
      case 'ozon':
        return "https://i.postimg.cc/3rgVbp1J/ozon-transformed.jpg"  
      case 'yandex':
        return  "https://i.postimg.cc/VLgTz82x/4y-Fk-R24-Im-K0.jpg"
      default:
          console.log('Invalid selection');
    }
  }

  function formatPrice(number) {
    number=parseInt(number);
    const lastDigit = number % 10;
    const lastTwoDigits = number % 100;

    if (lastTwoDigits >= 11 && lastTwoDigits <= 14) {
        return 'рублей';
    } else if (lastDigit === 1) {
        return 'рубль';
    } else if (lastDigit >= 2 && lastDigit <= 4) {
        return 'рубля';
    } else {
        return 'рублей';
    }
}

function dragElement(elmnt) {
    var pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;
    if (document.getElementById("markethead")) {
      // if present, the header is where you move the DIV from:
      document.getElementById("markethead").onmousedown = dragMouseDown;
    } else {
      // otherwise, move the DIV from anywhere inside the DIV:
      elmnt.onmousedown = dragMouseDown;
    }
  
    function dragMouseDown(e) {
      e = e || window.event;
      e.preventDefault();
      // get the mouse cursor position at startup:
      pos3 = e.clientX;
      pos4 = e.clientY;
      document.onmouseup = closeDragElement;
      // call a function whenever the cursor moves:
      document.onmousemove = elementDrag;
    }
  
    function elementDrag(e) {
      e = e || window.event;
      e.preventDefault();
      // calculate the new cursor position:
      pos1 = pos3 - e.clientX;
      pos2 = pos4 - e.clientY;
      pos3 = e.clientX;
      pos4 = e.clientY;
      // set the element's new position:
      elmnt.style.top = (elmnt.offsetTop - pos2) + "px";
      elmnt.style.left = (elmnt.offsetLeft - pos1) + "px";
    }
  
    function closeDragElement() {
      // stop moving when mouse button is released:
      document.onmouseup = null;
      document.onmousemove = null;
    }
  }

function enable_closed(){
    document.getElementById("market-check-extension-closed").style.display = "flex";
    document.getElementById("market-check-extension").style.display = "None";
    //document.getElementById("market-check-extension-rolled");
}

function enable_full(){
    document.getElementById("market-check-extension-closed").style.display = "None";
    document.getElementById("market-check-extension").style.display = "block";
    //document.getElementById("market-check-extension-rolled");
}

function enable_rolled(){
    document.getElementById("market-check-extension-closed").style.display = "None";
    document.getElementById("market-check-extension").style.display = "None";
    //document.getElementById("market-check-extension-rolled");
}
function enableHover(){
let extra_8648921892381 = document.querySelector('.marketplace-closed-extended');
let more_8216481 = document.querySelector('#market-check-extension-closed');
//let mplace1 = document.getElementsByClassName('marketplace-closed-extra')[0];
//let mplace2 = document.getElementsByClassName('marketplace-closed-extra')[1];
more_8216481.addEventListener('mouseenter', function() {
    extra_8648921892381.style.display = 'Block';
    //extra.style.opacity = 1;
});
more_8216481.addEventListener('mouseleave', function() {
    extra_8648921892381.style.display = 'None';
    //extra.style.opacity = 0;

});
}
window.addEventListener("load", function(){
    console.log(currentUrl);
    runExtension();
    window.navigation.addEventListener("navigate", (event) => {
        console.log(currentUrl);
        if (location.href !== currentUrl){   
            currentUrl = location.href;
            if (document.querySelector("#market-check-extension") || document.querySelector("#market-check-extension-closed")){
                document.getElementById("market-check-extension").remove();
                document.getElementById("market-check-extension-closed").remove();
            }
            if (currentUrl.includes(rule[domain]["tag"])){
                console.log("PREANADNSDNAS");
                runExtension();
            } 
        }
    })
});
/*window.addEventListener("load", function(){
    console.log(currentUrl);
    if (currentUrl.includes(rule[domain]["tag"]) && currentUrl.includes(domain)){
        runExtension();
    }
    else{
        window.navigation.addEventListener("navigate", (event) => {
            console.log(currentUrl);
            if (location.href !== currentUrl){   
                currentUrl = location.href;
                if (document.querySelector("#market-check-extension") || document.querySelector("#market-check-extension-closed")){
                    document.getElementById("market-check-extension").remove();
                    document.getElementById("market-check-extension-closed").remove();
                }
                if (currentUrl.includes(rule[domain]["tag"])){
                    console.log("PREANADNSDNAS");
                    runExtension();
                } 
            }
        })
        //setInterval(() => {
            
        //}, 500);
    }
});*/


function runExtension(){
    const body = document.body;
    const location = window.location.href;
    let name = "";
    
    if (location.includes(domain) && location.includes(rule[domain]["tag"])){
        isRunning = true;
        onElementAvailable(rule[domain]["selector"], () => {
            name = document.querySelector(rule[domain]["selector"]).textContent;
            console.log(name)
       
            let url = `https://192.168.0.112:5000/get_item?product_name=${name.replaceAll('"','')}`;
            //let url = `https://192.168.0.107:5000/test`;
            //w1indow.open(url, '_blank');

            fetch(url).then(function(response) {
                console.log(response)
                return response.json();
            }).then((data) => {
                console.log(data)
                var dataFilter=JSON.parse(JSON.stringify(data));

                for (let i = 3; i >= 0; i--) {
                    var item = data.popular[i];
                    if (location.includes(item.name) || item.items.length===0){
                        dataFilter.popular.splice(i, 1);
                    }
                    item = data.price[i];
                    if (location.includes(item.name) || item.items.length==0){ 
                        dataFilter.price.splice(i, 1);
                    }
                
                }

                console.log(dataFilter)
                body.insertAdjacentHTML('afterbegin', CreateWebPage(dataFilter));
                body.insertAdjacentHTML('afterbegin', CreateClosePage(data.best["price"], data.best["popular"]));
                //body.insertAdjacentHTML('afterbegin', generateHtml(name, data));
            }).catch((e) => {
                console.error('Error: ' + e.message);
                console.log(e.response);
            })
            
        });
        onElementAvailable('div[id="market-check-extension"]', () => {
            document.getElementById("closeModal").onclick = function(){
                enable_closed();
            }
        
            document.getElementById("market-check-extension-closed").onclick = function(){
                enable_full();
            }
            enableHover();
            dragElement(document.getElementById("market-check-extension"));

            const radioButtons = document.querySelectorAll('input[type="radio"][name="radio"]');
            const itemsContainers = document.querySelectorAll('div[class="items-container"]');
            radioButtons.forEach((radioButton, index) => {
                radioButton.addEventListener('change', function() {
                    // Скрываем все контейнеры
                    itemsContainers.forEach(container => container.style.display = 'none');
                    
                    // Определяем индекс выбранной радио-кнопки
                    const selectedIndex = Array.from(radioButtons).indexOf(this);
                    
                    // Отображаем соответствующий контейнер
                    itemsContainers[selectedIndex].style.display = 'block';
                });
            });
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



function generateHtml(name, data1, data2) {
    let style = getStyles();
    let blocksPrice = "Price_content";
    let blocksPopular = "Poppular content";
    
    data1.forEach(marketplace => {
        if (marketplace == -1)
            console.log("Error");
         blocksPrice += `${generateBlock(marketplace)}`
    });

    data2.forEach(marketplace => {
        if (marketplace == -1)
            console.log("Error");
        blocksPopular += `${generateBlock(marketplace)}`
    });
    
    let html = `
        <style>
            ${style}
        </style>
        <div id="market-check-extension">
            <header>
                <h1>МАРКЕТЧЕК</h1>
                <div class="closeModal"></div>
            </header>
            <main>
                <section class="best-offers">
                    <h2>${name}</h2>
                    <h2>Лучшие предложения</h2>
                    <div class="form_toggle">
                        <div class="form_toggle-item item-1">
                            <input id="fid-price" type="radio" name="radio" checked>
                            <label for="fid-price">По возрастанию</label>
                        </div>
                        <div class="form_toggle-item item-2">
                            <input id="fid-popular" type="radio" name="radio">
                            <label for="fid-popular">По популярности</label>
                        </div>
                    </div>
                    <div class="items-container" id = "popular-list">
                    ${blocksPrice}
                    </div>
                    <div class="items-container" id = "price-list" >
                    ${blocksPopular}
                    </div>
                </section>
            </main>
            
        </div>
        `;
    
    return html;
}


