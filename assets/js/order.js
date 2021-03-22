// Variables
let wilaya_price = 0
let product_price = 0
let product_quantity = 1
let discount = 0
// this state is used only when purchasing one product, it will help to manage the data 

let state = {
    'wilaya': 0,
    'product': 0,
    'quantity':1,
    'discount_percentage': 0,
    'discount_amount': 0,
    'order_one_product': false
}

// Input
const url_input = document.querySelector('#order-form')
const commune_input = document.querySelector('#commune')
const delivery_price_container = document.querySelector('#delivery_price')
const order_total_container = document.querySelector('#order_total')
const total_container = document.querySelector("#order_total")
const order_info_list = document.querySelector('#order_info')

let sub_total_container = null
let product_info_container = null
try {
    sub_total_container = document.querySelector("#sub_total")
    product_info_container = document.querySelector("#product_info")
}
catch(err) {
    console.log(err)
}
// Buttons
let edit_quantity_btn, apply_coupon_btn

// Functions

const change_commune = function(e) {

    if(e.target.id == 'wilaya') {
        const url_value = url_input.getAttribute('data-communes-url')
        const wilaya_id = e.target.value
        const url = `http://${window.location.host}${url_value}?wilaya=${wilaya_id}`
        console.log('url', url)
    fetch(url, {
        headers : { 
            'Accept': 'application/json'
           } 
    } )
    .then(response => response.json())
    .then(data => {
        const communes = JSON.parse(data)
       
        commune_input.innerHTML = `<option class="option" value='' selected>Commune</option>`

        for(i = 0; i< communes.length; i++) {
            
            let commune = communes[i]
            console.log('commune key', commune.pk)
            commune_input.innerHTML += `
            <option value="${commune.pk}">${commune.fields.name}</option>
            `
        }
        change_wilaya(wilaya_id)

    })
    .catch(err => {
        // empty communes and price
        commune_input.innerHTML =  `<option class="option" value='' selected>Commune</option>`
        delivery_price_container.innerHTML = ``
        wilaya_price = 0
        state.wilaya = 0
        change_price()
    })

}

const change_wilaya = function(wilaya_id){
    const url = `http://${window.location.host}/commande/fetch/load-wilaya/?wilaya=${wilaya_id}`
    fetch(url, {
        headers : { 
            'Accept': 'application/json'
           } 
    } )
    .then(response => response.json())
    .then(data => {

        const wilaya = JSON.parse(data)[0]
        wilaya_price = wilaya.fields.price
        state.wilaya = wilaya_price
        delivery_price_container.innerHTML = ` ${wilaya_price} DA`
    change_price()
    })
    .catch(err => {
        delivery_price_container.innerHTML = ``
        wilaya_price = 0
        state.wilaya = 0
        change_price()
    })

    }
    
}


// FETCH method to change the product quantity

const change_quantity = function(e) {

    let product_id = edit_quantity_btn.getAttribute('data-product-id')
    let quantity = document.querySelector('#quantity').value
    // Csrf token:
    let csrftoken = getCookie('csrftoken');
    // url 
    const url = `http://${window.location.host}/commande/modifier-quantite/`

    // send my request to change the quantity
    fetch(url, {
        method: 'POST',
        headers : { 
            'Accept': 'application/json',
            "X-CSRFToken": csrftoken
           } ,
        credentials: 'same-origin',
        body: JSON.stringify({'product_id': product_id, 'quantity':quantity, 'discount': discount})
    } )
    .then(response =>  response.json())
    .then(data => {
        result = data
        if (result.success == true){
            state.order_one_product = true
            update_front_after_quantity(result)
        }
        else {
            alert('Une erreur est survenue ou le produit n\'est plus disponible.')
        }
    })
    .catch(err => {
        console.log(err)
    })
}


const apply_coupon = function(e) {

    let coupon_code = document.querySelector("#code").value

    if (coupon_code) {
    // Csrf token:
    let csrftoken = getCookie('csrftoken');
    // url 
    const url = `http://${window.location.host}/commande/ajouter-coupon/`

    // send my request to change the quantity
    fetch(url, {
        method: 'POST',
        headers : { 
            'Accept': 'application/json',
            "X-CSRFToken": csrftoken
           } ,
        credentials: 'same-origin',
        body: JSON.stringify({'coupon_code': coupon_code })
    } )
    .then(response =>  response.json())
    .then(data => {
        result = data
        console.log(data)
        if (result.success == true){
            state.order_one_product = true
            update_front_after_coupon(result)
        }
        else {
            alert('Une erreur est survenue ou le coupon n\'est plus disponible.')
        }
    })
    .catch(err => {
        console.log(err)
    })
    }
    else {
        alert('Vous n\'avez rien saisi dans le champ coupon')
    }
}

