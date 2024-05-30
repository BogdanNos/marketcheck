ClosedStyle = 
`<div id="market-check-extension-closed">   
<style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,100;0,300;0,400;0,500;0,700;0,900;1,100;1,300;1,400;1,500;1,700;1,900&display=swap');
    #market-check-extension-closed{
        font-family: "Roboto";
        width: 380px;
        background-color: #050C4D;
        display: flex;
        color: white;
        flex-direction: column;
        border-radius: 12px;
        position: fixed;
        right: 10px;
        bottom: 10px;
        transition: 0.5s;
        z-index:999999;
        /*display: none;*/
    }
    .show-more-closed{
        display: flex;
        flex-direction: row;
    }
    .show-more-closed:hover{
        cursor: pointer;   
        background-color: #122194;   
        border-radius: 12px;      
    }
    .show-more-closed h1{
        font-size: 20px;
        letter-spacing: 0.25px;
        line-height: 28px;
        text-align: left;
        color: white;
        margin: 0;
    }
    
    .show-more-closed div{
        width: 260px;
        padding: 16px 0 16px 16px;
    }
    .show-more-closed p{
        font-size: 14px;
        line-height: 20px;
        text-align: left;
        color: white;
        margin: 0;
        margin-top: 4px;
    }
    .show-more-closed svg{
        align-self: center;
        transition: 0.5s;
        width: 100px;
        fill: white;
    }
    .marketplace-closed-extra{
        width: 330px;
        margin: 0 auto;
        background-color: #050C4D;
        display: flex;
        flex-direction: row;
        
        margin-bottom: 32px;
        padding: 16px;
        border-radius: 12px;
    }
    .marketplace-closed-extra div{
        width: 250px;
    }
    .marketplace-closed-extended{
        background-color: white;
        flex-direction: row;
        display: none;
    }
    .marketplace-closed-extra div h1{
        font-size: 20px;
        font-weight: bold;
        margin-top: 0;
        margin-bottom: 26px;
    }
    .marketplace-closed-extra img{
        width: 80px;
        height: 80px;
        border-radius: 10px;
    }
    .marketplace-closed-extended h2{
        text-align: center;
        width: 100%;
        margin: 16px 0;
        color: black;
        font-size: 28px;
        font-weight: bold;
    }

    .marketplace-closed-extra div a{
        text-decoration: none;
        color: black;
        padding: 10px;
        font-size: 14px;
        transition: 0.5s;
        font-weight: bold;
        background-color: white;
        border-radius: 50px;
    }
    .marketplace-closed-extra div a:hover{
        background-color: rgb(200, 200, 200);
    }

</style>
`
function CreateClosePage(priceItem,popularItem) {
    Closed=
    
    `
    ${ClosedStyle}
    <div class="marketplace-closed-extended">
        <h2>Лучшие предложения</h2>
        <div class="marketplace-closed-extra">
            <div>
                <h1>
                    По популярности
                </h1>
                <a href="${popularItem.url}">от ${popularItem.price} ${formatPrice(popularItem.price)}</a>
            </div>
            <img width="100" height="100" src="${GetMPImage(popularItem.marketplace)}"></img>
        </div>
        <div class="marketplace-closed-extra">
            <div>
                <h1>
                    По возрастанию
                </h1>
                <a href="${priceItem.url}">от ${priceItem.price} рублей</a>
            </div>
            <img width="100" height="100" src="${GetMPImage(priceItem.marketplace)}"></img>
        </div>
    </div>
    <div class="show-more-closed">
        <div>
            <h1>
                Предложения на других маркетплейсах
            </h1>
            <p>Нажмите чтобы посмотреть</p>
        </div>
        <svg xmlns="http://www.w3.org/2000/svg" style="color: white;" x="0px" y="0px" width="100" height="100" viewBox="0 0 50 50">
        <path d="M 21 3 C 11.6 3 4 10.6 4 20 C 4 29.4 11.6 37 21 37 C 24.354553 37 27.47104 36.01984 30.103516 34.347656 L 42.378906 46.621094 L 46.621094 42.378906 L 34.523438 30.279297 C 36.695733 27.423994 38 23.870646 38 20 C 38 10.6 30.4 3 21 3 z M 21 7 C 28.2 7 34 12.8 34 20 C 34 27.2 28.2 33 21 33 C 13.8 33 8 27.2 8 20 C 8 12.8 13.8 7 21 7 z"></path>
        </svg>
    </div>
    <script> 
    </script>
    </div>
    `;
    return Closed;
}