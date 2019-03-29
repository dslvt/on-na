var search_field = document.querySelector('#search_input_field')
var search_button = document.querySelector('#search_button')

search_button.addEventListener('click', function(){
    $.ajax({
        url:'query/',
        data:{
            'select':search_field.value
        },
        dataType: 'json',
        success:function(data){
            if(data.is_taken){
                console.log("seccess: "+search_field.value)
            }
        }
    });
});
