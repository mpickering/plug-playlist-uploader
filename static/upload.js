function setProgress(done,total){
					var newWidth = (done/total)*100
					$('#progress').transition({
						width: newWidth
					})
					$('#textProgress').html(done +' / '+ total)
			}

			function upload(){
				var ids = $('#ids').val()
				var playlistName = $('#playlistName').val()
				var patt1=/^([\w-]{11})(,\s*[\w-]{11})*$/;
				if (patt1.test(ids)){
					ids=ids.split(',')
					var done = 0
					var total = ids.length
					$('#textProgress').html('0 / '+ total)
					$('#progressArea').slideDown()
					$.post('upload',{name: playlistName}, function(data){
						for (i in ids){
							$.post('track',{id:ids[i]}, function(data){
								done = done+1
								setProgress(done,total)
							})
						}
					$('#feedback').slideUp(function(){
						$('#message').html('<a href="' + data + '" target="_new" style="text-decoration:none"> Click here to go to your playlist </a>')
						$('#feedback').css('background-color','')
						$('#feedback').slideDown()
					})
				})
				}
				else{
					$('#feedback').slideUp(function(){
						$('#message').html('Invalid IDs')
						$('#feedback').css('background-color','#FF2424')
						$('#feedback').slideDown()
					})
				}


			}