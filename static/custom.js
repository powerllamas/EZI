$(document).ready(function(){
    $('a[rel=popover]').popover({
        placement: 'left'
    }).click(function(e){
        e.preventDefault();
    });

    var search = $('#search');
    search.attr('autocomplete', 'off');
});
