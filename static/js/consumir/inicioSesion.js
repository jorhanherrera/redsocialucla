function SetAuth(tokn, usrname){
	localStorage.setItem('token', tokn);
	localStorage.setItem('username',usrname);
	localStorage.setItem('logeado', 1);
}

function IniciarSesion() {
	if(localStorage.getItem('logeado')==1){
		window.location="http://localhost:8000/inicio";
	}
	else
	{
		var usrname = document.getElementById("login_usuario").value;
		var pass = document.getElementById("login_password").value;
		if ((usrname.length) == 0 || (pass.length)==0){
			alert("Especifique su nombre de usuario y contraseña");
		}else{
			var sendInfo = {
				username: usrname,
				password: pass
			}
			$.ajax({
				type: "POST",
				url : "http://localhost:8000/rest-auth/login/",
				dataType : "json",
				data : {"username":usrname,"password":pass},
				success : function(data) {
	            	SetAuth(data.key, usrname);
	            	console.log(localStorage.getItem('username'));
	            	window.location="http://localhost:8000/inicio";
				},
				error : function(){
					alert("Datos incorrectos");
				}
			});
		}
	}
}

function CerrarSesion(){
	$.ajax({
			type: "POST",
			url : "http://localhost:8000/rest-auth/logout/",
			dataType : "json",
			data : {},
			success : function(data) {
            	window.location="http://localhost:8000/index";
            	localStorage.setItem('logeado', 0);
			},
	});
}