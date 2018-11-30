/**
 * Funciones validadoras del primer paso
 */

const requiredFieldMessage = 'Este campo es requerido'









/*
COLOCA EN INPUTS TODOS TUS CAMPOS
*/






const inputs = [
    'nombre_add', 'apellido_add', 'ci_add', 'email_add', 'email_alt_add', 'telefono_add',
    'pagina_web_add', 'categoria_add', 'cargo_add', 'fecha_ingreso_add', 'fecha_salida_add',
    'estatus_add', 'operador_add', 'celular_add', 'persona_contacto', 'contacto_emergencia_add',
    'direccion_add', 'gremio_add', 'fecha_ingreso_usb_add', 'fecha_ingreso_ulab_add',
    'fecha_ingreso_admin_publica_add', 'condicion_add', 'ubicacion_add', 'dependencia_add', 'rol_add',
    'fecha_inicio_1_add', 'fecha_final_1_add', 'cargo_hist_1_add', 'dependencia_hist_1_add', 'organizacion_1_add',
    'fecha_inicio_2_add', 'fecha_final_2_add', 'cargo_hist_2_add', 'dependencia_hist_2_add', 'organizacion_2_add',
    'fecha_inicio_3_add', 'fecha_final_3_add', 'cargo_hist_3_add', 'dependencia_hist_3_add', 'organizacion_3_add',
    'fecha_inicio_4_add', 'fecha_final_4_add', 'cargo_hist_4_add', 'dependencia_hist_4_add', 'organizacion_4_add',
    'fecha_inicio_5_add', 'fecha_final_5_add', 'cargo_hist_5_add', 'dependencia_hist_5_add', 'organizacion_5_add',
    // Competencias
    'competencia1_nombre',
    'competencia2_nombre',
    'competencia3_nombre',
    'competencia4_nombre',
    'competencia5_nombre',
    'competencia6_nombre',
    'competencia7_nombre',
    'competencia8_nombre',
    'competencia9_nombre',
    'competencia10_nombre',
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
        return false;
    }
    else if (!moment(voltearFecha($this.val())).isSameOrBefore(moment().format("YYYY-MM-DD"))){
        $this.attr("data-content", 'La fecha de ingreso tiene que ser antes de la fecha de hoy u hoy');
        $this.addClass('input-error');
        $this.attr("data-valido", 'false');
        $this.popover('show');
        return false;
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

    if (fecha_inicio !== "" && fecha_final !== "" && !moment(fecha_inicio).isSameOrBefore(fecha_final)){
        $this.attr("data-content", "La fecha de egreso tiene que ser despues que la fecha de ingreso o igual a esta.");
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
    validaFechaIngresoUSB,
    validaFechaIngresoUlab,
    validaFechaIngresoAdminPubl
]

const validadoresSegundoPaso = [
    validaEstatus,
    validaCategoria,
    validaCondicion,
    validaFechaIngreso,
    validaFechaSalida
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

// Funciones para validar los campos de historial de trabajo

function validaTrabajo1() {
    // Campos del formulario de un trabajo
    const $fechIn= $('[name="fecha_inicio_1_add"]');
    const $fechFin = $('[name="fecha_final_1_add');
    const $depen = $('[name="dependencia_hist_1_add"]');
    const $org = $('[name="organizacion_1_add"]');
    const $cargo = $('[name="cargo_hist_1_add"]');
    var arreglo = [$fechIn, $fechFin, $depen, $org, $cargo]
    var validacion = true;
    //Si uno de los campos de un trabajo esta lleno entonces los
    // demás también son requeridos
    for (var i=0; i<arreglo.length; i++) {
        if (arreglo[i].val() !== "") {
            for (var j=0; j<arreglo.length; j++) {
                if (arreglo[j].val() === ""){
                    arreglo[j].attr("data-content", requiredFieldMessage);
                    arreglo[j].addClass('input-error');
                    arreglo[j].attr("data-valido", "false");
                    arreglo[j].popover('show');
                    validacion = false;
                } else {
                    arreglo[j].removeClass('input-error');
                    arreglo[j].popover('hide');
                }
            }
            break;
        }
    }
    return validacion;
}

function validaTrabajo2() {
    const $fechIn= $('[name="fecha_inicio_2_add"]');
    const $fechFin = $('[name="fecha_final_2_add');
    const $depen = $('[name="dependencia_hist_2_add"]');
    const $org = $('[name="organizacion_2_add"]');
    const $cargo = $('[name="cargo_hist_2_add"]');
    var arreglo = [$fechIn, $fechFin, $depen, $org, $cargo]
    var validacion = true;

    for (var i=0; i<arreglo.length; i++) {
        if (arreglo[i].val() !== "") {
            for (var j=0; j<arreglo.length; j++) {
                if (arreglo[j].val() === ""){
                    arreglo[j].attr("data-content", requiredFieldMessage);
                    arreglo[j].addClass('input-error');
                    arreglo[j].attr("data-valido", "false");
                    arreglo[j].popover('show');
                    validacion = false;
                } else {
                    arreglo[j].removeClass('input-error');
                    arreglo[j].popover('hide');
                }
            }
            break;
        }
    }
    return validacion;
}

function validaTrabajo3() {
    const $fechIn= $('[name="fecha_inicio_3_add"]');
    const $fechFin = $('[name="fecha_final_3_add');
    const $depen = $('[name="dependencia_hist_3_add"]');
    const $org = $('[name="organizacion_3_add"]');
    const $cargo = $('[name="cargo_hist_3_add"]');
    var arreglo = [$fechIn, $fechFin, $depen, $org, $cargo]
    var validacion = true;

    for (var i=0; i<arreglo.length; i++) {
        if (arreglo[i].val() !== "") {
            for (var j=0; j<arreglo.length; j++) {
                if (arreglo[j].val() === ""){
                    arreglo[j].attr("data-content", requiredFieldMessage);
                    arreglo[j].addClass('input-error');
                    arreglo[j].attr("data-valido", "false");
                    arreglo[j].popover('show');
                    validacion = false;
                } else {
                    arreglo[j].removeClass('input-error');
                    arreglo[j].popover('hide');
                }
            }
            break;
        }
    }
    return validacion;
}

function validaTrabajo4() {
    const $fechIn= $('[name="fecha_inicio_4_add"]');
    const $fechFin = $('[name="fecha_final_4_add');
    const $depen = $('[name="dependencia_hist_4_add"]');
    const $org = $('[name="organizacion_4_add"]');
    const $cargo = $('[name="cargo_hist_4_add"]');
    var arreglo = [$fechIn, $fechFin, $depen, $org, $cargo]
    var validacion = true;

    for (var i=0; i<arreglo.length; i++) {
        if (arreglo[i].val() !== "") {
            for (var j=0; j<arreglo.length; j++) {
                if (arreglo[j].val() === ""){
                    arreglo[j].attr("data-content", requiredFieldMessage);
                    arreglo[j].addClass('input-error');
                    arreglo[j].attr("data-valido", "false");
                    arreglo[j].popover('show');
                    validacion = false;
                } else {
                    arreglo[j].removeClass('input-error');
                    arreglo[j].popover('hide');
                }
            }
            break;
        }
    }
    return validacion;
}

function validaTrabajo5() {
    const $fechIn= $('[name="fecha_inicio_5_add"]');
    const $fechFin = $('[name="fecha_final_5_add');
    const $depen = $('[name="dependencia_hist_5_add"]');
    const $org = $('[name="organizacion_5_add"]');
    const $cargo = $('[name="cargo_hist_5_add"]');
    var arreglo = [$fechIn, $fechFin, $depen, $org, $cargo]
    var validacion = true;

    for (var i=0; i<arreglo.length; i++) {
        if (arreglo[i].val() !== "") {
            for (var j=0; j<arreglo.length; j++) {
                if (arreglo[j].val() === ""){
                    arreglo[j].attr("data-content", requiredFieldMessage);
                    arreglo[j].addClass('input-error');
                    arreglo[j].attr("data-valido", "false");
                    arreglo[j].popover('show');
                    validacion = false;
                } else {
                    arreglo[j].removeClass('input-error');
                    arreglo[j].popover('hide');
                }
            }
            break;
        }
    }
    return validacion;
}

function validaFechaInicio1(){
    const $this = $('[name="fecha_inicio_1_add"]');
    if ($this.val() !== ""){
        if (!moment(voltearFecha($this.val())).isSameOrBefore(moment().format("YYYY-MM-DD"))){
            $this.attr("data-content", 'La fecha tiene que ser antes de la fecha de hoy u hoy');
            $this.addClass('input-error');
            $this.attr("data-valido", 'false');
            $this.popover('show');
            return false;
        }
        else{
            $this.removeClass('input-error');
            $this.popover('hide');
            return true;
        }
    } else {
        return true;
    }
}

function validaFechaFin1(){
    const $this = $('[name="fecha_final_1_add"]');
    const fecha_inicio = voltearFecha($('[name="fecha_inicio_1_add"]').val());
    const fecha_final = voltearFecha($this.val());

    if ( !moment(fecha_final).isSameOrBefore(moment().format("YYYY-MM-DD")) ){
        $this.attr("data-content", "La fecha de egreso tiene que ser despues que la fecha de ingreso o igual a esta. No puede ser una fecha futura.");
        $this.addClass('input-error');
        $this.attr("data-valido", 'false');
        $this.popover('show');
        return false;
    } else if (fecha_inicio !== "" && fecha_final !== "" && (!moment(fecha_inicio).isSameOrBefore(fecha_final))){
        $this.attr("data-content", "La fecha de egreso tiene que ser despues que la fecha de ingreso o igual a esta. No puede ser una fecha futura.");
        $this.addClass('input-error');
        $this.attr("data-valido", 'false');
        $this.popover('show');
        return false;
    } else {
        $this.removeClass('input-error');
        $this.popover('hide');
        return true;
    }
}

function validaFechaInicio2(){
    const $this = $('[name="fecha_inicio_2_add"]');
    if ($this.val() != ""){
        if (!moment(voltearFecha($this.val())).isSameOrBefore(moment().format("YYYY-MM-DD"))){
            $this.attr("data-content", 'La fecha tiene que ser antes de la fecha de hoy');
            $this.addClass('input-error');
            $this.attr("data-valido", 'false');
            $this.popover('show');
            return false;
        }
        else{
            $this.removeClass('input-error');
            $this.popover('hide');
            return true;
        }
    } else {
        return true;
    }
}

function validaFechaFin2(){
    const $this = $('[name="fecha_final_2_add"]');
    const fecha_inicio = voltearFecha($('[name="fecha_inicio_2_add"]').val());
    const fecha_final = voltearFecha($this.val());

    if (fecha_inicio !== "" && fecha_final !== "" && (!moment(fecha_inicio).isSameOrBefore(fecha_final) || !moment(fecha_final).isSameOrBefore(moment().format("YYYY-MM-DD")) ) ){
        $this.attr("data-content", "La fecha de egreso tiene que ser despues que la fecha de ingreso o igual a esta");
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

function validaFechaInicio3(){
    const $this = $('[name="fecha_inicio_3_add"]');
    if ($this.val() != ""){
        if (!moment(voltearFecha($this.val())).isSameOrBefore(moment().format("YYYY-MM-DD"))){
            $this.attr("data-content", 'La fecha tiene que ser antes de la fecha de hoy');
            $this.addClass('input-error');
            $this.attr("data-valido", 'false');
            $this.popover('show');
            return false;
        }
        else{
            $this.removeClass('input-error');
            $this.popover('hide');
            return true;
        }
    } else {
        return true;
    }
}

function validaFechaFin3(){
    const $this = $('[name="fecha_final_3_add"]');
    const fecha_inicio = voltearFecha($('[name="fecha_inicio_3_add"]').val());
    const fecha_final = voltearFecha($this.val());

    if (fecha_inicio !== "" && fecha_final !== "" && (!moment(fecha_inicio).isSameOrBefore(fecha_final) || !moment(fecha_final).isSameOrBefore(moment().format("YYYY-MM-DD")) ) ){
        $this.attr("data-content", "La fecha de egreso tiene que ser despues que la fecha de ingreso o igual a esta");
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

function validaFechaInicio4(){
    const $this = $('[name="fecha_inicio_4_add"]');
    if ($this.val() != ""){
        if (!moment(voltearFecha($this.val())).isSameOrBefore(moment().format("YYYY-MM-DD"))){
            $this.attr("data-content", 'La fecha tiene que ser antes de la fecha de hoy');
            $this.addClass('input-error');
            $this.attr("data-valido", 'false');
            $this.popover('show');
            return false;
        }
        else{
            $this.removeClass('input-error');
            $this.popover('hide');
            return true;
        }
    } else {
        return true;
    }
}

function validaFechaFin4(){
    const $this = $('[name="fecha_final_4_add"]');
    const fecha_inicio = voltearFecha($('[name="fecha_inicio_4_add"]').val());
    const fecha_final = voltearFecha($this.val());

    if (fecha_inicio !== "" && fecha_final !== "" && (!moment(fecha_inicio).isSameOrBefore(fecha_final) || !moment(fecha_final).isSameOrBefore(moment().format("YYYY-MM-DD")) ) ){
        $this.attr("data-content", "La fecha de egreso tiene que ser despues que la fecha de ingreso o igual a esta");
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

function validaFechaInicio5(){
    const $this = $('[name="fecha_inicio_5_add"]');
    if ($this.val() != ""){
        if (!moment(voltearFecha($this.val())).isSameOrBefore(moment().format("YYYY-MM-DD"))){
            $this.attr("data-content", 'La fecha tiene que ser antes de la fecha de hoy');
            $this.addClass('input-error');
            $this.attr("data-valido", 'false');
            $this.popover('show');
            return false;
        }
        else{
            $this.removeClass('input-error');
            $this.popover('hide');
            return true;
        }
    } else {
        return true;
    }
}

function validaFechaFin5(){
    const $this = $('[name="fecha_final_5_add"]');
    const fecha_inicio = voltearFecha($('[name="fecha_inicio_5_add"]').val());
    const fecha_final = voltearFecha($this.val());

    if (fecha_inicio !== "" && fecha_final !== "" && (!moment(fecha_inicio).isSameOrBefore(fecha_final) || !moment(fecha_final).isSameOrBefore(moment().format("YYYY-MM-DD")) ) ){
        $this.attr("data-content", "La fecha de egreso tiene que ser despues que la fecha de ingreso o igual a esta");
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

const validadoresQuintoPaso = [
    validaTrabajo1,
    validaTrabajo2,
    validaTrabajo3,
    validaTrabajo4,
    validaTrabajo5,
    validaFechaInicio1,
    validaFechaFin1,
    validaFechaInicio2,
    validaFechaFin2,
    validaFechaInicio3,
    validaFechaFin3,
    validaFechaInicio4,
    validaFechaFin4,
    validaFechaInicio5,
    validaFechaFin5
]

function validaCompetencia(){
    var valid=true;
    for(var i=1; i<11;i++){
        if($('#competencia-container'+i).is(':hidden'))
            continue;

        var nombre = $('#competencia'+i+'_nombre');
        var chosenval = $('#competencia'+i+'_categoria').trigger("chosen-updated").val().length;
        chosen_container = $('#competencia'+i+'_categoria_chosen');
        if (chosenval == 0){
            chosen_container.attr("data-content", requiredFieldMessage);
            chosen_container.addClass('input-error');
            chosen_container.attr("data-valido", 'false');
            chosen_container.popover('show');
            valid = valid && false
        }
        else {
            chosen_container.removeClass('input-error');
            chosen_container.popover('hide');
            valid = valid && true;
        }
        if (nombre.val()==='') {
            nombre.attr("data-content", requiredFieldMessage);
            nombre.popover('show');
            nombre.addClass('input-error');
            valid = valid && false;
        }
        else {
            nombre.removeClass('input-error');
            nombre.popover('hide');
            valid = valid && true;
        }
    }
    return valid

}
const validadoresCuartoPaso = [
    validaCompetencia
]

// ESCRIBE AQUI TUS FUNCIONES















// ESCRIBE ALGO COMO
/*
const validadoresSextoPaso = [
]
*/






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


    //$('[name="fecha_inicio_1_add"]').on('change', validaFechaInicio)
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
        if ($("#sel2 option:selected").val()==="Fijo") {
            $("#fsalida").hide();
            $('#fingreso').show()
            $('[name="fecha_ingreso_add"]').val('');
            $('[name="fecha_salida_add"]').val('');
        }
        else {
            $("#fsalida").show();
            $("#fingreso").hide();
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
                $('[name="fecha_ingreso_add"]').val('');
                $('[name="fecha_salida_add"]').val('');

                next_step = validadoresCorrectos(validadoresSegundoPasoFijo)
            }
            else {
                next_step = validadoresCorrectos(validadoresSegundoPaso)
            }
        }
        else if (parent_fieldset.attr('id') === 'p3'){
            next_step = validadoresCorrectos(validadoresTercerPaso)
        }

        else if (parent_fieldset.attr('id') === 'p4'){
            next_step = validadoresCorrectos(validadoresCuartoPaso)
        }







        /* AQUI VAN OTROS ELSE IF CON LOS PASOS POR EJEMPLO
        
        //Paso de Moises
        else if (parent_fieldset.attr('id') === 'p4')
            next_step = validadoresCorrectos(validadoresCuartoPaso)
        
        // Paso de Constanza
        else if(parent_fieldset.attr('id') === 'p5')
            next_step = validadoresCorrectos(validadoresQuintoPaso)

        SI EL TUYO ES EL ULTIMO PASO ANTES DE HACER SUBMMIT NO VA AQUI

        */













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
    $('.registration-form .btn-submit').on('click', function (e) {
        
        var parent_fieldset = $(this).parents('fieldset');
        
        var enviar = validadoresCorrectos(validadoresQuintoPaso);




        /* 
        SI TU PASO ES EL ULTIMO ANTES DE HACER SUBMIT ENTONCES COLOCA TUS
        FUNCIONES EN ENVIAR POR EJEMPLO
        var enviar = validadoresCorrectos(validadoresSextoPaso);
        Y LISTO
        */











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
