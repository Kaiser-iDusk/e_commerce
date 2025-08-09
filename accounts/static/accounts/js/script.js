$(document).ready(function() {
    $('form').submit(function() {
        if ($('#id_username').val() === '') {
            alert('Username required');
            return false;
        }
    });
});