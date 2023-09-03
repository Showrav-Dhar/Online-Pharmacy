var updateBtns = document.getElementsByClassName ('update-cart')

for(var i = 0; i<updateBtns.length; i++){
    debugger;
    updateBtns[i].addEventListener('click',function(e){
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log('Click event triggered for productId:',productId, 'action:', action)

        console.log('USER : ',user)
        if (user == 'AnonymousUser'){
            addCookieItem(productId,action)
        }else{
            updateUserOrder(productId,action)
        }
    })
}

function addCookieItem(productId,action){
    console.log('Not Logged in........')

    if(action == 'add'){
        if(cart[productId] == undefined){
            cart[productId] = {'quantity':1}
        }else{
            cart[productId]['quantity'] += 1
        }
    }

    if(action == 'remove'){
        cart[productId]['quantity'] -= 1

        if(cart[productId]['quantity']<=0){
            console.log('REMOVE ITEM')
            delete cart[productId]
        }
    }
    console.log('Cart :',cart)
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
    
    if(action == 'add'){
        let cart_update_count = parseInt(document.getElementById('cart-total').innerText) + 1;
        document.getElementById('cart-total').innerText = cart_update_count ;
    }

    if(action == 'remove'){
        let cart_update_count = parseInt(document.getElementById('cart-total').innerText) - 1;
        document.getElementById('cart-total').innerText = cart_update_count ;
    }

   
    location.reload()

}



function updateUserOrder(productId,action){
    debugger;
    console.log('User is logged in , Sending Data....')

    var url = '/update_item/'

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type' : 'application/json',
            'X-CSRFTOKEN': csrftoken,
        },
        body: JSON.stringify({'productId': productId,'action': action})
    })

    .then((response)=>{
        return response.json()
    })


    .then((data)=>{
        debugger;
        console.log('data', data)
        if(data.action == 'add'){
            let cart_update_count = parseInt(document.getElementById('cart-total').innerText) + 1;
            document.getElementById('cart-total').innerText = cart_update_count ;
        }
    
        if(data.action == 'remove'){
            let cart_update_count = parseInt(document.getElementById('cart-total').innerText) - 1;
            document.getElementById('cart-total').innerText = cart_update_count ;
        }

        location.reload()
    })

    
}

//cart working fine