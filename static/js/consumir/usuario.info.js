function UsuarioInfo() {
	var self = this;
	self.username= ko.observable();
	self.foto = ko.observable();
	self.current_page = 2;
	
	//self.current_user = 'rvalera';

	
	self.load = function() {
		self.loadTimeline();
	}
	
	self.loadTimeline = function() {

		$.ajax({
			type: "GET",
			contentType: "application/json; charset=utf-8",
			dataType : "json",
			url : 'http://localhost:8000/entities/users/'+localStorage.getItem('username'),
			
			success : function(data) {
              
            	console.log(data);
                  
			},
			error : function(){
				window.location="http://localhost:8000/index";
			}
		});

	}
	
	
	
}

var usuarioInfo = new UsuarioInfo();
usuarioInfo.load();
ko.applyBindings(usuarioInfo);