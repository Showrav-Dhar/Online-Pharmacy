var updateBtns = document.getElementsByClassName('update-cart')

for(var i = 0; i<updateBtns.length; i++){
    updateBtns[i].addEventListener('click',function(){
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log('Click event triggered for productId:',productId, 'action:', action)

        console.log('USER : ',user)
        if (user == 'AnonymousUser'){
            console.log('Not Logged in')
        }else{
            console.log('User is logged in , Sending Data....')
        }
    })
}
// ajke push korlam 