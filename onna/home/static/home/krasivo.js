var search_button = document.getElementById('search_button')
var product_button = document.getElementById('product_button')
var report_button = document.getElementById('report_button')
var user_button = document.getElementById('your_car_values_button')

var market_group = document.getElementById('market_anal')
var product_anal = document.getElementById('product_anal')
var report_anal = document.getElementById('report_anal')
var show_user_inter = document.getElementById('your_car_values')

market_anal.style.display = 'none';
product_anal.style.display = 'none';
report_anal.style.display = 'none';
show_user_inter.style.display = 'none';

var statistic_show = document.getElementById('charts')
var statistic_button = document.getElementById('statistic_button')

statistic_button.addEventListener('click', function(){
    if(statistic_show.style.display=='none'){
        statistic_show.style.display='block'
    }else{
        statistic_show.style.display='none'
    }
});

user_button.addEventListener('click', function(){
    if(show_user_inter.style.display=='none'){
        show_user_inter.style.display='block'
    }else{
        show_user_inter.style.display='none'
    }
});

search_button.addEventListener('click', function(){
    market_anal.style.display = 'block';
    product_anal.style.display = 'none';
    report_anal.style.display = 'none';
});

product_button.addEventListener('click', function(){
    market_anal.style.display = 'none';
    product_anal.style.display = 'block';
    report_anal.style.display = 'none';
});

report_button.addEventListener('click', function(){
    market_anal.style.display = 'none';
    product_anal.style.display = 'none';
    report_anal.style.display = 'block';
});
