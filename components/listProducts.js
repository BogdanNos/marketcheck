listProductsStyles=`
 .marketplace{
  height: 100px;
  display: flex;  
  flex-direction: row;
  margin-bottom: 8px;
 }

 .marketText {
  width: 250px;
  padding: 16px 10px;
  display: flex-inline;
 
  
 }
 
 .market_img{
  width: 110px;
  padding-left: 12px;
  display: flex;
  align-items: center;
 }

 .marketphoto{
  height: 90px;
  width: 90px;
  border-radius: 18px;
 }
 


 .marketсard{
  display: flex;
  flex-direction: row;
  border: solid #E8E8E8;
  border-width: 2px;
  margin-bottom: 8px;
  height: 120px;
 }
 .marketplace + .marketсard{
  border-radius: 12px 12px 0% 0%;
 }
 .prod_info{
  width: 250px;
  padding: 16px 10px;
 }
 .prod_info h3{
  text-align: right;
  font-size: 14px !important;
  font-weight: regular;
  margin: 0;
 }
 .marketText h2{
  margin: 0;
 }
 .prod_info p{
  text-align: right;
 }
 .prod_img{
  width: 110px;
  padding-left: 12px;
  display: flex;
  align-items: center;
 }

 .productphoto{
  height: 90px;
  width: 90px;
  border-radius: 10px;
  object-fit: contain
  
 }

 .more_market{
  display: flex;
  width: 360px;
  flex-direction: row;
  background-color: black;
  border-radius: 0 0 12px 12px;
  height: 45px;
  text-decoration: none;
  padding: 10px 0 0 0;
  
  justify-content: space-around;
  margin-bottom: 24px;
 }

 .more_market h1{
  font-size: 18px;
  font-weight: 600;
  line-height: 24px;
  color: white;
  margin: 0;
  padding: 0;
 }
 
 .more_arrow{
  width: 24px;
  height: 24px;
 }
 

 
  .button_product{

    float:right;
  }
  .button_market{

    float:left;
  }
  .list_button{
    margin-top:10px;
    background-color: #E8E8E8;
    padding:10px;
    border-radius: 40px / 50px;
    display: flex;
    gap:10px;
    font-family: 'Roboto';
    font-style: normal;
    font-weight: 600;
    font-size: 16px;
    line-height: 19px;
    color: #000000;
    align-items: center;
  }
  .{

  }
`

function GetMPImage(name){
  console.log(name);
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

function CreateListProducts(items,nameMarketplace) {
  let listProducts = `
      <div class = "marketplace">
        <div class = "marketText">
            <h2>от 180р</h2> 
            <a class="list_button button_market" href="#" target="_blank">Подробнее<svg width="6" height="9" viewBox="0 0 6 9" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M0.333313 0.5H2.86664L5.93331 4.5L2.86664 8.5H0.333313L3.39998 4.5L0.333313 0.5Z" fill="black"/>
            </svg>
            \</a>
        </div>
        <div class="market_img"> 
          <img class="marketphoto" src="${GetMPImage(nameMarketplace)}">
        </div>
      </div>
  `;

  items.forEach(item => {
      listProducts += `
          <div class="marketсard">
              <div class="prod_img">
              <img class="productphoto"  src="${item.image}" alt="${item.name}">
              </div>
              <div class="prod_info">
                <h3>${item.name.substring(0, 50)}</h3>
              <a class="list_button button_product" href="${item.url}" target="_blank">${item.price}    <svg width="6" height="9" viewBox="0 0 6 9" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M0.333313 0.5H2.86664L5.93331 4.5L2.86664 8.5H0.333313L3.39998 4.5L0.333313 0.5Z" fill="black"/>
              </svg>
              \</a>
              </div>
              
          </div>`;
  });
  listProducts+= '<a class="more_market" href="#" target="_blank"> \
  <div class="more_arrow"></div>\
  <h1>Больше предложений</h1>\
  <svg class="more_arrow" width="21" height="18" viewBox="0 0 21 18" fill="none" xmlns="http://www.w3.org/2000/svg">\
  <path d="M20.2 9L13.7 18H10.2L15.7 10.5H0V7.5H15.7L10.2 0H13.7L20.2 9Z" fill="white"/>\
  </svg>\
  </a>'
  return listProducts
}