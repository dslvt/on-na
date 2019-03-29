var search_button = document.getElementById('search_button')
var product_button = document.getElementById('product_button')
var report_button = document.getElementById('report_button')

var market_group = document.getElementById('market_anal')
var product_anal = document.getElementById('product_anal')
var report_anal = document.getElementById('report_anal')

market_anal.style.display = 'none';
product_anal.style.display = 'none';
report_anal.style.display = 'none';

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
