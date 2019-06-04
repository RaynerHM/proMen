$(document).ready(function () {

	$('#video_ayuda')[0].pause();

	$('#tabla').DataTable({
		"order": []
	});

	$("body").on("click", "button.btn-detalles", function MostrarDetalles(event) {
	// $('.btn-detalles').click(function MostrarDetalles() {
		var codigo = $(this).attr('value');

		$.ajax({
			type: "POST",
			url: "/detalles_mensajeria_interna_ajax/",
			data: {
				'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val(),
				'codigo': codigo,
			},

			success: function (data) {

				if (data.fecha_entrega == 'Pendiente por entregar') {
					fecha_entrega = 'Pendiente por entregar';
				}
				if (data.comentario == 'None') {
					comentario = 'Sin comentario';
				}

				$('.datos').after().html(
					`<div class='input-field col m6 s12'>
						<i class='prefix fas fa-user-circle fa-3x'></i>
						<input disabled id='recepcionista_datos' value='${data.recepcionista}' type='text'></p>
						<label for='recepcionista_datos'>Recepcionista:</label>
					</div>
					<div class='input-field col m6 s12'>
						<i class='prefix fas fa-people-carry fa-3x'></i>
						<label for='recibido_por'>Recibido Por:</label>
						<input disabled id='recibido_por' value='${data.recibido_por}' type='text'></p>
					</div>
					<div class='input-field col m6 s12'>
						<i class='prefix far fa-building fa-3x'></i>
						<label for='sucursal-datos'>Sucursal:</label>
						<input disabled id='sucursal-datos' value='${data.sucursal}' type='text'></p>
					</div>
					<div class='input-field col m6 s12'>
						<i class='prefix far fa-clock fa-3x'></i>
						<label for='fecha_entrega-datos'>Fecha Entrega:</label>
						<input disabled id='fecha_entrega-datos' value='${data.fecha_entrega}' type='text'></p>
					</div>
					<div class='input-field col m6 s12'>
						<i class='prefix far fa-eye fa-3x'></i>
						<label for='observacion_datos'>Observacion:</label>
						<textarea disabled id='observacion_datos' class='materialize-textarea'>${data.observacion}</textarea>
					</div>
					<div class='input-field col m6 s12'>
						<i class='prefix fas fa-comments fa-3x'></i>
						<label for='comentario_datos'>Comentario:</label>
						<textarea disabled id='comentario_datos' class='materialize-textarea'>${comentario}</textarea>
					</div>`
					);

				$('#codigo-datos').text(data.codigo);

			},
			error: function (data) {
				var contenido = {
					'html': `<span>Error: ${data.mensaje}</span>`,
					'classes': 'rounded red text-white',
					'displayLength': 10000,
					'outDuration': 5000,
					'inDuration': 2000,
				}
				M.toast(contenido);

			}
		});
	});
});
