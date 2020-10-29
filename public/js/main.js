// testing the API call interface

document.addEventListener('DOMContentLoaded',function(){

    console.log('loaded');

    call('ping',function(r){
        console.log('r',r);
    },{
        a : 1,
        b : [
            {
                c : 1
            }
        ],
        d : {
            r : '123'
        }
    })

})