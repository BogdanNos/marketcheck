// Get the reference to the HTML body element
const WebPage = `
<div style="background-color:white; width: 300px; height:100px; z-index:999; position:fixed; right:0;">
    <header>
        <h1>МАРКЕТЧЕК</h1>
    </header>
    <main>
        <section class="best-offers">
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
`;
window.onload=function(){

    const body = document.body;
    body.insertAdjacentHTML('afterbegin', WebPage);
}
// Add a paragraph element after the existing content
