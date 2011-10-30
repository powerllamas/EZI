$(document).ready(function(){
    $('a[rel=popover]').popover({
        placement: 'left'
    }).click(function(e){
        e.preventDefault();
    });

    var search = $('#search');
    search.attr('autocomplete', 'off');
    search.smartAutoComplete({
      filter: function(term, source) {
                return $.Deferred(function(dfd){
                  $.getJSON('/guesses.json', {
                    search: term
                  }).success( function(data){
                    dfd.resolve( data.guesses );
                  });
                }).promise();
              }
    });
});
