$(document).ready(function() {

	$('#tablaExterna').DataTable({
		"order": []
	});

	$("body").on("click", "a.boton_ver", function MostrarDetalles(event) {
		var codigo = $(this).attr('value');

		$.ajax({
			type: "POST",
			url: "/detalles_mensajeria_externa_ajax/",
			data: {
				'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val(),
				'codigo': codigo,
			},

			success: function(data) {
				if (data.hora_entrada == 'None') {
					hora_entrada = 'Pendiente por entregar';
				}
				else {
					hora_entrada = data.hora_entrada;
				}

				if (data.acuse == 'None') {
					acuse = 'Pendiente por entregar';
				}
				else {
					acuse = data.acuse;
				}

				if (data.comentario == 'None') {
					comentario = 'Sin comentario';
				}
				else {
					comentario = data.comentario;
				}

				$('.datos').after().html(
					`<div id='informacion'>
						<div class='input-field col m6 s12'>
							<i class='prefix fas fa-user-circle fa-3x'></i>
							<input disabled id='recepcionista-datos' value='${data.recepcionista}' type='text'>
							<label for='recepcionista-datos'>Recepcionista:</label>
						</div>
						<div class='input-field col m6 s12'>
							<i class='prefix fas fa-user-tie'></i>
							<label for='mensajero-datos'>Mensajero:</label>
							<input disabled id='mensajero-datos' value='${data.mensajero}' type='text'>
						</div>
						<div class='input-field col m6 s12'>
							<i class='prefix far fa-building fa-3x'></i>
							<label for='departamento-datos'>Departamento:</label>
							<input disabled id='departamento-datos' value='${data.departamento}' type='text'>
						</div>
						<div class='input-field col m6 s12'>
							<i class='prefix fas fa-user-graduate fa-3x'></i>
							<label for='encargado-datos'>Encargado:</label>
							<input disabled id='encargado-datos' value='${data.encargado}' type='text'>
						</div>
						<div class='input-field col m6 s12'>
							<i class='prefix far fa-building fa-3x'></i>
							<label for='prioridad-datos'>Prioridad:</label>
							<input disabled id='prioridad-datos' value='${data.prioridad}' type='text'>
						</div>
						<div class='input-field col m6 s12'>
							<i class='prefix far fa-building fa-3x'></i>
							<label for='sucursal-datos'>Sucursal:</label>
							<input disabled id='sucursal-datos' value='${data.sucursal}' type='text'>
						</div>
						<div class='input-field col m6 s12'>
							<i class='prefix far fa-clock fa-3x'></i>
							<label for='hora_salida-datos'>Hora Salida:</label>
							<input disabled id='hora_salida-datos' value='${data.hora_salida}' type='text'>
						</div>
						<div class='input-field col m6 s12'>
							<i class='prefix far fa-clock fa-3x'></i>
							<label for='hora_entrada-datos'>Hora Entrada:</label>
							<input disabled id='hora_entrada-datos' value='${hora_entrada}' type='text'>
						</div>
						<div class='input-field col m6 s12'>
							<i class='prefix fas fas fa-edit fa-3x'></i>
							<label for='acuse-datos'>Acuse:</label>
							<input disabled id='acuse-datos' value='${acuse}' type='text'>
						</div>
						<div class='input-field col m6 s12'>
							<i class='prefix fas fa-info-circle'></i>
							<label for='estado-datos'>Estado:</label>
							<input disabled id='estado-datos' value='${data.estado}' type='text'>
						</div>
						<div class='input-field col m12 s12'>
							<i class='prefix fas fa-comments'></i>
							<label for='comentario-datos'>Comentario:</label>
							<textarea disabled id='comentario-datos' class='materialize-textarea'>${comentario}</textarea>
						</div>
					</div>`

				);

				if (data.archivo)
				{
					if (data.archivo.includes('.png') || data.archivo.includes('.jpg') || data.archivo.includes('.jpge') ||
						data.archivo.includes('.PNG') || data.archivo.includes('.JPG') || data.archivo.includes('.JPGE'))
					{
						$('#informacion').append(
							`<div class='input-field col m12 s12 center'>
							 	<button src='${data.archivo}' class='btn modal-trigger' data-target='datos-imagen'>Ver Acuse</button>
							 </div>`);
					}
					else if (data.archivo.includes('.pdf'))
					{
						$('#informacion').append(
							`<div class='input-field col m12 s12 center'>
								<a href='${data.archivo}' class='btn'>Ver Acuse</a>
							</div>`);
					}
				}

				$('#codigo-datos').text(data.codigo);
				$('#imagen_acuse').attr('src', data.archivo);

			},
			error: function(data) {
				var contenido = {
					'html': `<span>No se pudieron cargar los datos solicitados. \nError: ${data.mensaje}</span>`,
					'classes': 'rounded red text-white',
					'displayLength': 10000,
					'outDuration': 5000,
					'inDuration': 2000,
				}
				M.toast(contenido);
			}
		});
	})
});
