$(function() {
	alert("hi");
	var type;
	var url;
	var ip;
	$('.generate').bind('click', function() {
		type = this.id;
		url = "/make_graph/" + type + "/1/5";

		$.ajax({
			url: url,
			type: "get",
			success: function(response) {
				$("#graph-" + type).html(response);
			},
			error: function(xhr) {
				alert("error");
			}
		});
	});

	    
	$('.get_data').bind('click', function() {
		type = this.id;
		ip = '{{ ip }}';
		url = "/getJson/" + ip + "/" + type + "/1;
		$.ajax({
			url: url,
			type: "get",
			id: this.id,
			success: function(response) {
				$("#data-" + type).html(response);
			},
			error: function(xhr) {
				alert("error");
			}
		});
	});
});