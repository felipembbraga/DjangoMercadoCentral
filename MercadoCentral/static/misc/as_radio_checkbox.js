$(function(){
    $('body').bind('DOMNodeInserted', '.as-radio', function () {
        $('.as-radio').unbind('change');
        console.log($('.as-radio'));
        $('.as-radio').bind('change', function(event) {
            var currentId = $(this).attr('id');
            if($(this).prop('checked')){
                $('.as-radio:not(#' + currentId + ')').each(function() {
                    $(this).prop('checked', false);
                });
            }

        });
    });

});