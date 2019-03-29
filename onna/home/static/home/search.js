var input_mark = document.getElementById('input_mark');
var input_model = document.getElementById('input_model');
var input_year_to = document.getElementById('input_year_to')
var input_year_from = document.getElementById('input_year_from')
var input_eng_capacity_from = document.getElementById('eng_capacity_from')
var input_eng_capacity_to = document.getElementById('eng_capacity_to')
var input_mileage_from = document.getElementById('mileage_from')
var input_mileage_to = document.getElementById('mileage_to')
var input_transmission_type = document.getElementById('trainsmission')
var search_result = document.getElementById('search_result')

var tr_robot = document.getElementById('tr_robot')
var tr_automat = document.getElementById('tr_automat')
var tr_variator = document.getElementById('tr_variator')
var tr_mechanic = document.getElementById('tr_mechanic')

var input_user_year = document.getElementById('input_year_user')
var input_eng_cap_user = document.getElementById('eng_capacity_user')
var input_mileage_user = document.getElementById('mileage_user')

var search_button = document.getElementById('search_button')
var product_button = document.getElementById('product_button')
var report_button = document.getElementById('report_button')


search_button.addEventListener('click', function(){
    transm = []

    if(tr_automat.checked){
        transm.push('automat')
    }
    if(tr_mechanic.checked){
        transm.push('mechanika')
    }
    if(tr_variator.checked){
        transm.push('vibator')
    }
    if(tr_robot.checked){
        transm.push('robot')
    }
    console.log(transm)
    $.ajax({
        url:'query/',
        data:{
            'mark':input_mark.value,
            'model':input_model.value,
            'year':[input_year_from.value, input_year_to.value],
            'engine':[input_eng_capacity_from.value, input_eng_capacity_to.value],
            'millage':[input_mileage_from.value, input_mileage_to.value],
            'kpp':transm
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

product_button.addEventListener('click', function(){
    $.ajax({
        url:'product/',
        data:{},
        dataType:'json',
        success:function(data) {

        },
        fail:function(data){

        }
    });
});

report_button.addEventListener('click', function(){
    $.ajax(
        url:'report/',
        data:{},
        dataType:'json',
        success:function(data) {

        },
        fail:function(data){

        }
    );
})
