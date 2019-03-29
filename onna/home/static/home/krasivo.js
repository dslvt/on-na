var input_mark = document.getElementById('input_mark');
var input_model = document.getElementById('input_model');
var input_year_to = document.getElementById('input_year_to')
var input_year_from = document.getElementById('input_year_from')
var input_eng_capacity_from = document.getElementById('eng_capacity_from')
var input_eng_capacity_to = document.getElementById('eng_capacity_to')
var input_mileage_from = document.getElementById('mileage_from')
var input_mileage_to = document.getElementById('mileage_to')
var input_transmission_type = document.getElementById('trainsmission')
var search_button = document.getElementById('search_button')

search_button.addEventListener('click', function(){
    console.log(input_year_to.value)
    $.ajax({
        url:'query/',
        data:{
            'select':input_mark.value
        },
        dataType: 'json',
        success:function(data){
            if(data.is_taken){
                console.log("seccess: "+search_field.value)
            }
        }
    });
});
