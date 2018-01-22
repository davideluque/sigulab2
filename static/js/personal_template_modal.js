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

    $('#sel1').change(function (){
        if (($("#sel1 option:selected").val()=="Jubilado") || $("#sel1 option:selected").val()=="Retirado") {
            $("#fsalida").show();
        }
        else {
            $("#fsalida").hide();
        };
    });


    // next step
    $('.registration-form .btn-next').on('click', function () {
        var parent_fieldset = $(this).parents('fieldset');
        var next_step = true;

        parent_fieldset.find('input[type="text"],input[type="checkbox"],select[type="select"]').each(function () {
                        
            if (($(this).val() == "") && ($(this).attr('required'))) {
                if (($(this).attr('name')=="nombre_add") || ($(this).attr('name')=="nombre_edit")) {
                    $("#err_nombre").html("Este campo es obligatorio");
                    $("#err_nombre").show();
                }
                else if (($(this).attr('name')=="apellido_add") || ($(this).attr('name')=="apellido_edit")) {
                    $("#err_apellido").html("Este campo es obligatorio");
                    $("#err_apellido").show();
                }
                else if (($(this).attr('name')=="ci_add") || ($(this).attr('name')=="ci_edit")) {
                    $("#err_ci").html("Este campo es obligatorio");
                    $("#err_ci").show();
                }
                else if (($(this).attr('name')=="email_add") || ($(this).attr('name')=="email_edit")) {
                    $("#err_email").html("Este campo es obligatorio");
                    $("#err_email").show();
                }
                else if (($(this).attr('name')=="telefono_add") || ($(this).attr('name')=="telefono_edit")) {
                    $("#err_telefono").html("Este campo es obligatorio");
                    $("#err_telefono").show();
                }
                else if (($(this).attr('name')=="fecha_ingreso_add") || ($(this).attr('name')=="fecha_ingreso_edit")) {
                    $("#err_fecha_ingreso").html("Este campo es obligatorio");
                    $("#err_fecha_ingreso").show();
                }
                $(this).addClass('input-error');
                next_step = false;
            } else {
                if (($(this).attr('name')=="nombre_add") || ($(this).attr('name')=="nombre_edit")) {
                    if (!($(this).val().match(/^(([a-zA-Z ]+[\-\'\.]?)+[a-zA-Z ]+)+$/))) { // Todo lo que sean nombres
                        $("#err_nombre").html("Introduzca un nombre válido");
                        $("#err_nombre").show();
                        $(this).addClass('input-error');
                        next_step = false;
                    }
                    else {
                        $(this).removeClass('input-error');
                        $("#err_nombre").hide();
                    }
                }
                else if (($(this).attr('name')=="apellido_add") || ($(this).attr('name')=="apellido_edit")) {
                    if (!($(this).val().match(/^(([a-zA-Z ]+[\-\'\.]?)+[a-zA-Z ]+)+$/))) {
                        $("#err_apellido").html("Introduzca un apellido válido");
                        $("#err_apellido").show();
                        $(this).addClass('input-error');
                        next_step = false;
                    }
                    else {
                        $(this).removeClass('input-error');
                        $("#err_apellido").hide();
                    }
                }
                else if (($(this).attr('name')=="ci_add") || ($(this).attr('name')=="ci_edit")) {
                    if (!($(this).val().match(/[0-9]$/)) || $(this).val()>99999999) { // CI
                        $("#err_ci").html("Introduzca una cédula de identidad válida (Entre 1 y 99999999)");
                        $("#err_ci").show();
                        $(this).addClass('input-error');
                        next_step = false;
                    }
                    else {
                        $(this).removeClass('input-error');
                        $("#err_ci").hide();
                    }
                }
                else if (($(this).attr('name')=="email_add") || ($(this).attr('name')=="email_edit")) {
                    if (!($(this).val().match(/^\w+([\.-]?\ w+)*@\w+([\.-]?\ w+)*(\.\w{2,3})+$/))) { // Correo
                        $("#err_email").html("Introduzca un correo válido (Ej: usuario@domino.com)");
                        $("#err_email").show();
                        $(this).addClass('input-error');
                        next_step = false;
                    }
                    else {
                        $(this).removeClass('input-error');
                        $("#err_email").hide();
                    }
                }
                else if (($(this).attr('name')=="telefono_add") || ($(this).attr('name')=="telefono_edit")) {
                    if (!($(this).val().match(/[0-9]$/)) || $(this).val()>9999) { // Extension de 1 a 4 digitos
                        $("#err_telefono").html("La extensión debe tener entre 1 y 4 dígitos numéricos");
                        $("#err_telefono").show();
                        $(this).addClass('input-error');
                        next_step = false;
                    }
                    else {
                        $(this).removeClass('input-error');
                        $("#err_telefono").hide();
                    }
                }
                else {
                    $(this).removeClass('input-error');
                    $("#err_fecha_ingreso").hide();
                }
            }
            if (($("#sel1 option:selected").val()=="Jubilado") || $("#sel1 option:selected").val()=="Retirado") {
                if (($(this).val() == "") && ($(this).attr('name')=="fecha_salida_add")) {
                    $("#err_fecha_salida").html("Este campo es obligatorio");
                    $("#err_fecha_salida").show();
                    $(this).addClass('input-error');
                    next_step = false;
                };
            } else {
                $("#err_fecha_salida").hide();
                $(this).removeClass('input-error');
            };
        });

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

    // submit
    $('#submit').on('click', function (e) {
        var parent_fieldset = $(this).parents('fieldset');

        parent_fieldset.find('input[type="text"]').each(function () {
            if (($(this).val() == "") && ($(this).attr('required'))) {
                if (($(this).attr('name')=="cargo_add") || ($(this).attr('name')=="cargo_edit")) {
                    $("#err_cargo").html("Este campo es obligatorio");
                    $("#err_cargo").show();
                }
                $(this).addClass('input-error');
                e.preventDefault();
            } else {
                if (($(this).attr('name')=="cargo_add") || ($(this).attr('name')=="cargo_edit")) {
                    if (!($(this).val().match(/^(([a-zA-Z ]+[\-\'\.]?)+[a-zA-Z ]+)+$/))) { // Todo lo que sea nombres (Antes del submit)
                        $("#err_cargo").html("Introduzca un cargo válido");
                        $("#err_cargo").show();
                        $(this).addClass('input-error');
                        e.preventDefault();
                    }
                    else {
                        $("#err_cargo").hide();
                        $(this).removeClass('input-error');
                    }
                }
                else {
                    $(this).removeClass('input-error');
                }
            }
        });

    });

   
});
