function filter(type){

	var e = document.getElementById("fil_"+type);
	var opt = e.options[e.selectedIndex];
	var trs = document.querySelectorAll('#dummyID tr');
	for(i = 0; i < trs.length; ++i) {
	    idtr = trs[i].id.split("_");
	    if ( type == 'gremio' ){

	    	trs[i].style.display = 'None';
	    	if ( idtr[1] == opt.value ){trs[i].style.display = 'table-row';}

	    }else if ( type == 'dependencia' ){

	    	trs[i].style.display = 'None';
	    	if ( idtr[0] == opt.innerHTML ){trs[i].style.display = 'table-row';}

	    }

	}
	if (type=='gremio'){
		$("#botonreporte").attr("href","reporte?tipo="+type+"&filtro="+opt.value);
	}
	else {
		$("#botonreporte").attr("href","reporte?tipo="+type+"&filtro="+opt.innerHTML);
	}
}

$.fn.datepicker.defaults.format = "yyyy-mm-dd"
$.fn.datepicker.dates['en'] = {
    days: ["Domingo", "Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"],
    daysShort: ["Dom", "Lun", "Mar", "Mie", "Jue", "Vie", "Sab"],
    daysMin: ["Do", "Lu", "Ma", "Mi", "Ju", "Vi", "Sa"],
    months: ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Deciembre"],
    monthsShort: ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dec"],
    today: "Hoy",
    clear: "Limpiar",
    titleFormat: "MM yyyy", /* Leverages same syntax as 'format' */
    weekStart: 0
};


