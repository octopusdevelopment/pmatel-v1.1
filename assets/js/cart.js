// Inputs 
let products_container = document.querySelector('#products')
let total_input = document.querySelector('#total')
let label_cart_count = document.querySelector('#label-cart-count')
let sub_total_input
try {
    sub_total_input = document.querySelector('#sub-total')
}
catch(err) {
    console.log("No sub total input")
}

// The following function are copying from 
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

const update_front = function(quantity_input, total_product_input, result) {
    result = JSON.parse(result)
    quantity_input.value = result["quantity"]
    total_product_input.innerHTML = `${result["total-product"]} DA`
    try {
        sub_total_input.innerHTML = `${parseFloat(result["sub-total"]).toFixed(2)} DA`
    }
    catch (err) {
        console.log('No sub total - do not worry it is okay')
    }
    total_input.innerHTML = `${parseFloat(result["total"]).toFixed(2)} DA`
    label_cart_count.innerHTML = `${result["number-products"]}`
    
}
const change_quantity = function(e) {

    if(e.target.id.startsWith('edit-product')) {
        let id = e.target.id.split('-')[2]
        let quantity_input = document.querySelector(`#quantity-product-${id}`)
        let total_product_input = document.querySelector(`#total-product-${id}`)
       
        let quantity = quantity_input.value
        // Csrf token:
        let csrftoken = getCookie('csrftoken');

        // Url
        const url = `${window.location.protocol}://${window.location.host}/panier/modifier/${id}/`


    fetch(url, {
        method: 'POST',
        headers : { 
            'Accept': 'application/json',
            "X-CSRFToken": csrftoken
           } ,
        credentials: 'same-origin',
        body: JSON.stringify({'quantity':quantity})
    } )
    .then(response =>  response.json())
    .then(data => {
        result = JSON.stringify(data)

        update_front(quantity_input, total_product_input, result)
    })
    .catch(err => {
        console.log(err)
    })
}
}

products_container.addEventListener('click', change_quantity)