function CreateWebPage(data){

   
    WebPage = `
    <div id="market-check-extension">

    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,100;0,300;0,400;0,500;0,700;0,900;1,100;1,300;1,400;1,500;1,700;1,900&display=swap')
    </style>
    <style>

        #market-check-extension * {
        }
        #market-check-extension {
            display: None;
            background-color: white;
            z-index:999999;
            position:fixed;
            padding:0 10px 0 20px;
            right:0; 
            top: 100px;
            width:400px;
            border:1px solid #E8E8E8;
            border-radius: 12px;
        }
        .scroll {
            height: 400px; /* Высота блока */
            /*margin-left:-10px;*/
            overflow-y: scroll; 
            position: relative;
            width: 370px;
            padding-right: 5px;
        }
        .scroll::-webkit-scrollbar {
            width: 5px;
        }
        
        .scroll::-webkit-scrollbar-thumb {
            border-radius: 10px;
            background-color: #060602;
        }
        ${headerStyles}
        ${radioStyles}
        ${listProductsStyles}
    </style>
    ${headerPage}
    <div class="offers">${radioPage}</div>
    <main class="scroll">
    `
    WebPage+='<div class="items-container" id = "price-list" style="display:none">'
    data.price.forEach(item => {
        WebPage+=CreateListProducts(item.items,item.name);
    })
    WebPage+='</div>'
    WebPage+='<div class="items-container" id = "popular-list" >'
    data.popular.forEach(item => {
        WebPage+=CreateListProducts(item.items,item.name);
    })
    WebPage+=
    `
    </div>
    </main>
    </div>
    `
    return WebPage}