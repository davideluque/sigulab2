function testcheck(e)
{
    if (jQuery("#checkbox1").prop("checked") || 
        jQuery("#checkbox2").prop("checked") || 
        jQuery("#checkbox3").prop("checked") || 
        jQuery("#checkbox4").prop("checked")){
        return true;
    }     
    else{
        return false;
    }
}


$(document).ready(function () {
    $('.registration-form fieldset:first-child').fadeIn('slow');

    $('.registration-form input[type="text"]').on('focus', function () {
        $(this).removeClass('input-error');
    });

    $("#checkbox1").click(function() {
        jQuery("#funcion").removeClass('input-error');
    });

    $("#checkbox2").click(function() {
        jQuery("#funcion").removeClass('input-error');
    });

    $("#checkbox3").click(function() {
        jQuery("#funcion").removeClass('input-error');
    });

    $("#checkbox4").click(function() {
        jQuery("#funcion").removeClass('input-error');
    });

    $('.registration-form select[type="select"]').on('focus', function () {
        $(this).removeClass('input-error');
    });
    // *!* ELIMINAR?
    $('.registration-form textarea[name="propositoDescripcion"]').on('focus', function () {
        $(this).removeClass('input-error');
    });
    // *!* ELIMINAR?
    $('.registration-form input[name="itemServicio"]').on('focus', function () {
        $(this).removeClass('input-error');
    });

    // *!* ELIMINAR textarea[name="propositoDescripcion"], input[name="itemServicio"] ?
    // next step

        
            // next step
    $('.registration-form .btn-next').on('click', function () {
        var parent_fieldset = $(this).parents('fieldset');
        var next_step = true;

        parent_fieldset.find('input[type="text"],input[type="checkbox"],select[type="select"]').each(function () {
                        
            if (($(this).val() == "") && ($(this).attr('required'))) {
                if (($(this).attr('name')=="nombre") || ($(this).attr('name')=="nombre_edit")) {
                    //$("#err_nombre").html("Este campo es obligatorio");
                    //$("#err_nombre").show();

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
            }else {
                if (($(this).attr('name')=="no_bien")) {
                    if (!($(this).val().match(/^[0-9]{6}$/))) {
                        $("#err_no_bien").html("Formato Inválido. son 6 digitos");
                        $("#err_no_bien").show();
                        $(this).addClass('input-error');
                        next_step = false;
                    }
                    else {
                        $(this).removeClass('input-error');
                        $("#err_no_bien").hide();
                    }
                }
                else if (($(this).attr('name')=="no_placa")) {
                    if (!($(this).val().match(/^[0-9]{5}$/)) && $(this).val() != "") {
                        $("#err_placa").html("Formato Inválido. son 5 digitos");
                        $("#err_placa").show();
                        $(this).addClass('input-error');
                        next_step = false;
                    }
                    else {
                        $(this).removeClass('input-error');
                        $("#err_placa").hide();
                    }
                }
                else {
                    $(this).removeClass('input-error');
                    $("#err_fecha_ingreso").hide();
                }
            }
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
        
           
           parent_fieldset.find('input[type="text"],input[type="checkbox"],select[type="select"], textarea[name="propositoDescripcion"], input[name="itemServicio"]').each(function () {         

            if ($(this).val() == "") {
                $(this).addClass('input-error');
                next_step = false;
            }
            else {
                $(this).removeClass('input-error');
            }

        });

        // if (!testcheck()){
        //     jQuery("#funcion").addClass('input-error');
        //     next_step = false;
        // }
        // else{
        //      jQuery("#funcion").removeClass('input-error');
        // }

        if (next_step) {
            parent_fieldset.fadeOut(400, function () {
                $(this).next().fadeIn();
            });
        }


    // previous step
    $('.registration-form .btn-previous').on('click', function () {
        $(this).parents('fieldset').fadeOut(400, function () {
            $(this).prev().fadeIn();
        });
    });

    // submit
    $('#submit').on('click', function (e) {
        var parent_fieldset = $(this).parents('fieldset');

        parent_fieldset.find('input[name="itemServicio"]').each(function () {
            if ($(this).val() == "") {
                jQuery("#item_ensayar").addClass('input-error');
                e.preventDefault();
                return false;
            } else {
                $(this).removeClass('input-error');
            }
        });

    });

   
});