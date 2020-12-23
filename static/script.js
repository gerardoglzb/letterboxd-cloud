$(document).ready(function() {
	$('form').on('submit', function(e) {
		$.ajax({
			data: {
				username: $('#username-input').val()
			},
			type: 'POST',
			url: '/get-cloud'
		})
		.done(function(data, status, request) {
			if (data.error) {
				alert(data.error);
			} else {
				var status_url = request.getResponseHeader('Location');
				check_job_status(status_url);
			}
		});
		e.preventDefault();
	});
});

function check_job_status(status_url) {
	console.log("checking job status");
	$.getJSON(status_url, function(data) {
    switch (data.status) {
		case "unknown":
			alert("Unknown job");
			break;
		case "finished":
			console.log("image done");
			$("#cloud-img").attr("src", 'data:;base64,' + data['image']);
			$("#cloud-img").removeAttr('hidden');
          	break;
		case "failed":
			alert("Job failed");
			break;
		case "invalid":
			alert("Invalid user. Make sure it exists and has reviews.");
			break;
		default:
		setTimeout(function() {
			check_job_status(status_url);
		}, 1000);
    }
  });
}
