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

// Funciones que validan toda la pagina 1 del formulario 
function validaPaginaWeb () {
    const $this = $('[name="pagina_web_add"]')
    if ($this.val() === '') {
        $this.popover('hide');
        return true;
    }
    if (!($this.val().match(/^((https?|ftp|smtp):\/\/)?(www.)?[a-z0-9]+\.[a-z]+(\/[a-zA-Z0-9#]+\/?)*$/))) {
        $this.attr('data-content', "Formato incorrecto de pagina web. Ejemplo: hola.com");
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
    if (!($this.val().match(/^(([^<>()\[\]\.,;:\s@\"]+(\.[^<>()\[\]\.,;:\s@\"]+)*)|(\".+\"))@(([^<>()[\]\.,;:\s@\"]+\.)+[^<>()[\]\.,;:\s@\"]{2,})$/))){
        $this.attr("data-content", "El correo no tiene el formato correcto. Ejemplo: hola_mundo@dominio.com");
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
    const val = $this.val().replace(/-/g, '')
    if (val === '') {
        $this.attr('data-content', requiredFieldMessage);
        $this.popover('show');
        $this.addClass('input-error');
        $this.attr("data-valido", "false");
        return false;
    }
    if (!(val.match(/^\d{7}$/gm))) { // Extension de 1 a 4 digitos
        $this.attr('data-content', 'El número de celular tiene el formato incorrecto. Ejemplo 1234567');
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
    const val = $this.val().replace(/[()-]/g, '')
    if (val === '') {
        $this.attr("data-content", requiredFieldMessage);
        $this.addClass('input-error');
        $this.attr("data-valido", "false");
        $this.popover('show')
        return false;
    }
    if (!(val.match(/^\d{11}$/gm))){
        $this.attr("data-content", "El teléfono tiene el formato incorrecto. Ejemplo: 02121234567");
        $this.addClass('input-error');
        $this.attr("data-valido", "false");
        $this.popover('show');
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
    const val = $this.val().replace(/[()-]/g, '')
    if (val === '') {
        $this.attr("data-content", requiredFieldMessage);
        $this.addClass('input-error');
        $this.attr("data-valido", "false");
        $this.popover('show');
        return false;
    }
    if (!val.match(/\d{11}$/)) { 
        $this.attr("data-content", 'El contacto de emergencia debe tener solo números. Ejemplo: 02121234567');
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

// Funciones que validan la segunda pagina 
function validaEstatus(){
    const $this = $('[name="estatus_add"]')
    if ($this.val() === null){
        $this.attr("data-content", requiredFieldMessage);
        $this.addClass('input-error');
        $this.attr("data-valido", 'false');
        $this.popover('show');
        return false
    }
    else {
        $this.removeClass('input-error');
        $this.popover('hide');
        return true;
    }
}

function validaCategoria(){
    const $this = $('[name="categoria_add"]')
    if ($this.val() === null){
        $this.attr("data-content", requiredFieldMessage);
        $this.addClass('input-error');
        $this.attr("data-valido", 'false');
        $this.popover('show');
        return false
    }
    else {
        $this.removeClass('input-error');
        $this.popover('hide');
        return true;
    }
}

function validaCondicion(){
    const $this = $('[name="condicion_add"]')
    if ($this.val() === null){
        $this.attr("data-content", requiredFieldMessage);
        $this.addClass('input-error');
        $this.attr("data-valido", 'false');
        $this.popover('show');
        return false
    }
    else {
        $this.removeClass('input-error');
        $this.popover('hide');
        return true;
    }
}

function validaFechaIngreso(){
    const $this = $('[name="fecha_ingreso_add"]');
    if ($this.val() === ""){
        $this.attr("data-content", requiredFieldMessage);
        $this.addClass('input-error');
        $this.attr("data-valido", 'false');
        $this.popover('show');
    }
    else if (!moment(voltearFecha($this.val())).isSameOrBefore(moment().format("YYYY-MM-DD"))){
        $this.attr("data-content", 'La fecha de ingreso tiene que ser antes de la fecha de hoy');
        $this.addClass('input-error');
        $this.attr("data-valido", 'false');
        $this.popover('show');
    }
    else{
        $this.removeClass('input-error');
        $this.popover('hide');
        return true;
    }
}

// Funcion que se encarga de voltear la fecha y se muestre en el formato pedido
function voltearFecha(fecha){
    if (fecha !== ""){
        var dia = fecha.substr(0,2);
        var mes = fecha.substr(3,2);
        var anio = fecha.substr(6,10);
    
        var fecha = anio + "-" + mes + "-" + dia;
        
        return fecha;
    }
    else {
        return "";
    }
}

function validaFechaSalida(){
    const $this = $('[name="fecha_salida_add"]');
    const fecha_inicio = voltearFecha($('[name="fecha_ingreso_add"]').val());
    const fecha_final = voltearFecha($this.val());
    if (fecha_inicio !== "" && fecha_final !== "" && !moment(fecha_inicio).isBefore(fecha_final)){
        $this.attr("data-content", "La fecha de egreso tiene que ser antes que la fecha de ingreso");
        $this.addClass('input-error');
        $this.attr("data-valido", 'false');
        $this.popover('show');
        return false
    }
    else{
        $this.removeClass('input-error');
        $this.popover('hide');
        return true;
    }
}

function validaFechaIngresoUSB(){
    const $this = $('[name="fecha_ingreso_usb_add"]');
    const fecha_ingreso_ulab = voltearFecha($('[name="fecha_ingreso_ulab_add"]').val());
    const fecha_ingreso_usb = voltearFecha($this.val());

    if ($this.val() === "" && $('[name="categoria_add"]').val() !== 'Fijo'){
        $this.attr("data-content", requiredFieldMessage);
        $this.addClass('input-error');
        $this.attr("data-valido", 'false');
        $this.popover('show');
        return false
    }
    else if (fecha_ingreso_ulab !== "" && !(moment(fecha_ingreso_usb).isBefore(fecha_ingreso_ulab) || moment(fecha_ingreso_usb).isSame(fecha_ingreso_ulab))){
        $this.attr("data-content", "La fecha de ingreso al USB tiene que ser antes de la fecha de ingreso al ULAB");
        $this.addClass('input-error');
        $this.popover('show');
        return false;
    }
    else{
        $this.removeClass('input-error');
        $this.popover('hide');
        return true;
    }
}

function validaFechaIngresoUlab(){
    const $this = $('[name="fecha_ingreso_ulab_add"]');
    const fecha_inicio = voltearFecha($('[name="fecha_ingreso_add"]').val());
    const fecha_ingreso_ulab = voltearFecha($this.val());

    if ($this.val() === "" && $('[name="categoria_add"]').val() !== 'Fijo'){
        $this.attr("data-content", requiredFieldMessage);
        $this.addClass('input-error');
        $this.attr("data-valido", 'false');
        $this.popover('show');
        return false;
    }
    else if (fecha_inicio !== "" && !(moment(fecha_ingreso_ulab).isBefore(fecha_inicio) || moment(fecha_ingreso_ulab).isSame(fecha_inicio))) {
        $this.attr("data-content", "La fecha de ingreso al ULAB tiene que ser antes que la fecha de ingreso");
        $this.addClass('input-error');
        $this.popover('show');
        return false;
    }
    else{
        $this.removeClass('input-error');
        $this.popover('hide');
        return true;
    }
}

function validaFechaIngresoAdminPubl(){
    const $this = $('[name="fecha_ingreso_admin_publica_add"]');
    const fecha_ingreso_usb = voltearFecha($('[name="fecha_ingreso_usb_add"]').val());
    const fecha_ingreso_admin_pub = voltearFecha($this.val());

    if ($this.val() === "" && $('[name="categoria_add"]').val() !== 'Fijo'){
        $this.attr("data-content", requiredFieldMessage);
        $this.addClass('input-error');
        $this.attr("data-valido", 'false');
        $this.popover('show');
        return false;
    }
    else if (fecha_ingreso_usb !== "" && !(moment(fecha_ingreso_admin_pub).isBefore(fecha_ingreso_usb) || moment(fecha_ingreso_admin_pub).isSame(fecha_ingreso_usb))){
        $this.attr("data-content", "La fecha de ingreso a la administración pública debe ser antes de la fecha de ingreso a la USB");
        $this.addClass('input-error');
        $this.popover('show');
        return false;
    }
    else{
        $this.removeClass('input-error');
        $this.popover('hide');
        return true;
    }
}

const validadoresSegundoPasoFijo = [
    validaEstatus,
    validaCategoria,
    validaCondicion,
    validaFechaIngreso,
    validaFechaSalida
]
const validadoresSegundoPaso = [
    validaEstatus,
    validaCategoria,
    validaCondicion,
    validaFechaIngreso,
    validaFechaSalida,
    validaFechaIngresoUSB,
    validaFechaIngresoUlab,
    validaFechaIngresoAdminPubl
]

// Funciones para validar la tercera parte del formulario

function validarCargo(){
    const $this = $('[name="cargo_add"]');
    if ($this.val() === ''){
        $this.attr("data-content", requiredFieldMessage);
        $this.addClass('input-error');
        $this.attr("data-valido", "false");
        $this.popover('show');
        return false;
    } 
    else {
        $this.removeClass('input-error');
        $this.popover('hide');
        return true;
    }
}

function validarGremio(){
    const $this = $('[name="gremio_add"]');
    if ($this.val() === null){
        $this.attr("data-content", requiredFieldMessage);
        $this.addClass('input-error');
        $this.attr("data-valido", "false");
        $this.popover('show');
        return false;
    }
    else {
        $this.removeClass('input-error');
        $this.popover('hide');
        return true;
    }
}

function validarUbicacion(){
    const $this = $('[name="ubicacion_add"]');
    if ($this.val() === null){
        $this.attr("data-content", requiredFieldMessage);
        $this.addClass('input-error');
        $this.attr("data-valido", "false");
        $this.popover('show');
        return false;
    }
    else {
        $this.removeClass('input-error');
        $this.popover('hide');
        return true;
    }
}

function validarRol(){
    const $this = $('[name="rol_add"]');
    if ($this.val() === null){
        $this.attr("data-content", requiredFieldMessage);
        $this.addClass('input-error');
        $this.attr("data-valido", "false");
        $this.popover('show');
        return false;
    }
    else {
        $this.removeClass('input-error');
        $this.popover('hide');
        return true;
    }
}

const validadoresTercerPaso = [
    validarCargo,
    validarGremio,
    validarUbicacion,
    validarRol
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
    $('.fselect').fSelect({
        placeholder: 'Escoja sus ubicaciones',
        numDisplayed: 3,
        overflowText: '{n} ubicaciones',
        searchText: 'Buscar',
        showSearch: true
    })

    new Cleave('[name="telefono_add"]', {
        // delimiter: '-',
        delimiters: ['(', ')', '-'],
        blocks: [0, 4, 3, 4],
    })
    new Cleave('[name="contacto_emergencia_add"]', {
        // delimiter: '-',
        delimiters: ['(', ')', '-'],
        blocks: [0, 4, 3, 4],
    })
    new Cleave('[name="celular_add"]', {
        delimiter: '-',
        blocks: [3, 4]
    })

    $('.registration-form fieldset:first-child').fadeIn('slow');

    $('#sel2').change(function (){
        if ($("#sel2 option:selected").val()=="Fijo") {
            $("#fingreso").hide();

        }
        else {
            $("#fingreso").show();
        };
    });

    //-------------------------------- Primera parte del form agregar -----------------------------------------//

    validacionTiempoReal();

    // next step
    $('.registration-form .btn-next').on('click', function () {
        var parent_fieldset = $(this).parents('fieldset');
        var next_step = true;
        if (parent_fieldset.attr('id') === 'p1') {
            next_step = validadoresCorrectos(validadoresPrimerPaso)
        }
        else if (parent_fieldset.attr('id') === 'p2'){
            if ($('[name="categoria_add"]').val() === 'Fijo'){
                // Vacio los campos de fecha de ingreso y de salida para que no se guarden en la 
                // base de datos 
                $('[name="fecha_ingreso_usb_add"]').val('')
                $('[name="fecha_ingreso_ulab_add"]').val('');
                $('[name="fecha_ingreso_admin_publica_add"]').val('')

                next_step = validadoresCorrectos(validadoresSegundoPasoFijo)
            }
            else {
                next_step = validadoresCorrectos(validadoresSegundoPaso)
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
    $(inputSelectorsAll).on('focus change click', function(e){
        $(this).popover('hide');
        $(this).removeClass('input-error');
    })

    $('#formularioCarga').on('keyup keypress', function(e) {
        var keyCode = e.keyCode || e.which;
        if (keyCode === 13) { 
          e.preventDefault();
          return false;
        }
      });
    // submit
    $('#submit').on('click', function (e) {
        var parent_fieldset = $(this).parents('fieldset');
        var enviar = validadoresCorrectos(validadoresTercerPaso);
        console.log(enviar)
        if (enviar){
            $(this).attr("type", "submit");
        }
        else {
            $(this).attr("type", "button");
        }

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
