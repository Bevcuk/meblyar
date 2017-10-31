$(document).ready(function() {
    $('select#id_from_id').on('click', function() {
        var template = ($(this).find(':selected').text()).split(' - ')[1];
        $('textarea#id_extra_parameters_json').val(template);
    });
});