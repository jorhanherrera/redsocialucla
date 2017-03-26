function HomeVM() {
	var self = this;
	self.posts= ko.observableArray();
	self.comentarios= ko.observableArray();
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
			url : 'http://localhost:8000/entities/private-timeline/',
			
			success : function(data) {
              
              data.results.forEach(function (element) {
                //element.comentarios_count = element.comentarios_set.length
                  	console.log(element.contenido);
                  	console.log(element);
                  	//element.comentarios_count = element.comentarios.length;
                  	ko_element = ko.mapping.fromJS(element);
					self.posts.push(ko_element);
              });
			},
			error : function(){
				window.location="http://localhost:8000/index";
			}
		});

	}
	
	removePost = function(data) {
		
		alertify.confirm('Confirm Dialog',"Do you want delete this item?",
			function(){
				$.ajax({
					type:"DELETE",
					url : "entities/timeline/"+data.id()+"/",
					dataType : "json",
				 	success : function(data) {
						alertify.success('Data deleted sucesfully!');
				 		self.posts([]);		 		
				 		loadTimeline();		 		
					},
			 	});
				
			},
			function(){
		});
		
	}

	saveNewPost = function() {

		$.ajax({
			type:"POST",
			url : "entities/timeline/"  + "?&authenticity_token= xxxxxxxxx",
			dataType : "json",
			data : JSON.stringify({"content" : self.new_post(), "owner" : {"username" : self.current_user} }),
		 	success : function(data) {
		 		self.posts([]);		 		
		 		loadTimeline(); 		
			},
	 	});		
		
	}
	
}

var homeVM = new HomeVM();
homeVM.load();
ko.applyBindings(homeVM);