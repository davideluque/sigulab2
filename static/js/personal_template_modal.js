// Funcion para tranformar el attributo data-valido de los input para ver 
// si un input es valido 
function data_validoToBoolean(selector){
    if ($(selector).attr("data-valido") === "true"){
        return true;
    }
    else if ($(selector).attr("data-valido") === "false") {
        return false;
    }
}

// Funcion para mostrar errores 
function mostrarError(selector){
    if (selector === '[name="telefono_add"]'){
        if (!($(selector).val().match(/^\d+$/gm)) || $(this).val() < 999999999){
            $(selector).attr("data-content", "El teléfono tiene el formato incorrecto");
            $(selector).popover('hide');
            $(selector).popover('show');
            $(selector).addClass('input-error');
        }
    }
}

// Funcion que valida los campos cuando el usuario pasa a llenar otro input 
function validacionTiempoReal(){
    
    // Manejo de error del telefono 
    $('[name="telefono_add"]').blur(function (){
        if ($(this).val() !== ''){
            if (!($(this).val().match(/^\d+$/gm)) || $(this).val() < 999999999){
                $(this).attr("data-content", "El teléfono tiene el formato incorrecto");
                console.log($(this).popover('show'));
                $(this).addClass('input-error');
                $(this).attr("data-valido", "false");
            }
            else {
                $(this).removeClass('input-error');
                $(this).attr("data-valido", "true");
            }    
        }
    })     

    // Manejo del error de email alternativo
    $('[name="email_alt_add"]').blur(function (){
        if ($(this).val() !== ''){
            if (!($(this).val().match(/^(([^<>()\[\]\.,;:\s@\"]+(\.[^<>()\[\]\.,;:\s@\"]+)*)|(\".+\"))@(([^<>()[\]\.,;:\s@\"]+\.)+[^<>()[\]\.,;:\s@\"]{2,})$/)) || $(this).val() < 999999999){
                $(this).attr("data-content", "El correo no tiene el formato correcto");
                console.log($(this).popover('show'));
                $(this).addClass('input-error');
                $(this).attr("data-valido", "false");
            }
            else {
                $(this).removeClass('input-error');
                $(this).attr("data-valido", "true");
            }    
        }
    }) 

    // Manejo de error del numero de celular 
    $('[name="celular_add"]').blur(function (){
        pasoValidacion = true;
        if ($(this).val() !== ''){
            if (!($(this).val().match(/^\d+$/gm)) || $(this).val()<99999999) { // Extension de 1 a 4 digitos
                $(this).attr('data-content', 'El número de celular tiene el formato incorrecto');
                $(this).popover('show');
                $(this).addClass('input-error');
                $(this).attr("data-valido", "false");
            }
            else {
                $(this).removeClass('input-error');
                $(this).attr("data-valido", "true");
            }
        }
    });

    // Manejo de error del campo de contacto de emergencia 
    $('[name="contacto_emergencia_add"]').blur(function (){
        if ($(this).val() !== ''){
            pasoValidacion = true;
            if (!($(this).val().match(/[0-9]$/)) || $(this).val()<9999) { // Extension de 1 a 4 digitos
                $(this).attr("data-content", 'El contacto de emergencia debe tener solo números');
                $(this).popover('show');
                $(this).addClass('input-error');
                pasoValidacion = false;
            }
            else {
                $(this).removeClass('input-error');
            }
        }
        return pasoValidacion;
    })

    // Manejo de error del campo de pagina de web 
    $('[name="pagina_web_add"]').blur(function (){
        if ($(this).val() !== ''){
            pasoValidacion = true;
            if (!($(this).val().match(/^((https?|ftp|smtp):\/\/)?(www.)?[a-z0-9]+\.[a-z]+(\/[a-zA-Z0-9#]+\/?)*$/))) { // Extension de 1 a 4 digitos
                $(this).attr('data-content', "Formato incorrecto de pagina web");
                $(this).popover('show');
                $(this).addClass('input-error');
                $(this).attr("data-valido", "false");
            }
            else {
                $(this).removeClass('input-error');
                $(this).attr("data-valido", "true");
            }
        }
        return pasoValidacion;
    })
    
}


$(document).ready(function () {
    $('.registration-form fieldset:first-child').fadeIn('slow');

    $('.registration-form input[type="text"]').on('focus', function () {
        $(this).removeClass('input-error');
    });

    $('.registration-form input[type="checkbox"]').on('focus', function () {
        $(this).removeClass('input-error');
    });

    $('.registration-form select[type="select"]').on('focus', function () {
        $(this).removeClass('input-error');
    });

    $('#sel2').change(function (){
        if ($("#sel2 option:selected").val()=="Fijo") {
            $("#fsalida").hide();
        }
        else {
            $("#fsalida").show();
        };
    });

    //-------------------------------- Primera parte del form agregar -----------------------------------------//

    validacionTiempoReal();

    // next step
    $('.registration-form .btn-next').on('click', function () {
        var parent_fieldset = $(this).parents('fieldset');
        var next_step = true;
        if (parent_fieldset.attr('id') === 'p1') {
            $(` [name="email_alt_add"],
                [name="telefono_add"],
                [name="celular_add"],
                [name="contacto_emergencia_add"],
                [name="direccion_add"],
                [name="pagina_web_add"],
                [name="operador_add"]`).filter(function () {
                    $(this).next().first().hide()
                    $(this).removeClass('input-error')
                    if (data_validoToBoolean(this) !== undefined && data_validoToBoolean(this) === false){
                        next_step = data_validoToBoolean(this);
                        mostrarError(this);
                    }
                    if ($(this).attr("name") === "operador_add" && $(this).val() === null){
                        $(this).next().first().show()
                        $(this).addClass('input-error')
                        $(this).attr("data-content", "Este campo es requerido");
                        $(this).popover('show');
                        next_step = false;
                    }
                    return $(this).val() === ''
                }).each(function(idx) {
                    // $(this).next().first().html('Por favor, llene el campo')
                    if ($(this).attr("name") !== "pagina_web_add"){
                        $(this).next().first().show()
                        $(this).addClass('input-error')
                        $(this).attr("data-content", "Este campo es requerido");
                        $(this).popover('show');
                        next_step = false 
                    }
                })
        } else if (parent_fieldset.attr('id') === 'p2') {
            // dropdowns
            $(`[name="estatus_add"],
                [name="categoria_add"],
                [name="condicion_add"]`).filter(function () {
                    $(this).next().first().hide()
                    $(this).removeClass('input-error')
                    return $(this).val() === '' || $(this).val() === null
                }).each(function(idx) {
                    // $(this).next().first().html('Por favor, escoja una opción')
                    // $(this).next().first().show()
                    $(this).addClass('input-error')
                    if ($(this).val() === null){
                        $(this).attr("data-content", "Seleccione una opción");
                        $(this).popover('show');
                    }
                    next_step = false
                })

            // date inputs
            if ($('[name="categoria_add"]').val() !== 'Fijo'){
                $(`[name="fecha_ingreso_usb_add"],
                [name="fecha_ingreso_ulab_add"],
                [name="fecha_ingreso_admin_publica_add"],
                [name="fecha_ingreso_add"],
                [name="fecha_salida_add"]`).filter(function () {
                    return $(this).val() === '' || $(this).val() === null
                }).each(function(idx) {
                    $(this).addClass('input-error')
                    if ($(this).val() === ''){
                        $(this).popover('show');
                    }
                    next_step = false
                })    
            }
            else{
                $(`[name="fecha_ingreso_usb_add"],
                [name="fecha_ingreso_ulab_add"],
                [name="fecha_ingreso_admin_publica_add"]
                `).filter(function () {
                    return $(this).val() === '' || $(this).val() === null
                }).each(function(idx) {
                    $(this).addClass('input-error')
                    if ($(this).val() === ''){
                        $(this).popover('show');
                    }
                    next_step = false
                })
    
            }
            

            // Aqui se maneja el caso donde el trabajador tiene la condicion de fijo 
            console.log($('[name="categoria_add"]').val());
            if ($('[name="categoria_add"]').val() === 'Fijo'){
                $(`[name="fecha_ingreso_add"], [name="fecha_egreso_add"]`).removeAttr("required");
            }
        }

        if (next_step) {
            parent_fieldset.fadeOut(400, function () {
                $(this).next().fadeIn();
            });
        }

    });

    // previous step
    $('.registration-form .btn-previous').on('click', function () {
        $(this).parents('fieldset').fadeOut(400, function () {
            $(this).prev().fadeIn();
        });
    });


    // Desaparecer popover 
    $(`[name="apellido_add"],
        [name="ci_add"],
        [name="email_add"],
        [name="telefono_add"],
        [name="celular_add"],
        [name="contacto_emergencia_add"],
        [name="direccion_add"],
        [name="pagina_web_add"],
        [name="estatus_add"],
        [name="categoria_add"],
        [name="condicion_add"],
        [name="fecha_ingreso_usb_add"],
        [name="fecha_ingreso_ulab_add"],
        [name="fecha_ingreso_admin_publica_add"],
        [name="fecha_ingreso_add"],
        [name="fecha_salida_add"],
        [name="operador_add]`).on('focus', function(e){
        $(this).popover('hide');
        $(this).removeClass('input-error');
    })
    
    // submit
    $('#submit').on('click', function (e) {
        var parent_fieldset = $(this).parents('fieldset');

       

        parent_fieldset.find('input[type="text"]').each(function () {
            // if (($(this).val() == "") && ($(this).attr('required'))) {
            //     if (($(this).attr('name')=="cargo_add") || ($(this).attr('name')=="cargo_edit")) {
            //         $("#err_cargo").html("Este campo es obligatorio");
            //         $("#err_cargo").show();
            //     }
            //     $(this).addClass('input-error');
            //     e.preventDefault();
            // } else {
            //     if (($(this).attr('name')=="cargo_add") || ($(this).attr('name')=="cargo_edit")) {
            //         if (!($(this).val().match(/^(([a-zA-Z ]+[\-\'\.]?)+[a-zA-Z ]+)+$/))) { // Todo lo que sea nombres (Antes del submit)
            //             $("#err_cargo").html("Introduzca un cargo válido");
            //             $("#err_cargo").show();
            //             $(this).addClass('input-error');
            //             e.preventDefault();
            //         }
            //         else {
            //             $("#err_cargo").hide();
            //             $(this).removeClass('input-error');
            //         }
            //     }
            //     else {
            //         $(this).removeClass('input-error');
            //     }
            // }
        });

    });
    
    


   
});
