$(document).ready(function() {

    $.ajax({
        type: "GET",
        url: "/cargar_departamentos_ajax/",
        data: {},

        success: function(data) {
                $('input.autocomplete').autocomplete({
                    data: data.dep,
                    limit: 4,
                    onAutocomplete: function(val) {
                        if (val != "") {
                            $('#departamento').val(data.dep_con_id[val]);
                        } else {
                            alert('ERROR:\n\nEl departemento seleccionado, es incorrecto o esta mal escrito.');
                        }
                    },
                });
        },
        error: function(data) {
            var contenido = {
                'html': '<span>No se pudieron cargar los nombres de los departamentos.</span>',
                'classes': 'rounded red text-white',
                'displayLength': 10000,
                'outDuration': 5000,
                'inDuration': 2000,
            }
            M.toast(contenido);
        }
    });
});