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
var input_price_user = document.getElementById('price_user')
var input_h_power = document.getElementById('u_h_power')

var search_button = document.getElementById('search_button')
var product_button = document.getElementById('product_button')
var report_button = document.getElementById('report_button')

var table = document.getElementById('product_table')

var download_link_button = document.getElementById('download_link_button')
var sent_to_email_button = document.getElementById('email_button')
var email_text = document.getElementById('email_text')

function create_trunsm(){
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
    return transm
}

search_button.addEventListener('click', function(){
    transm = create_trunsm()
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
            document.getElementById('std_market').innerHTML = 'Standard deviation: ' + data['std']+'₽';
            document.getElementById('mean_market').innerHTML = "Mean: " + data['mean']+'₽';
            document.getElementById('n_market').innerHTML = "Amount: " + data['n'];
        },
        fail:function(data){
            search_result.innerHTML = "Cannot find"
        }
    });
});

product_button.addEventListener('click', function(){
    transm = create_trunsm()
    $.ajax({
        url:'product/',
        data:{
            'mark':input_mark.value,
            'model':input_model.value,
            'year':[input_year_from.value, input_year_to.value],
            'engine':[input_eng_capacity_from.value, input_eng_capacity_to.value],
            'millage':[input_mileage_from.value, input_mileage_to.value],
            'kpp':transm,
            'u_year':input_user_year.value,
            'u_eng':input_eng_cap_user.value,
            'u_mileage':input_mileage_user.value,
            'u_price':input_price_user.value,
            'u_h_power':input_h_power.value,
        },
        dataType:'json',
        success:function(data) {
            table.rows[1].cells[2].innerHTML = data['multi_r']
            table.rows[2].cells[2].innerHTML = data['r_sqr'],
            table.rows[3].cells[2].innerHTML = data['norm_r'],
            table.rows[4].cells[2].innerHTML = data['std'],
            table.rows[5].cells[2].innerHTML = data['n']
        },
        fail:function(data){
        }
    });
});

sent_to_email_button.addEventListener('click', function(){
    transm = create_trunsm()
    $.ajax({
        url:'report/',
        data:{
            'mark':input_mark.value,
            'model':input_model.value,
            'year':[input_year_from.value, input_year_to.value],
            'engine':[input_eng_capacity_from.value, input_eng_capacity_to.value],
            'millage':[input_mileage_from.value, input_mileage_to.value],
            'kpp':transm,
            'u_year':input_user_year.value,
            'u_eng':input_eng_cap_user.value,
            'u_mileage':input_mileage_user.value,
            'u_price':input_price_user.value,
            'u_h_power':input_h_power.value,
            'email':email_text.value,
        },
        dataType:'json',
        success:function(data) {
            download_link_button.setAttribute('href', data['url'])
        },
        fail:function(data){
        }
    });
})