// The following function are copying from  : get csrf token
// https://docs.djangoproject.com/en/dev/ref/csrf/#ajax
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Change price after wilaya update

const change_price = function() {
    
    if(state.order_one_product == true) {
        const delivery_price_container = document.querySelector('#delivery_price')
        const order_total_container = document.querySelector('#order_total')
        delivery_price_container.innerHTML = `${parseFloat(state.wilaya).toFixed(2)}`
        order_total_container.innerHTML = `${get_price().toFixed(2)} DA`
    }

    else {
        const total_without_delivery = parseFloat(order_total_container.getAttribute('data-order-total'))
        const total_price = parseFloat(total_without_delivery)+ parseFloat(wilaya_price)
        order_total_container.innerHTML = `${total_price} DA`
    }
}



const update_front_after_quantity = function(result) {

    let total_container, sub_total_container

    try {
    total_container = document.querySelector("#order_total")
    sub_total_container = document.querySelector("#sub_total")
    }
    catch {
        console.log('no sub total')
    }

    // update my state
    state.product = parseFloat(result['price'])
    state.quantity = result['quantity']
    console.log('happening here')
    console.log(state)
    // update the front 
    if (product_info_container) {
        product_info_container.innerHTML = `${result.name} x ${result.quantity} <span>${parseFloat(result['total-product']).toFixed(2)} DA</span>`
    }
    if(sub_total_container) {
        const sub_total_price = parseFloat(state.product) * state.quantity + parseFloat(state.wilaya)
        sub_total_container.innerHTML = `${sub_total_price.toFixed(2)} DA`
    }
    console.log(total_container)
    total_container.setAttribute("data-order-total",  get_price().toFixed(2))
    total_container.innerHTML =  `${ get_price().toFixed(2)} DA`
}

// Function to apply a coupon

const update_front_after_coupon = function(result) {
    const total_price_before = parseFloat(state.product) * parseFloat(state.quantity)
    let reduction

    if (result.percentage != 0) {
        state.discount_percentage = result.percentage
        state.discount_amount = 0
        reduction = `${result.percentage} %`
    }
    else {
        state.discount_amount = result.discount
        state.discount_percentage = 0
        reduction = `- ${result.discount} DA`
    }

    const new_element =  `
    <li>Coupon: <div><strong id="coupon_code">${result.code}<strong></div></li>
    <li>Réduction<span id="coupon_reduction">${reduction}</span></li>
    <li>Livraison<span id="delivery_price">${parseFloat(state.wilaya).toFixed(2)} DA</span></li>
    <li>SOUS TOTAL <span id="sub_total">${total_price_before.toFixed(2)} DA</span></li>
    <li class="total">TOTAL<span class="dark" id="order_total" data-order-total="${get_price().toFixed(2)}">${get_price().toFixed(2)} DA</span></li>`

    order_info_list.innerHTML = new_element
}

// Used for ordering one product
const get_price = function() {
    console.log(state)
    let product_cost = parseFloat(state.product) * parseFloat(state.quantity)

    if(state.discount_amount !=0) {
        console.log(state.discount_amount)
        product_cost -= parseFloat(state.discount_amount)
    }

    if(state.discount_percentage !=0) {
        document.querySelector('#order_total').getAttribute('data-order-total')
        product_cost = product_cost - (product_cost * parseFloat(state.discount_percentage) / 100)
        console.log(state.discount_percentage)
    }
    console.log(typeof product_cost)
    product_cost = product_cost +  parseFloat(state.wilaya)
    return parseFloat(product_cost)
}

window.addEventListener('DOMContentLoaded', function() {

    order_total_container.innerHTML = `${document.querySelector('#order_total').getAttribute('data-order-total')} DA`
    state.product = parseFloat(document.querySelector('#order_total').getAttribute('data-order-total'))

    url_input.addEventListener('change', change_commune)
    
    // Get elements from the order one product part
    try {
        edit_quantity_btn = document.querySelector('#edit-product-quantity')
        apply_coupon_btn = document.querySelector('#apply-coupon')

        edit_quantity_btn.addEventListener('click', change_quantity)
        apply_coupon_btn.addEventListener('click', apply_coupon)
    }

    catch(err) {
        console.log('Not in order one product')
    }
});