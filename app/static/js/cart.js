function addToCart(id, name, price) {
    console.log(id)
    console.log(name)
    console.log(price)
    fetch('/cart', {
        method: 'post',
        body: JSON.stringify({
            "id": id,
            "name": name,
            "price": price
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json())
    .then(data => {
        let d = document.getElementsByClassName("cart-counter")
        for (let i = 0; i < d.length; i++)
            d[i].innerText = data.total_quantity
        }).catch(err => console.error(err))
}

function updateCart(flightId, obj) {
    fetch(`/cart/${flightId}`, {
        method: 'put',
        body: JSON.stringify({
            "quantity": obj.value
        }),
        headers: {
            "Content-Type": "application/json"
        }
    }).then(res => res.json()).then(data => {
        let d = document.getElementsByClassName("cart-counter")
        for (let i = 0; i < d.length; i++)
            d[i].innerText = data.total_quantity

        let d2 = document.getElementsByClassName("cart-amount")
        for (let i = 0; i < d2.length; i++)
            d2[i].innerText = data.total_amount.toLocaleString("en-US")
    }).catch(err => console.error(err))
}

function deleteCart(flightId) {
    if (confirm("Bạn chắc chắn xóa không?") == true) {
        fetch(`/cart/${flightId}`, {
            method: 'delete'
        }).then(res => res.json()).then(data => {
            let d = document.getElementsByClassName("cart-counter")
            for (let i = 0; i < d.length; i++)
                d[i].innerText = data.total_quantity

            let d2 = document.getElementsByClassName("cart-amount")
            for (let i = 0; i < d2.length; i++)
                d2[i].innerText = data.total_amount.toLocaleString("en-US")

            let r = document.getElementById(`cart${flightId}`)
            r.style.display = "none"
        }).catch(err => console.error(err))
    }
}

function pay() {
    if (confirm('Bạn chắc chắn thanh toán?') == true) {
        fetch("/pay").then(res => res.json).then(data => location.reload()).catch(err => console.info(err))
    }
}

//function btn() {
//    fetch(`/`, {
//            method: 'show'
//        })
//            const btn = document.querySelector('#btn')
//            const divList = document.querySelector('.divList')
//
//            btn.addEventListener('click', () =>{
//            if(divList.style.display === 'none'){
//                divList.style.display = 'block'
//            }})
//        }).catch(err => console.error(err))
//}

//function show(){
//    d = document.getElementById('divList')
//
//    if(d.style.display == 'none'){
//        d.style.display = 'block' !important
//    }
//    d.style.display = 'block'!important
//}


