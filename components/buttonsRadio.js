radioStyles=`
    #market-check-extension .form_toggle {
        margin-bottom:15px;
        display: flex;
    }
    #market-check-extension .form_toggle-item {
        float: left;
        width: 180px;
    }
    #market-check-extension .form_toggle-item input[type=radio] {
        display: none;
    }
    #market-check-extension .form_toggle-item label {
        display: flex;
        cursor: pointer;
        align-items: center;
        justify-content: center;
        height: 60px;
        opacity: 0.5;
        border-bottom:4px solid;

        font-family: 'Roboto';
        font-style: normal;
        font-weight: 500;
        font-size: 14px;
        /* identical to box height, or 114% */

    }
    .offers{
        width: 360px;
    }
    #market-check-extension .form_toggle-item label iframe {
        height: 16px;
        margin-right:10px;
        width:16px;
        border:none;
    }

    #market-check-extension .form_toggle .item-price input[type=radio]:checked + label {
        opacity: 1;
    }
    #market-check-extension .form_toggle .item-popular input[type=radio]:checked + label {
        opacity: 1;
    }  
`
radioPage=`
    <div class="form_toggle">
        <div class="form_toggle-item item-price">
            <input id="fid-price" type="radio" name="radio" >
            <label for="fid-price">
                
                <iframe src="https://svgshare.com/f/15HR" class="toggle-iframe"></iframe>
                <div>По возрастанию </div>
               
            </label>
            </div>
            <div class="form_toggle-item item-popular">
            <input id="fid-popular" type="radio" name="radio" checked="">
            <label for="fid-popular">
                
                <iframe src='https://svgshare.com/f/15HS' width=100% height=100% ></iframe>
                <div>По популярности</div>
               
            </label>
        </div>
    </div>

`