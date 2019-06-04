$(document).ready(function() {

    $.ajax({
        type: "GET",
        url: "/cargar_usuarios_ajax/",
        data: {},

        success: function(data) {
            $('input.usuarios').autocomplete({
                data: data.usuarios,
                limit: 4,
                onAutocomplete: function(val) {},
            });
        },
        error: function(data) {
            var contenido = {
                'html': '<span>No se pudieron cargar los nombres de los usuarios.</span>',
                'classes': 'rounded red text-white',
                'displayLength': 10000,
                'outDuration': 5000,
                'inDuration': 2000,
            }
            M.toast(contenido);
        }
    });
});