document.addEventListener('DOMContentLoaded', ()=>{

    // accordion effects
    let acc = document.getElementsByClassName('accordion')
    for(i = 0; i < acc.length; ++i) {
        acc[i].addEventListener('click', function(){
            let panel = this.nextElementSibling
            if (panel.style.display === 'none') {
                panel.style.display = 'block'
            } else {
                panel.style.display = 'none'
            }
        })
    }

    // search input
    let input = document.getElementsByTagName('input')
    for(i = 0; i < input.length; ++i) {
        input[i].addEventListener('input', function(){
            sum()
        })
    }

})

// show total items and amount
function sum() {
    let totalItems = 0
    let totalAmount = 0
    let input = document.getElementsByTagName('input')

    for(i = 0; i < input.length; ++i) {
        if(input[i].value > 0) {
            totalItems += parseInt(input[i].value)
            // get the product id for each input
            let price = document.querySelector(`.price_col[data-productid="${input[i].dataset.productid}"]`).innerHTML
            totalAmount += parseInt(input[i].value) * price
        }
    }
    
    document.getElementById("totalItems").innerHTML = totalItems
    document.getElementById("amount").innerHTML = totalAmount.toFixed(2)
}