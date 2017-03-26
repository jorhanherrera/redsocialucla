function TimelinePublico() {
	var self = this;
	self.posts= ko.observableArray();
	self.comentarios= ko.observableArray();
	self.username = ko.observable();
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
			url : 'http://localhost:8000/entities/public-timeline/',
			
			success : function(data) {
              
              data.results.forEach(function (element) {
                  	
                  	ko_element = ko.mapping.fromJS(element);
					self.posts.push(ko_element);
                  
              });
			},
			error : function(){
				window.location="http://localhost:8000/index";
			}
		});

		$.ajax({
			type: "GET",
			contentType: "application/json; charset=utf-8",
			dataType : "json",
			url : 'http://localhost:8000/entities/users/'+localStorage.getItem('username'),
			
			success : function(data) {
              
            	console.log(data);
            	self.username(data.username);
            	self.foto(data.foto);
                  
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
			url : "entities/timeline/",
			dataType : "json",
			data : JSON.stringify({"content" : self.new_post(), "owner" : {"username" : self.current_user} }),
		 	success : function(data) {
		 		self.posts([]);		 		
		 		loadTimeline(); 		
			},
	 	});		
		
	}
	
}

var timelinePublico = new TimelinePublico();
timelinePublico.load();
ko.applyBindings(timelinePublico);