document.addEventListener('DOMContentLoaded', ()=>{
    // manage_orders.html

    // click delivered btn
    let delivereds = document.getElementsByClassName('delivered')
    for(i = 0; i < delivereds.length; ++i) {
        delivereds[i].addEventListener('click', function(){
        let order = this.dataset.orderid
        Delivered(order)
        })
    }

    // click cancel btn
    let cancels = document.getElementsByClassName('cancel')
    for(i = 0; i < cancels.length; ++i) {
        cancels[i].addEventListener('click', function(){
        let order = this.dataset.orderid
        Cancel(order)
        })
    }
})

function Cancel(order) {
    let alert = confirm('Are you sure to cancel this order?')
      if(alert) {
          fetch('/cancel', {
              method: 'POST',
              headers:{
                  'Content-Type':'application/json',
                  'X-CSRFToken':csrftoken
              },
              body: JSON.stringify({
                  'order': order
              })
          })
          .then(
              document.querySelector(`.orders[data-orderid="${order}"]`).remove()
          )
        }
}
  
function Delivered(order) {
    fetch('/delivered', {
        method: 'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken
        },
        body: JSON.stringify({
            'order': order
        })
    })
    .then(
        document.querySelector(`.orders[data-orderid="${order}"]`).remove()
    )
}