$(document).ready( function() {
    $('.datepicker').datepicker({
        language: 'en'
    })
    var d1=$( "#datepicker" ).datepicker();
    $( "#datepicker2" ).datepicker();
    var dateUsb = $( "#datepickerUsb" ).datepicker();
    $( "#datepickerUlab" ).datepicker();
    $( "#datepicker5" ).datepicker();

    // Funcion para reiniciar el modal de mostrar ficha cada vez que 
    // se selecciona una persona 
    $( ".empleado" ).on("click", function(e){
      $(".tab-edicion-principal").attr("class", "tab-edicion-principal nav-item active");
      $(".tab-edicion").attr("class", "tab-edicion nav-item");
      $(".pane-edicion-principal").attr("class", "pane-edicion-principal tab-pane active");
      $(".pane-edicion").attr("class", "pane-edicion tab-pane")
    })

    $('#ficha_edicion').on('show.bs.modal', function(e){
        var ci = $(e.relatedTarget).data('ci');
        var gremio = $(e.relatedTarget).data('gremio');
        var email = $(e.relatedTarget).data('email');
        var email_alt = $(e.relatedTarget).data('email_alt');
        var fecha_salida = $(e.relatedTarget).data('fecha_salida');
        var fecha_ingreso = $(e.relatedTarget).data('fecha_ingreso');
        var nombre = $(e.relatedTarget).data('nombre');
        var apellido = $(e.relatedTarget).data('apellido');
        var cargo = $(e.relatedTarget).data('cargo');
        var dependencia = $(e.relatedTarget).data('dep-name');
        var estatus = $(e.relatedTarget).data('estatus');
        var telefono = $(e.relatedTarget).data('telefono');
        var pagina_web = $(e.relatedTarget).data('pagina_web');
        var rol = $(e.relatedTarget).data('rol');
        var extension_USB = $(e.relatedTarget).data('extension_usb');
        var extension_interna = $(e.relatedTarget).data('extension_interna');

        var unidad_jerarquica_superior = $(e.relatedTarget).data('unidad_jerarquica_superior');
        var ubicacion = $(e.relatedTarget).data('ubicacion');
        var celular = $(e.relatedTarget).data('celular');
        var persona_contacto = $(e.relatedTarget).data('persona_contacto');
        var contacto_emergencia = $(e.relatedTarget).data('contacto_emergencia');
        var direccion = $(e.relatedTarget).data('direccion');
        var categoria = $(e.relatedTarget).data('categoria');
        var fecha_ingreso_ulab = $(e.relatedTarget).data('fecha_ingreso_ulab');
        var fecha_ingreso_usb = $(e.relatedTarget).data('fecha_ingreso_usb');
        var fecha_ingreso_admin_publica = $(e.relatedTarget).data('fecha_ingreso_admin_publica');
        var condicion = $(e.relatedTarget).data('condicion');
        var nombre_completo= nombre +" "+apellido;

        f = [ci, gremio, email, fecha_salida, fecha_ingreso, nombre, cargo, estatus, telefono, pagina_web, unidad_jerarquica_superior,
              ubicacion, celular, contacto_emergencia, direccion, categoria,fecha_ingreso_ulab, fecha_ingreso_usb, fecha_ingreso_admin_publica,
               condicion,rol, extension_USB, extension_interna, email_alt, persona_contacto];
        if (categoria === 'Fijo') {
          $('#field_fecha_ingreso').parent().addClass('hide')
          $('#field_fecha_salida').parent().addClass('hide')
        } else {
          $('#field_fecha_ingreso').parent().removeClass('hide')
          $('#field_fecha_salida').parent().removeClass('hide')
        }
        $("#field_ci").html(ci);
        $("#field_gremio").html(gremio);
        $("#field_dependencia").html(dependencia);
        $("#field_email").html(email);
        $("#field_email_alt").html(email_alt);
        $("#field_fecha_salida").html(fecha_salida);
        $("#field_fecha_ingreso").html(fecha_ingreso);
        $("#field_nombre").html(nombre);
        $("#field_apellido").html(apellido);
        $("#field_cargo").html(cargo);
        $("#field_estatus").html(estatus);
        $("#field_telefono").html(telefono);
        $("#field_pagina_web").html(pagina_web);
        $("#field_rol").html(rol);
        $("#field_extension_interna").html(extension_interna);
        $("#field_extension_USB").html(extension_USB);

        $("#field_unidad_jerarquica_superior").html(unidad_jerarquica_superior);
        $("#field_ubicacion").html(ubicacion);
        $("#field_celular").html(celular);
        $("#field_persona_contacto").html(persona_contacto);
        $("#field_contacto_emergencia").html(contacto_emergencia);
        $("#field_direccion").html(direccion);
        $("#field_categoria").html(categoria);
        $("#field_fecha_ingreso_ulab").html(fecha_ingreso_ulab);
        $("#field_fecha_ingreso_usb").html(fecha_ingreso_usb);
        $("#field_fecha_ingreso_admin_publica").html(fecha_ingreso_admin_publica);
        $("#field_condicion").html(condicion);
        $("#field_nombre_completo").html(nombre_completo)

        var superusuario = 'sigulabusb@gmail.com';
        var gestor = 'asis-ulab@usb.ve';
        var director = 'ulab@usb.ve';
        const currentlyLogged = $('[name=CORREO_LOGIN]').val()
        
        if( currentlyLogged !== email && currentlyLogged != superusuario && currentlyLogged != gestor){
             $('#editar').prop('disabled',true);
        }else{
            $('#editar').removeAttr('disabled');
        }
        
        if( currentlyLogged !== email && currentlyLogged != superusuario && currentlyLogged != gestor && 
            currentlyLogged != director){
             $('#tab_datos_personales').hide();
        }else{
            $('#tab_datos_personales').show();
            console.log("aca")
        }
        
        
        //$('#editar').prop('disabled',( currentlyLogged !== email && currentlyLogged && superusuario && currentlyLogged != gestor))

        $('#eliminar').on('click',function(f){
          var answer=confirm('¿Seguro que desea eliminar esta persona?');
          if(answer){
            alert('Persona eliminada!');
            this.value = $(e.relatedTarget).data('ci');
          }
          else{
            f.preventDefault();
          }
            

        });


        fields = [ci,gremio,email,fecha_salida,fecha_ingreso,nombre,cargo,estatus,telefono,pagina_web, unidad_jerarquica_superior,
              ubicacion, celular, contacto_emergencia, direccion, categoria,fecha_ingreso_ulab, fecha_ingreso_usb, fecha_ingreso_admin_publica,
               condicion, rol, extension_USB, extension_interna, email_alt, persona_contacto];
        //$("#field_ci").html(item);
        //$(e.currentTarget).find('input[name="usbid"]').val(usbid);
    });

} );
