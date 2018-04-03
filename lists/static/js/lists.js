var initialize = function () {
    $('input[name="text"]').on('keypress', function () {
        $('.has-danger').hide();
    });
};

initialize();