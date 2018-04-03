window.superlists = {};

window.superlists.initialize = function () {
    $('input[name="text"]').on('keypress', function () {
        $('.has-danger').hide();
    });
};


$(document).ready(function(){
    window.superlists.initialize();
});