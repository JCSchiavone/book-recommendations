

$('#submit-btn').click(function(e){
	var book = $('#booksearch').val();
	
	data = {'title': book};
	
	$.ajax({
		type: 'POST',
		url: '/search_title',
		data: data,
		success: function(res) {
		},
		error: function(res) {
			console.log(res);
		}
	});
});
