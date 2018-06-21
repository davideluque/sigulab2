/**
 * Funciones validadoras del primer paso
 */

const requiredFieldMessage = 'Este campo es requerido'
const inputs = [
    'nombre_add', 'apellido_add', 'ci_add', 'email_add', 'email_alt_add', 'telefono_add',
    'pagina_web_add', 'categoria_add', 'cargo_add', 'fecha_ingreso_add', 'fecha_salida_add',
    'estatus_add', 'operador_add', 'celular_add', 'persona_contacto', 'contacto_emergencia_add',
    'direccion_add', 'gremio_add', 'fecha_ingreso_usb_add', 'fecha_ingreso_ulab_add',
    'fecha_ingreso_admin_publica_add', 'condicion_add', 'ubicacion_add', 'dependencia_add', 'rol_add',
]

const inputSelectorsAll = inputs.map(i => `[name="${i}"]`).join(',')

function validaPaginaWeb () {
    const $this = $('[name="pagina_web_add"]')
    if ($this.val() === '') {
        $this.popover('hide');
        return true;
    }
    if (!($this.val().match(/^((https?|ftp|smtp):\/\/)?(www.)?[a-z0-9]+\.[a-z]+(\/[a-zA-Z0-9#]+\/?)*$/))) {
        $this.attr('data-content', "Formato incorrecto de pagina web");
        $this.popover('show');
        $this.addClass('input-error');
        $this.attr("data-valido", "false");
        return false;
    }
    else {
        $this.removeClass('input-error');
        $this.popover('hide');
        $this.attr("data-valido", "true");
        return true;
    }
}

function validaEmailAlternativo () {
    const $this = $('[name="email_alt_add"]')
    if ($this.val() === '') {
        $this.popover('hide');
        return true;
    }
    if (!($this.val().match(/^(([^<>()\[\]\.,;:\s@\"]+(\.[^<>()\[\]\.,;:\s@\"]+)*)|(\".+\"))@(([^<>()[\]\.,;:\s@\"]+\.)+[^<>()[\]\.,;:\s@\"]{2,})$/)) || $this.val() < 999999999){
        $this.attr("data-content", "El correo no tiene el formato correcto");
        console.log($this.popover('show'));
        $this.addClass('input-error');
        $this.attr("data-valido", "false");
        return false;
    }
    else {
        $this.removeClass('input-error');
        $this.attr("data-valido", "true");
        $this.popover('hide');
        return true;
    }
}

function validaOperador () {
    const $this = $('[name="operador_add"]')
    if (!$this.val()) {
        $this.attr('data-content', requiredFieldMessage);
        $this.popover('show');
        $this.addClass('input-error');
        $this.attr("data-valido", "false");
        return false;
    }
    else {
        $this.removeClass('input-error');
        $this.attr("data-valido", "true");
        $this.popover('hide');
        return true;
    }
}

function validaCelular () {
    const $this = $('[name="celular_add"]')
    if ($this.val() === '') {
        $this.attr('data-content', requiredFieldMessage);
        $this.popover('show');
        $this.addClass('input-error');
        $this.attr("data-valido", "false");
        return false;
    }
    if (!($this.val().match(/^\d{7}$/gm))) { // Extension de 1 a 4 digitos
        $this.attr('data-content', 'El número de celular tiene el formato incorrecto');
        $this.popover('show');
        $this.addClass('input-error');
        $this.attr("data-valido", "false");
        return false;
    }
    else {
        $this.removeClass('input-error');
        $this.attr("data-valido", "true");
        $this.popover('hide');
        return true;
    }
}

function validaDireccionHab () {
    const $this = $('[name="direccion_add"]')
    if ($this.val() === '') {
        $this.attr("data-content", requiredFieldMessage);
        $this.popover('show');
        $this.addClass('input-error');
        return false;
    }
    else {
        $this.removeClass('input-error');
        $this.popover('hide');
        return true;
    }
}

function validaTelefonoResidencial (){
    const $this = $('[name="telefono_add"]')
    if ($this.val() === '') {
        $this.attr("data-content", requiredFieldMessage);
        $this.addClass('input-error');
        $this.attr("data-valido", "false");
        return false;
    }
    if (!($this.val().match(/^\d+$/gm)) || $this.val() < 999999999){
        $this.attr("data-content", "El teléfono tiene el formato incorrecto");
        $this.addClass('input-error');
        $this.attr("data-valido", "false");
        return false;
    }
    else {
        $this.removeClass('input-error');
        $this.attr("data-valido", "true");
        $this.popover('hide');
        return true;
    }
}

function validaPersonaContacto () {
    const $this = $('[name="persona_contacto"]')
    if ($this.val() === '') {
        $this.attr("data-content", requiredFieldMessage);
        $this.popover('show');
        $this.addClass('input-error');
        return false;
    }
    else {
        $this.removeClass('input-error');
        $this.popover('hide');
        return true;
    }

}

function validaContactoEmergencia () {
    const $this = $('[name="contacto_emergencia_add"]')
    if ($this.val() === '') {
        $this.attr("data-content", requiredFieldMessage);
        $this.addClass('input-error');
        $this.attr("data-valido", "false");
        return false;
    }
    if (!$this.val().match(/\d{7}$/)) { // Extension de 1 a 4 digitos
        $this.attr("data-content", 'El contacto de emergencia debe tener solo números');
        $this.popover('show');
        $this.addClass('input-error');
        return false;
    }
    else {
        $this.removeClass('input-error');
        $this.popover('hide');
        return true;
    }
}

const validadoresPrimerPaso = [
    validaPaginaWeb,
    validaEmailAlternativo,
    validaOperador,
    validaCelular,
    validaDireccionHab,
    validaTelefonoResidencial,
    validaPersonaContacto,
    validaContactoEmergencia
]

// Funcion que valida los campos cuando el usuario pasa a llenar otro input
function validacionTiempoReal(){

    // Manejo de error del telefono
    $('[name="telefono_add"]').on('change', validaTelefonoResidencial)

    // Manejo del error de email alternativo
    $('[name="email_alt_add"]').on('change', validaEmailAlternativo)

    // Manejo de error del numero de celular
    $('[name="celular_add"]').on('change', validaCelular);

    // Manejo de error del campo de contacto de emergencia
    $('[name="contacto_emergencia_add"]').on('change', validaContactoEmergencia)

    // Manejo de error del campo de pagina de web
    $('[name="pagina_web_add"]').on('change', validaPaginaWeb)

    $('[name="direccion_add"]').on('change', validaDireccionHab)
}

/**
 * Funcion que determina si los validadores pasan o no
 * @param {array_fun} validatorsList Arreglo que tiene funciones validadores. La firma de cada funcion es:
 * () -> bool
 */
function validadoresCorrectos(validatorsList) {
    return validatorsList
        .map(fn => fn())
        .reduce((acc, i) => acc && i, true)
}

$(document).ready(function () {
    $('.registration-form fieldset:first-child').fadeIn('slow');

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
            next_step = validadoresPrimerPaso.map(fn => fn()).reduce((acc, i) => acc && i, true)
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
    $(inputSelectorsAll).on('focus change click', function(e){
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
