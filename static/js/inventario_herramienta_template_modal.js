function testcheck()
{
    if (jQuery("#tipo_uso1").prop("checked") || 
        jQuery("#tipo_uso2").prop("checked") || 
        jQuery("#tipo_uso3").prop("checked") || 
        jQuery("#tipo_uso4").prop("checked")){
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


                $(this).addClass('input-error');
                next_step = false;
            }else {
                if (($(this).attr('name')=="num_her")) {
                    console.log("aqui");
                    if ($(this).val()!=""){    
                        if (!($(this).val().match(/^[0-9]{6}$/) ) || $(this).val() === "000000" ) {
                            $("#err_num_her").html("Formato Inválido. Ingrese 6 dígitos");
                            $("#err_num_her").show();
                            $(this).addClass('input-error');
                            next_step = false;
                        }
                        else {
                            $(this).removeClass('input-error');
                            $("#err_num_her").hide();
                        }
                    }else {
                        $(this).removeClass('input-error');
                        $("#err_num_her").hide();
                    }
                }
                else if (($(this).attr('name')=="numpiezasher")) {
                    console.log("ayuda2");
                    if (!($(this).val().match(/^[0-9]{1,3}$/)) && $(this).val() != "") {
                        $("#err_numpiezasher").html("Formato Inválido. Ingrese de 1 a 3 dígitos");
                        $("#err_numpiezasher").show();
                        $(this).addClass('input-error');
                        next_step = false;
                    }
                    else {
                        $(this).removeClass('input-error');
                        $("#err_numpiezasher").hide();
                    }
                }
                else if (($(this).attr('name')=="ancho")) {
                    console.log( $(this).val() );
                    console.log("entro");
                    if ( !($(this).val().match(/^[0-9]+$/) || ($(this).val().match(/^[0-9]+\.[0-9]+$/) )) && $(this).val() != "") {
                        $("#errAnchoHer").html("Ingrese solo números decimales con punto: 2.5");
                        $("#errAnchoHer").show();
                        //$(this).addClass('input-error');
                        next_step = false;
                    }
                    else {
                        //$(this).removeClass('input-error');
                        $("#err_anchoHer").hide();
                    }
                }
                else if (($(this).attr('name')=="largo_her")) {
                    if ( !($(this).val().match(/^[0-9]+$/) || ($(this).val().match(/^[0-9]+\.[0-9]+$/) )) && $(this).val() != "") {
                        $("#err_largo_her").html("Ingrese números decimales con punto: 2.5");
                        $("#err_largo_her").show();
                        $(this).addClass('input-error');
                        next_step = false;
                    }
                    else {
                        $(this).removeClass('input-error');
                        $("#err_largo_her").hide();
                    }
                }else if (($(this).attr('name')=="alto_her")) {
                    if ( !($(this).val().match(/^[0-9]+$/) || ($(this).val().match(/^[0-9]+\.[0-9]+$/) )) && $(this).val() != "") {
                        $("#err_alto_her").html("Ingrese solo números decimales con punto: 2.5");
                        $("#err_alto_her").show();
                        $(this).addClass('input-error');
                        next_step = false;
                    }
                    else {
                        $(this).removeClass('input-error');
                        $("#err_alto_her").hide();
                    }
                }else if (($(this).attr('name')=="diametro_her")) {
                    if ( !($(this).val().match(/^[0-9]+$/) || ($(this).val().match(/^[0-9]+\.[0-9]+$/) )) && $(this).val() != "") {
                        $("#err_diametro_her").html("Ingrese solo números decimales con punto: 2.5");
                        $("#err_diametro_her").show();
                        $(this).addClass('input-error');
                        next_step = false;
                    }
                    else {
                        $(this).removeClass('input-error');
                        $("#err_diametro_her").hide();
                    }
                }
                else if( $(this).attr('name')== 'tipo_uso' && !testcheck())  {
                    $("#err_tipo_uso").html("Seleccione al menos una opción");
                    $("#err_tipo_uso").show();
                    $(this).addClass('input-error');
                     next_step = false;
                }
                else {
                    $(this).removeClass('input-error');
                    $("#err_fecha_ingreso").hide();
                }
            }
        });

        //if (!testcheck() && next_step){
        //    $("#err_tipo_uso").html("Seleccione al menos una opción");
        //    $("#err_ancho").show();
        //     next_step = false;
        // }
        // else{
        //    $("#err_cargo").hide();
        // }
        if (testcheck()){
            $("#err_tipo_uso").hide();
        }

        const $this = $('[name="ancho"]');
        console.log( $(this).val() );
        console.log("entro");
        if ( !($this.val().match(/^[0-9]+$/) || ($this.val().match(/^[0-9]+\.[0-9]+$/) )) && $this.val() != "") {
            $("#errAnchoHer").html("Ingrese solo números decimales con punto: 2.5");
            $("#errAnchoHer").show();
            //$(this).addClass('input-error');
            next_step = false;
        }
        else {
            //$(this).removeClass('input-error');
            $("#err_anchoHer").hide();
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
        
            // submit
            $('#submit').on('click', function (e) {
                var parent_fieldset = $(this).parents('fieldset');
                var next_step = true;

        
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
                        }else if (($(this).attr('name')=="ancho")) {
                            console.log( $(this).val() );
                            console.log("entro");
                            if ( !($(this).val().match(/^[0-9]+$/) || ($(this).val().match(/^[0-9]+\.[0-9]+$/) )) && $(this).val() != "") {
                                console.log("No cumple con")
                                $("#errancho").html("Ingrese solo números decimales con punto: 2.5");
                                $("#errancho").show();
                                $(this).addClass('input-error');
                                next_step = false;
                            }
                            else {
                                $(this).removeClass('input-error');
                                $("#err_ancho").hide();
                            }
                        }
                        else if (($(this).attr('name')=="largo_her")) {
                            if ( !($(this).val().match(/^[0-9]+$/) || ($(this).val().match(/^[0-9]+\.[0-9]+$/) )) && $(this).val() != "") {
                                $("#err_largo_her").html("Ingrese números decimales con punto: 2.5");
                                $("#err_largo_her").show();
                                $(this).addClass('input-error');
                                next_step = false;
                            }
                            else {
                                $(this).removeClass('input-error');
                                $("#err_largo_her").hide();
                            }
                        }else if (($(this).attr('name')=="alto_her")) {
                            if ( !($(this).val().match(/^[0-9]+$/) || ($(this).val().match(/^[0-9]+\.[0-9]+$/) )) && $(this).val() != "") {
                                $("#err_alto_her").html("Ingrese solo números decimales con punto: 2.5");
                                $("#err_alto_her").show();
                                $(this).addClass('input-error');
                                next_step = false;
                            }
                            else {
                                $(this).removeClass('input-error');
                                $("#err_alto_her").hide();
                            }
                        }else if (($(this).attr('name')=="diametro_her")) {
                            if ( !($(this).val().match(/^[0-9]+$/) || ($(this).val().match(/^[0-9]+\.[0-9]+$/) )) && $(this).val() != "") {
                                $("#err_diametro_her").html("Ingrese solo números decimales con punto: 2.5");
                                $("#err_diametro_her").show();
                                $(this).addClass('input-error');
                                next_step = false;
                            }
                            else {
                                $(this).removeClass('input-error');
                                $("#err_diametro_her").hide();
                            }
                        }
                        else {
                            $(this).removeClass('input-error');
                        }
                    }
                });
                if (!next_step){
                    e.preventDefault();
                }
        
            });
        
           
           parent_fieldset.find('input[type="text"],input[type="checkbox"],select[type="select"], textarea[name="propositoDescripcion"], input[name="itemServicio"], input[type="date"]').each(function () {         

            if ($(this).val() == "") {
                $(this).addClass('input-error');
                next_step = false;
            }
            else {
                $(this).removeClass('input-error');
            }

        });


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