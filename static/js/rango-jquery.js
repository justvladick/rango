$(document).ready(function() {
// JQuery code to be added in here.
    $('#likes').click(function() {
        var catid;
        catid = $(this).attr("data-catid");
        $.get('/rango/like/', {category_id: catid})
            .done(function(data) {
                $('#like_count').html(data);
                $('#likes').hide();
            });
    });
    $('#suggestion').keyup(function(){
        $.get('/rango/suggest/', {'suggestion': $(this).val()} )
            .done(function(data) {
                $('#cats').html( data )

            });
    });
});