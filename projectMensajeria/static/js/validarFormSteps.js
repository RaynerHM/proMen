$(document).ready(function () {

	var form = $("#id_form")

	form.validate();

	form.children(".div").steps({
		headerTag: "h5",
		bodyTag: "section",
		transitionEffect: "slideLeft",

		onStepChanging: function (event, currentIndex, newIndex) {
			form.validate().settings.ignore = ":disabled,:hidden";
			$('#enviarExterna').remove();
			return form.valid();
		},
		onFinishing: function (event, currentIndex) {
			form.validate().settings.ignore = ":disabled";
			$('#enviarExterna').remove();

			return form.valid();
		},
		onFinished: function (event, currentIndex) {
			$('#bCancelarExterna').after('<input id="enviarExterna" type="submit" value="Guardar" class=" btn">')
		}
	});
});