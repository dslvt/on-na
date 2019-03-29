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
var search_result = document.getElementById('search_result')

search_button.addEventListener('click', function(){
    $.ajax({
        url:'query/',
        data:{
            'mark':input_mark.value,
            'model':input_model.value,
            'year':[input_year_from.value, input_year_to.value],
            'engine':[input_eng_capacity_from.value, input_eng_capacity_to.value],
            'millage':[input_mileage_from.value, input_mileage_to.value],
            'kpp':input_transmission_type.value
        },
        dataType: 'json',
        success:function(data){
            search_result.innerHTML = data['response']
        },
        fail:function(data){
            search_result.innerHTML = "Cannot find"
        }
    });
});
