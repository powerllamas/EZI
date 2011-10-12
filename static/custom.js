$(document).ready(function(){
    $('a[rel=popover]').popover({
        placement: 'left'
    }).click(function(e){
        e.preventDefault();
    });
});
