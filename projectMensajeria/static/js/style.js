$(document).ready(function() {

	$("body")
		.on('click', '#modalMensajeriaExterna a[role=menuitem]', function(){
			$('label.error').css("display", "none");
		})
		.on('blur', '#modalMensajeriaExterna input', function() {
			$('label.error').css("display", "none");
		});

	$('.modal').modal({
		dismissible: false,
		onOpenEnd: function() {

			let fecha = new Date(Date.now());
			let hora = 0;
			let minutos = 0;

			if (fecha.getMinutes() < 10) {
				minutos = (`0${fecha.getMinutes()}`);
			}
			else{
				minutos = fecha.getMinutes();
			}

			if (fecha.getHours() < 10) {
				hora = (`0${fecha.getHours()}`);
			}
			else{
				hora = fecha.getHours();
			}

			let dia = `0${fecha.getDate()}`.slice(-2);
			let mes = `0${(fecha.getMonth() + 1)}`.slice(-2);
			// let mes = `0${(fecha.getMonth() + 1).slice(-2)}`;
			let hoy = `${fecha.getFullYear()}-${mes}-${dia}`;
			$('#fecha_envio_depto').val(hoy)
			$('#fechaRecibido').val(hoy)
			$('#horaRecibido').val(`${hora}:${minutos}`)
			$('#hora_envio_depto').val(`${hora}:${minutos}`)
			$('#hora_salida').val(`${hora}:${minutos}`)
			$('#hora_entrada').val(`${hora}:${minutos}`)
		},
	});

	$('#prioridad').formSelect();

	$('.dropdown-trigger').dropdown();

	$('.a_boton').click(function () {
		let codigo = $(this).attr('value');
		$('#codigo').val(codigo);

	})

	$('.tooltipped').tooltip();

	$('#modal_video.modal').modal({
		onOpenEnd: function () {
			$('#video_ayuda')[0].play();
		},
		onCloseEnd: function () {
			$('#video_ayuda')[0].pause();
		}
	});
});