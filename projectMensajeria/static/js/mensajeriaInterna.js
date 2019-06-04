$(document).ready(function() {

	$('#remitente').on('keyup', function(txt){
			var palabra = txt.split(' ');
			var lista = [];

			for (let num = 0; num < palabra.length; num++) {
				lista.push(palabra[num].toString().substr(0, 1).toUpperCase() + palabra[num].slice(1).toLowerCase());
			}

			return lista.join(' ');
	});

	$('#tabla').DataTable({
		"order": []
	});

	moment.locale('es-DO');

	var div_tercero = (`<div id='div-tercero' class='input-field col m12'>
		<i class='prefix fas fa-users fa-3x'></i>
		<input id='tercero' name='tercero' type='text' class='usuarios' autocomplete='off'>
		<label for='tercero'>Nombre de Tercero</label>
		</div>`);

	var id_mensajeria = 0;
	var estado = '';
	var r_ext = '';

	$("body").on("click", "button.btn-detalles", function MostrarDetalles(event) {
		var codigo = $(this).attr('value');

		$.ajax({
			type: "POST",
			url: "/detalles_mensajeria_interna_ajax/",
			data: {
				'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val(),
				'codigo': codigo,
			},

			success: function(data) {
				if (data.tipo_remitente == 'True') {
					tipo_remitente = 'Externo';
				}
				else if (data.tipo_remitente == 'False') {
					tipo_remitente = 'Interno';
				};

				if (data.fecha_entrega == 'Pendiente por entregar') {
					fecha_entrega = 'Pendiente por entregar';
				}
				else {
					fecha_entrega = (`${data.fecha_entrega.split(' ')[0].split('-').reverse().join('-')} a las ${data.fecha_entrega.split(' ')[1].split('.')[0]}`)
				}

				$('.datos').after().html(`
					<div class='input-field col m4 s12'>
						<i class='prefix fas fa-user-circle fa-3x'></i>
						<input disabled id='recepcionista_datos'value='${data.recepcionista}' type='text'></p>
						<label for='recepcionista_datos'>Recepcionista:</label>
					</div>
					<div class='input-field col m4 s12'>
						<i class='prefix fas fa-people-carry fa-3x'></i>
						<label for='recibido_por'>Recibido Por:</label>
						<input disabled id='recibido_por' value='${data.recibido_por}' type='text'></p>
					</div>
					<div class='input-field col m4 s12'>
						<i class='prefix fas fa-arrow-right fa-3x'></i>
						<label for='tipo_remitente'>Tipo de Remitente:</label>
						<input disabled id='tipo_remitente' value='${tipo_remitente}' type='text'></p>
					</div>
					<div class='input-field col m4 s12'>
						<i class='prefix far fa-clock fa-3x'></i>
						<label for='prioridad_datos'>Prioridad:</label>
						<input disabled id='prioridad_datos' value='${data.prioridad}' type='text'></p>
					</div>
					<div class='input-field col m4 s12'>
						<i class='prefix far fa-clock fa-3x'></i>
						<label for='fecha_entrega-datos'>Fecha Entrega:</label>
						<input disabled id='fecha_entrega-datos' value='${fecha_entrega}' type='text'></p>
					</div>
					<div class='input-field col m4 s12'>
						<i class='prefix far fa-building fa-3x'></i>
						<label for='sucursal-datos'>Sucursal:</label>
						<input disabled id='sucursal-datos' value='${data.sucursal}' type='text'></p>
					</div>
					<div class='input-field col m12 s12'>
						<i class='prefix far fa-eye fa-3x'></i>
						<label for='observacion_datos'>Observacion:</label>
						<textarea disabled id='observacion_datos' class='materialize-textarea'>${data.observacion}</textarea>
					</div>
					<div class='input-field col m12 s12'>
						<i class='prefix fas fa-comments fa-3x'></i>
						<label for='comentario_datos'>Comentario:</label>
						<textarea disabled id='comentario_datos' class='materialize-textarea'>${data.comentario}</textarea>
					</div>`
				);

				$('#codigo-datos').text(data.codigo);

			},
			error: function(data) {
				var contenido = {
					'html': `<span>Error: ${data.mensaje} </span>`,
					'classes': 'rounded red text-white',
					'displayLength': 10000,
					'outDuration': 5000,
					'inDuration': 2000,
				}
				M.toast(contenido);

			}
		});
	});


	$("#check1").change(function HabilitarTerceros() {
		if (this.checked) {
			$('#obs').append(div_tercero);
		} else {
			$('#obs').empty();
		}
	});


	$('#guardar').click(function EntregarMensajeria() {
		var tercero = $('#tercero').val();
		$.ajax({
			type: "POST",
			url: "/entregar_mensajeria_ajax/",
			data: {
				'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val(),
				'id_mensajeria': id_mensajeria,
				'tercero': tercero,
				'estado': estado,
				'r_ext': r_ext,
			},

			success: function(data) {

				$(`#anc${id_mensajeria}`).children()
					.removeAttr('data-target value')
					.attr('class', data.boton.clase)
					.text(data.texto);

				$(`div[name=${id_mensajeria}]`)
					.removeClass('red accent-4')
					.addClass('green accent-4')
					.text(data.boton.texto);

				$('#cancelar').trigger('click');
				$('#check1').prop('checked', false);
				$('#check1').trigger('change');

				var contenido = {
					'html': data.mensaje,
					'classes': 'rounded green accent-4 text-white',
					'displayLength': 10000,
					'outDuration': 5000,
					'inDuration': 2000,
				}
				M.toast(contenido);

				id_mensajeria = '';
			},
			error: function(data) {
				var contenido = {
					'html': '<span>La mensajeria no pudo ser marcada como entregada.</span>',
					'classes': 'rounded red text-white',
					'displayLength': 10000,
					'outDuration': 5000,
					'inDuration': 2000,
				}
				M.toast(contenido);
			}
		});
	});


	function CambiarEstado(id, estado, r_ext) {
		$.ajax({
			type: "POST",
			url: "/cambiar_estado_ajax/",
			data: {
				'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val(),
				'id_mensajeria': id,
				'estado': estado,
				'r_ext': r_ext,
			},

			success: function(data) {
				$(`#anc${id}`).children()
					.attr('value', data.boton.valor)
					.attr('class', data.boton.clase)
					.text(data.boton.texto);
					if (data.boton.modal) {
						$(`#anc${id}`).children()
						.attr('data-target', data.boton.modal)
					}
				$(`div[name=${id}]`)
					.removeAttr('class')
					.addClass(data.clase)
					.text(data.estado);

				var contenido = {
					'html': data.mensaje,
					'classes': 'rounded green accent-4 text-white',
					'displayLength': 10000,
					'outDuration': 5000,
					'inDuration': 2000,
				}
				M.toast(contenido);
			},
			error: function(data) {
				var contenido = {
					'html': '<span>La mensajeria no pudo ser marcada como entregada.</span>',
					'classes': 'rounded red text-white',
					'displayLength': 10000,
					'outDuration': 5000,
					'inDuration': 2000,
				}
				M.toast(contenido);
			}
		});
	}


	$("body").on("click", "button.btn.control", function (event) {
		var valores = $(this).val();
		var id_mensajeria = valores.split('-')[0];
		var estado = valores.split('-')[1];
		var r_ext = $(this).attr('r_ext');
		if (id_mensajeria != '' & estado != '' & r_ext != ''){
			CambiarEstado(id_mensajeria, estado, r_ext);
		}
	});


	$("body").on("click", "button.entregar", function (event) {
		var valores = $(this).val();
		r_ext = $(this).attr('r_ext');
		id_mensajeria = valores.split('-')[0];
		estado = valores.split('-')[1];
		$('#codigo-firma').val(id_mensajeria);
		$('#id-h4').text('CODIGO:  ' + $(`td[id=cod${id_mensajeria}]`).text());
	});
});