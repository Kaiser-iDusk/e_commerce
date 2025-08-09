$(document).ready(function() {
    $('.add-to-cart').click(function(e) {
        e.preventDefault();
        var pk = $(this).data('pk');
        $.post('/add_to_cart/' + pk + '/', function(data) {
            alert('Added to cart');
        });
    });
});