headerStyles=`
    #market-check-extension header{
        width:360px;
        display: flex;
        justify-content: space-between;

        background-color: #fff;
    }


    #market-check-extension header h1 {
        /* Text */
        width: 125px;
        height: 36px;
        margin:0;
        font-family: 'Roboto';
        font-style: normal;
        font-weight: 700;
        font-size: 20px;
        line-height: 36px;
        /* identical to box height, or 140% */
        letter-spacing: 0.25px;

        /* Primitives/Black */
        color: #000000;


      }

    #market-check-extension #closeModal {
        position: relative;
        width: 36px;
        height: 36px;
        opacity: 0.2;
        cursor: pointer;
        margin-right:-15px;
        transition: opacity ease 0.5s;
        &:hover {
            opacity: 1;
        }
    }

    #market-check-extension #closeModal::before,
    #market-check-extension #closeModal::after {
    content: '';
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 16px;
    height: 3px;
    background: #000;
    }

    #markethead:hover{
        cursor:pointer;
    }

    #market-check-extension #closeModal::before {
        transform-origin: center;
        transform: translate(-50%, -50%) rotate(45deg);
    }

    #market-check-extension #closeModal::after {
        transform-origin: center;
        transform: translate(-50%, -50%) rotate(-45deg);
    }
`
headerPage= `
    <header id="markethead">
        <h1>МАРКЕТЧЕК</h1>
        <div id="closeModal"></div>
    </header>
`

