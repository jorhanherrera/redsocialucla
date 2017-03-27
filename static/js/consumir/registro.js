function Registrar() {
	console.log("holaaa");
	if(localStorage.getItem('logeado')==1){
		window.location="http://localhost:8000/inicio";
	}
	else
	{
		var r_username = document.getElementById("registro_username").value;
		var r_pass1 = document.getElementById("registro_pass1").value;
		var r_pass2 = document.getElementById("registro_pass2").value;
		if ((r_username.length) == 0 || (r_pass1.length)==0 || (r_pass2.length)==0){
			alert("Especifique su nombre de usuario y contraseña");
		}
		else{
			if(r_pass1!=r_pass2){
				alert("La contraseña no coincide");
			}
			else{
				
				$.ajax({
					type: "POST",
					url : "http://localhost:8000/entities/users/",
					dataType : "json",
					data : {"username":r_username,"password1":r_pass1, "password2":r_pass2},
					success : function(data) {
		            	window.location="http://localhost:8000/index";
					},
					error : function(xhr, ajaxOptions, thrownError){
						alert(xhr.statusText);
					}
				});
			}
		}
	}
}

function Consultar() {
	if(localStorage.getItem('logeado')==1){
		window.location="http://localhost:8000/inicio";
	}
	else
	{
		var r_cedula = document.getElementById("registro_cedula").value;
		if ((r_cedula.length) == 0 ){
			alert("Campo cédula vacío");
		}
		else{
				
				$.ajax({
					type: "GET",
					url : "http://localhost:8000/entities/cumlaude"+r_cedula,
					dataType : "json",
					success : function(data) {
		            	window.location="http://localhost:8000/registro";
					},
					error : function(xhr, ajaxOptions, thrownError){
						//alert(xhr.status);
					}
				});
		}
	}
}
