var search_button = document.getElementById('search_button');
var market_anal = document.getElementById('market_anal')
market_anal.style.display = 'none';

search_button.addEventListener('click', function(){
    market_anal.style.display = 'block';
    $.ajax({
        url:'market/',
        data:{},
        dataType:'json',
        success:function(data) {
            document.getElementById('std_market').innerHTML = "Standard deviation: " + data['std']
            document.getElementById('mean_market').innerHTML = "Mean: "+ data['mean']
            document.getElementById('n_market').innerHTML = "Amount: "+ data['n']
        },
        fail:function(data){
        }
    });
});
