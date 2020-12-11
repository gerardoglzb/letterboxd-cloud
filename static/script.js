console.log("working!");

$(document).ready(function() {
	$('form').on('submit', function(e) {
		console.log("pressed");
		$.ajax({
			data: {
				username: $('#username-input').val()
			},
			type: 'POST',
			url: '/get-cloud'
		})
		.done(function(data) {
			if (data.error) {
				console.log(data.error);
			} else {
				console.log("success!");
				$("#cloud-img").attr("src", 'data:;base64,' + data['image']);
				$("#cloud-img").removeAttr('hidden');
			}
		});
		e.preventDefault();
	});
});