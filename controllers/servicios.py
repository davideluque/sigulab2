
#
# Controladores de las funcionalidades del modulo de Servicios
#
#
# - Erick Flejan <12-1155@usb.ve>
# - Amanda Camacho <12-10644@usb.ve>
# - David Cabeza <13-10191@usb.ve>
# - Fabiola Martínez <13-10838@usb.ve>
# - Lautaro Villalon <12-10427@usb.ve>
# - Yarima Luciani <13-10770@usb.ve>
#-----------------------------------------------------------------------------
from servicios_libreria import *
import re

# Pagina principal del modulo
@auth.requires_login(otherwise=URL('modulos', 'login'))
def index():

    solicitud_nueva = ListaSolicitudes(db, auth, "Ejecutante").cuenta > 0

    # TODO Sacar esto de la nueva tabla de historial?

    certificacion_nueva = ListaSolicitudes(db, auth, "Certificante").cuenta > 0

    return dict(solicitud_nueva=solicitud_nueva, certificacion_nueva=certificacion_nueva)


@auth.requires_login(otherwise=URL('modulos', 'login'))
def usuario():
    return dict(form=auth.profile(), form2=auth.change_password())

# Tabla de servicios agregados
@auth.requires_login(otherwise=URL('modulos', 'login'))
def listado(): 

    #----- AGREGAR SERVICIO -----#

    if request.post_vars.nombreServicio and request.post_vars.envio != "edicion":

        docencia = False if not request.post_vars.docenciaServicio else True
        investigacion = False if not request.post_vars.investigacionServicio else True
        extension = False if not request.post_vars.extensionServicio else True
        gestion = False if not request.post_vars.gestionServicio else True


        entregaResultados=  False if not request.post_vars.entregadeResultadosServicio else True
        ensayoCalibracion=  False if not request.post_vars.informedeEnsayoCalibracionServicio else True
        certificadoConformidadProducto=  False if not request.post_vars.certificadoConformidadServicio else True
        certificadoCalibracion=  False if not request.post_vars.certificadoCalibracionServicio else True
        otro=  False if not request.post_vars.otroServicio else True

        ambito_in_situ = False if not request.post_vars.ambito_in_situ else True
        ambito_en_campo =  False if not request.post_vars.ambito_en_campo else True
        ambito_otro =  False if not request.post_vars.ambito_otro else True

        servicio_nuevo = Servicio(db, request.post_vars.nombreServicio, request.post_vars.tipoServicio,
                   request.post_vars.categoriaServicio, request.post_vars.objetivoServicio,
                   request.post_vars.alcanceServicio, request.post_vars.metodoServicio,
                   request.post_vars.rangoServicio, request.post_vars.incertidumbreServicio,
                   request.post_vars.itemServicio, request.post_vars.requisitosServicio,
                   entregaResultados,ensayoCalibracion,certificadoConformidadProducto,certificadoCalibracion,
                   otro,docencia,investigacion, gestion, extension, True,
                   request.post_vars.responsableServicio, request.post_vars.dependenciaServicio, 
                   request.post_vars.ubicacionServicio, ambito_in_situ=ambito_in_situ, 
                   ambito_en_campo=ambito_en_campo, ambito_otro=ambito_otro, 
                   ambito_otro_detalle=request.post_vars.ambito_otro_detalle,
                   per_tecnico=request.post_vars.per_tecnico, cant_per_tecnico=request.post_vars.cant_per_tecnico, 
                   per_supervisor=request.post_vars.per_supervisor, cant_per_supervisor=request.post_vars.cant_per_supervisor,
                   per_tesista=request.post_vars.per_tesista, cant_per_tesista=request.post_vars.cant_per_tesista,
                   per_pasante=request.post_vars.per_pasante, cant_per_pasante=request.post_vars,
                   per_preparador=request.post_vars.per_preparador, cant_per_preparador=request.post_vars.cant_per_preparador,
                   per_obrero=request.post_vars.per_obrero, cant_per_obrero=request.post_vars.cant_per_obrero, 
                   per_otro=request.post_vars.per_otro, per_otro_detalle=request.post_vars.per_otro_detalle,
                   equipo_presta_servicio=request.post_vars.equipo_presta_servicio,
                   esp_fis_servicio=request.post_vars.esp_fis_servicio,
                   insumos_servicio=request.post_vars.insumos_servicio,
                   condicion_ambiental=request.post_vars.condicion_ambiental,
                   condicion_ambiental_detalle= request.post_vars.condicion_ambiental_detalle)

        servicio_nuevo.insertar()


        # Se envia el email de notificacion al agregar un servicio 

        ########################### TO DO #############################################
        #
        #            NO TIENE POR QUE SER UN ASSERT Y SI L ES QUE SEA DE ERROR
        #
        ##############################################################################

        try:
            idDependencia = db(auth.user_id == db.t_Personal.f_usuario).select(db.t_Personal.ALL)[0].f_dependencia

            dependencia = db(idDependencia == db.dependencias.id).select(db.dependencias.ALL)[0]

            jefe_dependencia = db(dependencia.id_jefe_dependencia == db.auth_user.id).select(db.auth_user.ALL)[0]

            assert(jefe_dependencia != None)
            
        except:

            return redirect(URL(args=request.args, vars=request.get_vars, host=True)) 
            

        nombre_y_apellido = "%s %s" % (jefe_dependencia.first_name, jefe_dependencia.last_name)

        nombre_anade = "%s %s" % (auth.user.first_name, auth.user.last_name)

        correo = '<html><head><meta charset="UTF-8"></head><body><table><tr><td><p>Hola, %s.</p><p>Se ha añadido un nuevo servicio. La operación fue realizada por %s, el/la cual pertenece a la dependencia de %s.</p><p>Para consultar dicha operación diríjase a la página web de <a href="159.90.171.24">SIGULAB</a>.</p><p>Saludos.</p></td></tr></table></body></html>' % (nombre_y_apellido, nombre_anade, dependencia.nombre)

        asunto = '[SIGULAB] ' + 'Se ha añadido un nuevo servicio'

        __enviar_correo(jefe_dependencia.email, asunto, correo)

        # Variable nombre persona que recibe el email

        # Variable nombre persona que realizo la operacion
        # nombreUsuario = auth.user.first_name + ' ' + auth.user.last_name

        # Variable rol persona que realizo la operacion
        # rolUsuario = db(auth.user_id == db.t_Personal.f_usuario).select(db.t_Personal.ALL)[0].rol   

        # Variable dependencia de la persona que realizo la operacion
        # dependenciaUsuario = db(idDependencia == db.dependencias.id).select(db.dependencias.ALL)[0].nombre

        return redirect(URL(args=request.args, vars=request.get_vars, host=True)) 

    #----- FIN AGREGAR SERVICIO -----#

    #----- EDITAR SERVICIO -----#

    elif request.post_vars.nombreServicio and request.post_vars.envio == "edicion":
        
        docencia = False if not request.post_vars.docenciaServicio else True
        investigacion = False if not request.post_vars.investigacionServicio else True
        extension = False if not request.post_vars.extensionServicio else True
        gestion = False if not request.post_vars.gestionServicio else True      

        entregaResultados=  False if not request.post_vars.entregadeResultadosServicio else True
        ensayoCalibracion=  False if not request.post_vars.informedeEnsayoCalibracionServicio else True
        certificadoConformidadProducto=  False if not request.post_vars.certificadoConformidadServicio else True
        certificadoCalibracion=  False if not request.post_vars.certificadoCalibracionServicio else True
        otro=  False if not request.post_vars.otroServicio else True

        ambito_in_situ = False if not request.post_vars.ambito_in_situ else True
        ambito_en_campo =  False if not request.post_vars.ambito_en_campo else True
        ambito_otro =  False if not request.post_vars.ambito_otro else True

        servicio_edicion = Servicio(db)
        servicio_edicion.instanciar(request.vars.idServicioEdit)

        servicio_edicion.editar(request.post_vars.nombreServicio, request.post_vars.tipoServicio,
                   request.post_vars.categoriaServicio, request.post_vars.objetivoServicio,
                   request.post_vars.alcanceServicio, request.post_vars.metodoServicio,
                   request.post_vars.rangoServicio, request.post_vars.incertidumbreServicio,
                   request.post_vars.itemServicio, request.post_vars.requisitosServicio,
                   entregaResultados,ensayoCalibracion,certificadoConformidadProducto,certificadoCalibracion,
                   otro, docencia,investigacion, gestion, extension, True,
                   request.post_vars.responsableServicio, request.post_vars.dependenciaServicio, 
                   request.post_vars.ubicacionServicio, ambito_in_situ, 
                   ambito_en_campo, ambito_otro, request.post_vars.ambito_otro_detalle,
                   request.post_vars.per_tecnico, request.post_vars.cant_per_tecnico, request.post_vars.per_supervisor, 
                   request.post_vars.cant_per_supervisor, request.post_vars.per_tesista, request.post_vars.cant_per_tesista,
                   request.post_vars.per_pasante, request.post_vars.cant_per_pasante, request.post_vars.per_preparador, 
                   request.post_vars.cant_per_preparador, request.post_vars.per_obrero, request.post_vars.cant_per_obrero,
                   request.post_vars.per_otro, request.post_vars.per_otro_detalle, 
                   request.post_vars.equipo_presta_servicio, request.post_vars.esp_fis_servicio, 
                   request.post_vars.insumos_servicio, request.post_vars.condicion_ambiental,
                   request.post_vars.condicion_ambiental_detalle)

        servicio_edicion.actualizar(request.vars.idServicioEdit)

        # Se envia el email de notificacion al editar un servicio 
       
        try:
            idDependencia = db(auth.user_id == db.t_Personal.f_usuario).select(db.t_Personal.ALL)[0].f_dependencia

            dependencia = db(idDependencia == db.dependencias.id).select(db.dependencias.ALL)[0]

            jefe_dependencia = db(dependencia.id_jefe_dependencia == db.auth_user.id).select(db.auth_user.ALL)[0]

            assert(jefe_dependencia != None)
            
        except:

            return redirect(URL('listado'))

        nombre_y_apellido = "%s %s" % (jefe_dependencia.first_name, jefe_dependencia.last_name)

        nombre_anade = "%s %s" % (auth.user.first_name, auth.user.last_name)

        correo = '<html><head><meta charset="UTF-8"></head><body><table><tr><td><p>Hola, %s.</p><br><p>Se ha editado un servicio. La operación fue realizada por %s, el/la cual pertenece a la dependencia de %s.</p><br><p>Para consultar dicha operación diríjase a la página web <a href="159.90.171.24">SIGULAB</a></p></td></tr></table></body></html>' % (nombre_y_apellido, nombre_anade, dependencia.nombre)

        asunto = '[SIGULAB] ' + 'Se ha editado un servicio'

        __enviar_correo(jefe_dependencia.email, asunto, correo)

        return redirect(URL(args=request.args, vars=request.get_vars, host=True)) 


    #----- FIN EDITAR SERVICIO -----#

    #----- COMIENZO EDITAR SERVICIO -----#

    if request.post_vars.edit and (request.post_vars.eliminar is None) and (request.post_vars.visibilidad is None):
        editar = db(db.servicios.id == request.vars.idFicha).select(db.servicios.ALL)
        
    else:
        editar = []

    #----- FIN COMIENZO EDITAR SERVICIO -----#

    #----- EDITAR VISIBILIDAD -----#

    if request.post_vars.visibilidad:
        db(db.servicios.id == request.post_vars.idFicha).update(
            visibilidad=eval(request.post_vars.visibilidad))

        if request.post_vars.visibilidad == True:
            estado_visibilidad = "mostrar"
        else:
            estado_visibilidad = "ocultar"

        # Se envia el email de notificacion al ocultar/mostrar un servicio 

        idDependencia = db(auth.user_id == db.t_Personal.f_usuario).select(db.t_Personal.ALL)[0].f_dependencia

        dependencia = db(idDependencia == db.dependencias.id).select(db.dependencias.ALL)[0]

        jefe_dependencia = db(dependencia.id_jefe_dependencia == db.auth_user.id).select(db.auth_user.ALL)[0]
            
        nombre_y_apellido = "%s %s" % (jefe_dependencia.first_name, jefe_dependencia.last_name)

        nombre_anade = "%s %s" % (auth.user.first_name, auth.user.last_name)

        correo = '<html><head><meta charset="UTF-8"></head><body><table><tr><td><p>Hola, %s.</p><br><p>Se ha modificado la visibilidad de un servicio a %s. La operación fue realizada por %s, el/la cual pertenece a la dependencia de %s.</p><br><p>Para consultar dicha operación diríjase a la página web <a href="159.90.171.24">SIGULAB</a></p></td></tr></table></body></html>' % (nombre_y_apellido, estado_visibilidad, nombre_anade, dependencia.nombre)

        asunto = '[SIGULAB] ' + 'Se ha modificado la visibilidad de un servicio'

        __enviar_correo(jefe_dependencia.email, asunto, correo)

        return redirect(URL(args=request.args, vars=request.get_vars, host=True)) 


    #----- FIN EDITAR VISIBILIDAD -----#

    #----- ELIMINAR SERVICIO -----#

    if request.post_vars.eliminar:
        db(db.servicios.id == request.post_vars.idFicha).delete()

        # Se envia el email de notificacion al eliminar un servicio 

        idDependencia = db(auth.user_id == db.t_Personal.f_usuario).select(db.t_Personal.ALL)[0].f_dependencia

        dependencia = db(idDependencia == db.dependencias.id).select(db.dependencias.ALL)[0]

        jefe_dependencia = db(dependencia.id_jefe_dependencia == db.auth_user.id).select(db.auth_user.ALL)[0]
            

        nombre_y_apellido = "%s %s" % (jefe_dependencia.first_name, jefe_dependencia.last_name)

        nombre_anade = "%s %s" % (auth.user.first_name, auth.user.last_name)

        correo = '<html><head><meta charset="UTF-8"></head><body><table><tr><td><p>Hola, %s.</p><br><p>Se ha eliminado un servicio. La operación fue realizada por %s, el/la cual pertenece a la dependencia de %s.</p><br><p>Para consultar dicha operación diríjase a la página web <a href="159.90.171.24">SIGULAB</a></p></td></tr></table></body></html>' % (nombre_y_apellido, nombre_anade, dependencia.nombre)

        asunto = '[SIGULAB] ' + 'Se ha eliminado un servicio'

        __enviar_correo(jefe_dependencia.email, asunto, correo)

        return redirect(URL(args=request.args, vars=request.get_vars, host=True))     

    #----- FIN ELIMINAR SERVICIO -----#

    #----- SOLICITAR SERVICIO -----#

    if request.post_vars.solicitar:
        redirect(URL('solicitudes', vars=dict(idServicio=request.post_vars.solicitar)))

    #----- FIN SOLICITAR SERVICIO -----#

    listado_de_servicios = ListaServicios(db, __obtener_jerarquia()[1], 
        __obtener_jerarquia()[0])

    return dict(servicios=listado_de_servicios.filas,
                rol=__obtener_jerarquia()[0],
                categorias=listar_categorias(db),
                tipos=listar_tipos(db),
                sedes=listar_sedes(db), 
                editar=editar)

#----- GESTIONAR SOLICITUDES -----#
@auth.requires_login(otherwise=URL('modulos', 'login'))
def solicitudes():


    servicio_solicitud = None

    #----- AGREGAR SOLICITUDES -----#
    if request.post_vars.numRegistro:

        id_responsable = db(auth.user_id == db.t_Personal.f_usuario).select(db.t_Personal.ALL)[0].id

        solicitud_nueva = Solicitud(db, auth, request.post_vars.numRegistro, id_responsable,
            request.now, request.post_vars.nombreServicio, request.post_vars.propositoServicio,
            request.post_vars.propositoDescripcion, None, request.post_vars.descripcionSolicitud, "", 0)

        solicitud_nueva.insertar()

        # ENVIAR CORREO AL RESPONSABLE DE LA SOLICITUD Y AL JEFE DE LA DEPENDENCIA PARA NOTIFICARLE QUE SE HIZO UNA SOLICITUD
        solicitud_nueva.correoHacerSolicitud()

        return redirect(URL(args=request.args, vars=request.get_vars, host=True)) 

    #----- FIN DE AGREGAR SOLICITUDES -----#

    #----- AGREGAR SOLICITUD DESDE SERVICIO -----#
    if request.post_vars.idServicio:
        servicio_solicitud = Servicio(db)
        servicio_solicitud.instanciar(int(request.vars.idServicio))

    #----- FIN AGREGAR SOLICITUD DESDE SERVICIO -----#

    #----- CAMBIO DE ESTADO DE SOLICITUD -----#
    if request.post_vars.idFicha:
        solicitud_a_cambiar = Solicitud(db, auth)
        solicitud_a_cambiar.instanciar(int(request.post_vars.idFicha))
        solicitud_a_cambiar.cambiar_estado(int(request.post_vars.estado), request)
        solicitud_a_cambiar.actualizar(int(request.post_vars.idFicha))

        # ENVIAR CORREO A SOLICITANTE PARA AVISAR EL CAMBIO DE ESTADO DE SU SOLICITUD
        solicitud_a_cambiar.correoCambioEstadoSolicitud()
        solicitud_a_cambiar.correoSolicitudFinalizada()

        # if request.post_vars.estado == "1":
        #     solicitud_a_cambiar.fecha_aprobacion = request.now
        #     solicitud_a_cambiar.aprobada_por = auth.user.first_name
        #     solicitud_a_cambiar.actualizar(request.post_vars.idFicha)

        if request.post_vars.estado == "2":
            solicitud_a_cambiar.observaciones = request.post_vars.observaciones
            # solicitud_a_cambiar.elaborada_por = auth.user.first_name
            # solicitud_a_cambiar.fecha_elaboracion = request.now
            solicitud_a_cambiar.actualizar(request.post_vars.idFicha)

            # TODO Quitar la solicitud de la lista de solicitudes luego de que pase a certificarse

            #solicitud_a_cambiar.elaborar_certificacion()

        # if request.post_vars.estado == "-1":
        #     solicitud_a_cambiar.eliminar(int(request.post_vars.idFicha))

        return redirect(URL(args=request.args, vars=request.get_vars, host=True)) 

    #----- FIN DE CAMBIO DE ESTADO DE SOLICITUD -----#

    #----- ELIMINAR SOLICITUD -----#

    if request.post_vars.eliminar:
        id_a_eliminar = int(request.post_vars.idFicha_eliminar)
        db(id_a_eliminar == db.solicitudes.id).delete()

        return redirect(URL(args=request.args, vars=request.get_vars, host=True)) 

    #----- FIN DE ELIMINAR SOLICITUD -----#

    #----- DATOS DE SOLICITANTE -----#
    personal_usuario = db(auth.user_id == db.t_Personal.f_usuario).select(db.t_Personal.ALL)[0]

    dependencia_usuario = db(personal_usuario.f_dependencia == db.dependencias.id).select(db.dependencias.ALL)[0]

    if auth.has_membership(group_id="CLIENTE INTERNO"):
        registro = "FUSB"
    else:
        registro = dependencia_usuario.codigo_registro

    num_registro = validador_registro_solicitudes(request, db, registro)

    nombre_dependencia = dependencia_usuario.nombre

    id_jefe_dependencia = dependencia_usuario.id_jefe_dependencia

    usuario_jefe = db(id_jefe_dependencia == db.auth_user.id).select(db.auth_user.ALL)[0]

    nombre_jefe = usuario_jefe.first_name
    apellido_jefe = usuario_jefe.last_name
    email_jefe = usuario_jefe.email

    nombre_responsable = personal_usuario.f_nombre
    email_responsable = personal_usuario.f_email

    datos_solicitud = [nombre_dependencia, nombre_jefe, apellido_jefe, email_jefe, nombre_responsable, email_responsable, num_registro]

    #----- GENERACION DE LISTADOS -----#
    listado_de_solicitudes_generadas = ListaSolicitudes(db, auth, "Solicitante")

    listado_de_solicitudes_recibidas = ListaSolicitudes(db, auth, "Ejecutante")


    return dict(solicitudes_generadas=listado_de_solicitudes_generadas.filas,  
        solicitudes_recibidas=listado_de_solicitudes_recibidas.filas, datos_solicitud=datos_solicitud,
        categorias=listar_categorias(db), tipos=listar_tipos(db), servicio_solicitud=servicio_solicitud)

# ---- GESTIONAR CERTIFICACIONES ---- #
@auth.requires_login(otherwise=URL('modulos', 'login'))
def certificaciones():

    # ---- ACCION DE CERTIFICACION DEL SERVICIO ----
    if request.post_vars.registro:

        registro = request.post_vars.registro
        proyecto = request.post_vars.proyecto
        elaborado_por = request.post_vars.usuarioid
        dependencia = request.post_vars.dependenciaid
        solicitud = request.post_vars.solicitudid

        solicitud_a_actualizar = Solicitud(db,auth)
        solicitud_a_actualizar.instanciar(int(solicitud))
        solicitud_a_actualizar.certificar(request)
        solicitud_a_actualizar.correoCertificacionFinalizada()

        fecha = request.post_vars.fecha

        solicitud_a_actualizar.guardar_en_historial()

    #-------------------FIN------------------------

    #----- GENERACION DE LISTADOS -----#

    listado_de_certificaciones_a_generar = ListaSolicitudes(db, auth, "Certificante")

    listado_de_certificaciones_a_recibir = ListaSolicitudes(db, auth, "Ejecutante")

  
    return dict(certificaciones_a_generar=listado_de_certificaciones_a_generar.filas,
                certificaciones_a_recibir=listado_de_certificaciones_a_recibir.filas,
                categorias=listar_categorias(db), tipos=listar_tipos(db), sedes=listar_sedes(db))

# ---- GESTIONAR HISTORIAL ---- #
@auth.requires_login(otherwise=URL('modulos', 'login'))
def historial():
    listado_de_solicitudes = ListaHistorial(db, auth, "Certificante")
    
    return dict(listado_de_solicitudes=listado_de_solicitudes.filas)

def detallesServicios():

    nombre_categoria = ""

    listado_de_servicios_catalogo = ListaServicios(db, False, None, None)
    if request.vars.categoria:
        categoria = int(request.vars.categoria)
        servicios_mostrar_catalogo = listado_de_servicios_catalogo.catalogo(categoria)

    if categoria == 1:
        nombre_categoria = "Alimentos"
    elif categoria == 2: 
        nombre_categoria = "Ambiente"
    elif categoria == 3:
        nombre_categoria = "Biología"
    elif categoria == 4: 
        nombre_categoria = "Energía"
    elif categoria == 5: 
        nombre_categoria = "Manufactura, Instrumentación y Control"
    elif categoria == 6:
        nombre_categoria = "Matemáticas y Estadísticas"
    elif categoria == 7: 
        nombre_categoria = "Mecánica y Materiales"
    elif categoria == 8: 
        nombre_categoria = "Química"
    elif categoria == 9:
        nombre_categoria = "Física"
    elif categoria == 10: 
        nombre_categoria = "Informática, Computación, Comunicación e Información"
    elif categoria == 11: 
        nombre_categoria = "Música"
    elif categoria == 12:
        nombre_categoria = "Salud"
    elif categoria == 13:
        nombre_categoria = "Otros"

    return dict(nombre_categoria=nombre_categoria, ensayo=servicios_mostrar_catalogo[0], inspeccion=servicios_mostrar_catalogo[1], calibracion=servicios_mostrar_catalogo[2], 
        desarrollo_prototipo_piezas=servicios_mostrar_catalogo[3], consultoria_asesoria=servicios_mostrar_catalogo[4],
        formacion_capacitacion_transferencia=servicios_mostrar_catalogo[5], sala_computadoras=servicios_mostrar_catalogo[6], 
        sala_videos=servicios_mostrar_catalogo[7], verificacion=servicios_mostrar_catalogo[8])

def catalogoServicios():
    return dict()

#------------------------------------------------------------------------------
#
# Controladores de los Ajax del modulo de Servicios
#
#------------------------------------------------------------------------------

@auth.requires_login(otherwise=URL('modulos', 'login'))
def ajax_ficha_servicio():
  
    session.forget(response)

    # Servicio
    entrada = db(db.servicios.id == int(request.vars.serv)).select(db.servicios.ALL)

    # Funciones
    funcion = []
    if entrada[0].gestion:
        funcion.append("Gestión  ")
    else:
        funcion.append("")

    if entrada[0].docencia:
        funcion.append("Docencia  ")
    else:
        funcion.append("")

    if entrada[0].investigacion:
        funcion.append("Investigación  ")
    else:
        funcion.append("")

    if entrada[0].extension:
        funcion.append("Extensión  ")
    else:
        funcion.append("")

    producto = ""
    if entrada[0].entregaResultados:
        producto = producto + "Entrega de Resultados, "
    if entrada[0].ensayoCalibracion:
        producto = producto + "Informe de ensayo o calibración, "
    if entrada[0].certificadoConformidadProducto:
        producto = producto + "Certificado de conformidad del producto (ensayado o calibrado), "
    if entrada[0].certificadoCalibracion:
        producto = producto + "Certificado de calibración, "
    if entrada[0].otro:
        producto = producto + "Otro"

    if len(producto) > 0 and producto[-1] == ' ' and producto[-2] == ',':
        # El producto no termino con "Otro". Debemos eliminar el espacio y la coma
        producto = producto.rstrip(', ')

    valores_de_ficha = query_ficha(db, int(request.vars.serv))
    valores_de_ficha['funcion'] = funcion
    valores_de_ficha['producto'] = producto

    valores_de_ficha['ambito_in_situ'] = entrada[0].ambito_in_situ
    valores_de_ficha['ambito_en_campo'] = entrada[0].ambito_en_campo
    valores_de_ficha['ambito_otro'] = entrada[0].ambito_otro
    valores_de_ficha['ambito_otro_detalle'] = entrada[0].ambito_otro_detalle

    valores_de_ficha['per_tecnico'] = entrada[0].per_tecnico
    valores_de_ficha['per_supervisor'] = entrada[0].per_supervisor
    valores_de_ficha['per_tesista'] = entrada[0].per_tesista
    valores_de_ficha['per_pasante'] = entrada[0].per_pasante
    valores_de_ficha['per_preparador'] = entrada[0].per_preparador
    valores_de_ficha['per_obrero'] = entrada[0].per_obrero
    valores_de_ficha['per_otro'] = entrada[0].per_otro
    valores_de_ficha['per_otro_detalle'] = entrada[0].per_otro_detalle

    valores_de_ficha['condicion_ambiental'] = entrada[0].condicion_ambiental
    valores_de_ficha['condicion_ambiental_detalle'] = entrada[0].condicion_ambiental_detalle

    edicion = False
    privilegios = __obtener_priviliegios()
    rol = privilegios[0]
    dependencia = privilegios[1]

    if rol == 2:
        edicion = True

    elif rol == 1:
        if int(dependencia) != int(entrada[0].dependencia):
            secciones = []
            dep = db(db.dependencias.unidad_de_adscripcion == dependencia).select(db.dependencias.id)

            for d in dep:
                secciones.append(int(d.id))
            if entrada[0].dependencia in secciones:
                edicion = True
        else:
            edicion = True

    return dict(ficha=valores_de_ficha, edicion = edicion)

def ajax_ficha_servicio_catalogo():
    session.forget(response)

    # Servicio
    entrada = db(db.servicios.id == int(request.vars.servicio)).select(db.servicios.ALL)

    # Funciones
    funcion = []
    if entrada[0].gestion:
        funcion.append("Gestión  ")
    else:
        funcion.append("")

    if entrada[0].docencia:
        funcion.append("Docencia  ")
    else:
        funcion.append("")

    if entrada[0].investigacion:
        funcion.append("Investigación  ")
    else:
        funcion.append("")

    if entrada[0].extension:
        funcion.append("Extensión  ")
    else:
        funcion.append("")

    producto = ""
    if entrada[0].entregaResultados:
        producto = producto + "Entrega de Resultados, "
    if entrada[0].ensayoCalibracion:
        producto = producto + "Informe de ensayo o calibración, "
    if entrada[0].certificadoConformidadProducto:
        producto = producto + "Certificado de conformidad del producto (ensayado o calibrado), "
    if entrada[0].certificadoCalibracion:
        producto = producto + "Certificado de calibración, "
    if entrada[0].otro:
        producto = producto + "Otro"

    if len(producto) > 0 and producto[-1] == ' ' and producto[-2] == ',':
        # El producto no termino con "Otro". Debemos eliminar el espacio y la coma
        producto = producto.rstrip(', ')

    valores_de_ficha = query_ficha(db, int(request.vars.servicio))
    valores_de_ficha['funcion'] = funcion
    valores_de_ficha['producto'] = producto

    return dict(ficha=valores_de_ficha)

@auth.requires_login(otherwise=URL('modulos', 'login'))
def ajax_ficha_solicitud():
    session.forget(response)
    # Solicitud
    solicitud = Solicitud(db, auth)

    solicitud.instanciar(int(request.vars.solicitud))

    return dict(ficha = solicitud, tipo_solicitud = request.vars.tipoSolicitud)

@auth.requires_login(otherwise=URL('modulos', 'login'))
def ajax_ficha_certificacion():
    session.forget(response)
    # Solicitud
    solicitud = Solicitud(db, auth)

    solicitud.instanciar(int(request.vars.solicitud))

    return dict(ficha = solicitud, tipo_solicitud = request.vars.tipo_solicitud)

@auth.requires_login(otherwise=URL('modulos', 'login'))
def ajax_ficha_historial():
    session.forget(response)
    # Solicitud
    solicitud = Historial(db, auth)

    solicitud.instanciar(int(request.vars.solicitud))

    solicitud.generacion_pdf()

    return dict(ficha = solicitud, tipo_solicitud = request.vars.tipoSolicitud)

@auth.requires_login(otherwise=URL('modulos', 'login'))
def ajax_obtener_adscripcion():
    session.forget(response)
    adscripcion_query = db((db.dependencias.id_sede == int(request.vars.sede))).select(db.dependencias.ALL)
    dependencias_a_mostrar = []

    for l in adscripcion_query:
        if re.match( r'LABORATORIO\s[A-G]', l.nombre) or (l.id == 1):
            dependencias_a_mostrar.append(l)
    return dict(dependencias=dependencias_a_mostrar)

@auth.requires_login(otherwise=URL('modulos', 'login'))
def ajax_obtener_dependencia():
    session.forget(response)
    dependencia_query = db((db.dependencias.unidad_de_adscripcion == int(request.vars.adscripcion))).select(db.dependencias.ALL)
    dependencias_a_mostrar = []

    for l in dependencia_query:
        if (re.match( r'LABORATORIO\s[A-G]', l.nombre)) == None:
            dependencias_a_mostrar.append(l)
    return dict(dependencias=dependencias_a_mostrar)

@auth.requires_login(otherwise=URL('modulos', 'login'))
def ajax_obtener_ubicacion():
    session.forget(response)
    ubicacion_query = db((db.espacios_fisicos.dependencia == int(request.vars.dependencia))).select(db.espacios_fisicos.ALL)
    ubicaciones_a_mostrar = []

    for l in ubicacion_query:
        ubicaciones_a_mostrar.append(l)
    return dict(ubicaciones=ubicaciones_a_mostrar)

@auth.requires_login(otherwise=URL('modulos', 'login'))
def ajax_obtener_responsable():
    session.forget(response)
    responsable_query = db((db.t_Personal.f_dependencia == int(request.vars.dependencia))).select(db.t_Personal.ALL)
    responsables_a_mostrar = []

    for l in responsable_query:
        responsables_a_mostrar.append(l)
    return dict(responsables=responsables_a_mostrar)

@auth.requires_login(otherwise=URL('modulos', 'login'))
def ajax_obtener_adscripcion_editar():
    session.forget(response)
    adscripcion_query = db((db.dependencias.id_sede == int(request.vars.sede))).select(db.dependencias.ALL)
    dependencias_a_mostrar = []

    for l in adscripcion_query:
        if re.match( r'LABORATORIO\s[A-G]', l.nombre) or (l.id == 1):
            dependencias_a_mostrar.append(l)
    return dict(dependencias=dependencias_a_mostrar)

@auth.requires_login(otherwise=URL('modulos', 'login'))
def ajax_obtener_dependencia_editar():
    session.forget(response)
    dependencia_query = db((db.dependencias.unidad_de_adscripcion == int(request.vars.adscripcion))).select(db.dependencias.ALL)
    dependencias_a_mostrar = []

    for l in dependencia_query:
        if (re.match( r'LABORATORIO\s[A-G]', l.nombre)) == None:
            dependencias_a_mostrar.append(l)
    return dict(dependencias=dependencias_a_mostrar)

@auth.requires_login(otherwise=URL('modulos', 'login'))
def ajax_obtener_ubicacion_editar():
    session.forget(response)
    ubicacion_query = db((db.espacios_fisicos.dependencia == int(request.vars.dependencia))).select(db.espacios_fisicos.ALL)
    ubicaciones_a_mostrar = []
    for l in ubicacion_query:
        ubicaciones_a_mostrar.append(l)
    return dict(ubicaciones=ubicaciones_a_mostrar)

@auth.requires_login(otherwise=URL('modulos', 'login'))
def ajax_obtener_responsable_editar():
    session.forget(response)
    responsable_query = db((db.t_Personal.f_dependencia == int(request.vars.dependencia))).select(db.t_Personal.ALL)
    responsables_a_mostrar = []

    for l in responsable_query:
        responsables_a_mostrar.append(l)
    return dict(responsables=responsables_a_mostrar)

@auth.requires_login(otherwise=URL('modulos', 'login'))
def ajax_obtener_nombre_servicio():
    session.forget(response)
    servicio_query = db((db.servicios.tipo == int(request.vars.tipo))&(db.servicios.categoria == int(request.vars.categoria))&(db.servicios.visibilidad == True)).select(db.servicios.ALL)

    servicios_a_mostrar = []
    for servicio in servicio_query:
        servicios_a_mostrar.append(servicio)

    return dict(servicios=servicios_a_mostrar)

@auth.requires_login(otherwise=URL('modulos', 'login'))
def ajax_obtener_proposito_servicio():
    session.forget(response)

    servicio = db(db.servicios.id == int(request.vars.idServicio)).select(db.servicios.ALL)[0]

    propositos_a_mostrar = []

    if servicio.docencia == True:
        propositoServicio = db("Docencia" == db.propositos.tipo).select(db.propositos.ALL)[0] 
        propositos_a_mostrar.append(propositoServicio)

    if servicio.investigacion == True:
        propositoServicio = db("Investigación" == db.propositos.tipo).select(db.propositos.ALL)[0]
        propositos_a_mostrar.append(propositoServicio)

    if servicio.extension == True:
        propositoServicio = db("Extensión" == db.propositos.tipo).select(db.propositos.ALL)[0]
        propositos_a_mostrar.append(propositoServicio)    

    if servicio.gestion == True:
        propositoServicio = db("Gestión" == db.propositos.tipo).select(db.propositos.ALL)[0]
        propositos_a_mostrar.append(propositoServicio)

    return dict(propositos=propositos_a_mostrar)

@auth.requires_login(otherwise=URL('modulos', 'login'))
def ajax_obtener_datos_depen_ejecutora():
    session.forget(response)

    servicio = db(db.servicios.id == int(request.vars.idServicio2)).select(db.servicios.ALL)[0]
    dependencia_ejecutora = db(db.dependencias.id == servicio.dependencia).select(db.dependencias.ALL)[0]

    jefe_dependencia_ejecutora = db(db.auth_user.id == dependencia_ejecutora.id_jefe_dependencia).select(db.auth_user.ALL)[0]

    datos_jefe_depen_ejecutora = [jefe_dependencia_ejecutora.first_name, jefe_dependencia_ejecutora.last_name, jefe_dependencia_ejecutora.email]

    unidad_de_adscripcion = db(db.dependencias.id == dependencia_ejecutora.unidad_de_adscripcion).select(db.dependencias.nombre)[0].nombre

    return dict(nombreDepenEjecutora= dependencia_ejecutora.nombre, jefeDepenEjecutora = datos_jefe_depen_ejecutora, unidad_de_adscripcion = unidad_de_adscripcion)

@auth.requires_login(otherwise=URL('modulos', 'login'))
def ajax_certificar_servicio():
    solicitudesid = int(request.post_vars.solicitud)
    solicitud_info = db(db.solicitudes.id == solicitudesid).select()[0]
    usuario = db(db.t_Personal.f_usuario == auth.user_id).select()[0]
    servicio = db(db.servicios.id == solicitud_info.id_servicio_solicitud).select()[0]
    responsable = db(db.t_Personal.id == servicio.responsable).select()[0]
    fecha = request.now
    dependencia = db(auth.user_id == db.auth_membership.user_id).select()[0].dependencia_asociada

    proyecto = "N/A"
    proposito = db(solicitud_info.proposito == db.propositos.id).select()[0].tipo

    if not(dependencia is None):
        dependencianombre = db(db.dependencias.id == dependencia).select()[0].nombre
    else:
        dependencia = db(db.dependencias.id > 0).select()[0].id
        dependencianombre = db(db.dependencias.id == dependencia).select()[0].nombre

    registro = solicitud_info.registro


    return dict(solicitud=solicitud_info,
                usuario=usuario,
                servicio=servicio,
                responsable=responsable,
                fecha=fecha,
                registro=registro,
                dependenciaid=dependencia,
                dependencia=dependencianombre,
                proyecto=proyecto)

#------------------------------------------------------------------------------
#
# Ajax de Listados
#
#------------------------------------------------------------------------------

# Servicios

@auth.requires_login(otherwise=URL('modulos', 'login'))
def ajax_listado_servicios():

    #----- LISTAR SERVICIOS -----#

    # Conseguir dependencia y si su rol es suficiente para ver servicios ocultos

    grupo_lab = db(db.auth_group.role == "JEFE DE LABORATORIO").select(db.auth_group.id)[0].id
    grupo_dir = db(db.auth_group.role == "DIRECTOR").select(db.auth_group.id)[0].id
    grupo_asistdir = db(db.auth_group.role == "ASISTENTE DEL DIRECTOR").select(db.auth_group.id)[0].id
    grupo_admin = db(db.auth_group.role == "WEBMASTER").select(db.auth_group.id)[0].id

    info_membership = db(db.auth_membership.user_id == auth.user_id).select()[0]
    user_group_id = info_membership.group_id

    dependencia = info_membership.dependencia_asociada

    rol = 0
    if user_group_id == grupo_dir or user_group_id == grupo_asistdir or user_group_id == grupo_admin or auth.user.email == "ulab-calidad@usb.ve":
        rol = 2
    elif user_group_id == grupo_lab:
        rol = 1

    listado_de_servicios = ListaServicios(db, dependencia, rol)

    order_by_asc = eval(request.post_vars.ordenarAlfabeticamente.title())
    order_by_col = request.post_vars.ordenarPor

    listado_de_servicios.cambiar_ordenamiento(order_by_asc)
    listado_de_servicios.cambiar_columna(order_by_col)

    if request.post_vars.cambiarPagina:
        listado_de_servicios.cambiar_pagina(int(request.post_vars.cambiarPagina))

    listado_de_servicios.orden_y_filtrado()

    firstpage=listado_de_servicios.boton_principio
    lastpage=listado_de_servicios.boton_fin
    nextpage=listado_de_servicios.boton_siguiente
    prevpage=listado_de_servicios.boton_anterior

    #----- FIN LISTAR SERVICIOS -----#
    return dict(grid=listado_de_servicios.servicios_a_mostrar,
                pages=listado_de_servicios.rango_paginas,
                actualpage=listado_de_servicios.pagina_central,
                nextpage=nextpage, prevpage=prevpage,
                firstpage=firstpage, lastpage=lastpage, rol=rol)

# Solicitudes Generadas

@auth.requires_login(otherwise=URL('modulos', 'login'))
def ajax_listado_solicitudes_generadas():

    #----- LISTAR SOLICITUDES -----#
    listado_de_solicitudes = ListaSolicitudes(db, auth, "Solicitante")

    order_by_asc = eval(request.post_vars.ordenar_solicitudes_generadas_alfabeticamente.title())
    order_by_col = request.post_vars.ordenar_solicitudes_generadas_por

    listado_de_solicitudes.cambiar_ordenamiento(order_by_asc)
    listado_de_solicitudes.cambiar_columna(order_by_col)

    if request.post_vars.cambiar_pagina_solicitudes_generadas:
        listado_de_solicitudes.cambiar_pagina(int(request.post_vars.cambiar_pagina_solicitudes_generadas))

    listado_de_solicitudes.orden_y_filtrado()
    firstpage=listado_de_solicitudes.boton_principio
    lastpage=listado_de_solicitudes.boton_fin
    nextpage=listado_de_solicitudes.boton_siguiente
    prevpage=listado_de_solicitudes.boton_anterior

    #----- FIN LISTAR SERVICIOS -----#
    return dict(grid=listado_de_solicitudes.solicitudes_a_mostrar,
                pages=listado_de_solicitudes.rango_paginas,
                actualpage=listado_de_solicitudes.pagina_central,
                nextpage=nextpage, prevpage=prevpage,
                firstpage=firstpage, lastpage=lastpage)

# Solicitudes Recibidas

@auth.requires_login(otherwise=URL('modulos', 'login'))
def ajax_listado_solicitudes_recibidas():

    #----- LISTAR SOLICITUDES -----#
    listado_de_solicitudes = ListaSolicitudes(db, auth, "Ejecutante")

    order_by_asc = eval(request.post_vars.ordenar_solicitudes_recibidas_alfabeticamente.title())
    order_by_col = request.post_vars.ordenar_solicitudes_recibidas_por

    listado_de_solicitudes.cambiar_ordenamiento(order_by_asc)
    listado_de_solicitudes.cambiar_columna(order_by_col)

    if request.post_vars.cambiar_pagina_solicitudes_recibidas:
        listado_de_solicitudes.cambiar_pagina(int(request.post_vars.cambiar_pagina_solicitudes_recibidas))

    listado_de_solicitudes.orden_y_filtrado()
    firstpage=listado_de_solicitudes.boton_principio
    lastpage=listado_de_solicitudes.boton_fin
    nextpage=listado_de_solicitudes.boton_siguiente
    prevpage=listado_de_solicitudes.boton_anterior

    #----- FIN LISTAR SERVICIOS -----#
    return dict(grid=listado_de_solicitudes.solicitudes_a_mostrar,
                pages=listado_de_solicitudes.rango_paginas,
                actualpage=listado_de_solicitudes.pagina_central,
                nextpage=nextpage, prevpage=prevpage,
                firstpage=firstpage, lastpage=lastpage)

@auth.requires_login(otherwise=URL('modulos', 'login'))
def ajax_listado_certificaciones_a_generar():

    #------ ACCION LISTAR CERTIFICACIONES A GENERAR -----#
    listado_de_certificaciones_a_generar = ListaSolicitudes(db, auth, "Certificante")

    order_by_asc = eval(request.post_vars.ordenar_certificaciones_a_generar_alfabeticamente.title())
    order_by_col = request.post_vars.ordenar_certificaciones_a_generar_por

    listado_de_certificaciones_a_generar.cambiar_ordenamiento(order_by_asc)
    listado_de_certificaciones_a_generar.cambiar_columna(order_by_col)

    if request.post_vars.cambiar_pagina_certificaciones_a_generar:
        listado_de_certificaciones_a_generar.cambiar_pagina(int(request.post_vars.cambiar_pagina_certificaciones_a_generar))

    listado_de_certificaciones_a_generar.orden_y_filtrado()

    firstpage=listado_de_certificaciones_a_generar.boton_principio
    lastpage=listado_de_certificaciones_a_generar.boton_fin
    nextpage=listado_de_certificaciones_a_generar.boton_siguiente
    prevpage=listado_de_certificaciones_a_generar.boton_anterior

    return dict(grid=listado_de_certificaciones_a_generar.solicitudes_a_mostrar, pages=listado_de_certificaciones_a_generar.rango_paginas, actualpage=listado_de_certificaciones_a_generar.pagina_central, nextpage=nextpage, prevpage=prevpage, firstpage=firstpage, lastpage=lastpage)


@auth.requires_login(otherwise=URL('modulos', 'login'))
def ajax_listado_certificaciones_a_recibir():
  #------ ACCION LISTAR SOLICITUDES DE SERV -----
    listado_de_certificaciones_a_recibir = ListaSolicitudes(db, auth, "Ejecutante")

    order_by_asc = eval(request.post_vars.ordenar_certificaciones_a_recibir_alfabeticamente.title())
    order_by_col = request.post_vars.ordenar_certificaciones_a_recibir_por

    listado_de_certificaciones_a_recibir.cambiar_ordenamiento(order_by_asc)
    listado_de_certificaciones_a_recibir.cambiar_columna(order_by_col)

    if request.post_vars.cambiar_pagina_certificaciones_a_recibir:
        listado_de_certificaciones_a_recibir.cambiar_pagina(int(request.post_vars.cambiar_pagina_certificaciones_a_recibir))

    listado_de_certificaciones_a_recibir.orden_y_filtrado()

    firstpage=listado_de_certificaciones_a_recibir.boton_principio
    lastpage=listado_de_certificaciones_a_recibir.boton_fin
    nextpage=listado_de_certificaciones_a_recibir.boton_siguiente
    prevpage=listado_de_certificaciones_a_recibir.boton_anterior

    return dict(grid=listado_de_certificaciones_a_recibir.solicitudes_a_mostrar,
                pages=listado_de_certificaciones_a_recibir.rango_paginas,
                actualpage=listado_de_certificaciones_a_recibir.pagina_central,
                nextpage=nextpage, prevpage=prevpage,
                firstpage=firstpage, lastpage=lastpage)


@auth.requires_login(otherwise=URL('modulos', 'login'))
def ajax_listado_historial():

    #------ ACCION LISTAR SOLICITUDES DE SERV -----
    listado_de_solicitudes = ListaHistorial(db, auth, "Certificante")

    order_by_asc = eval(request.post_vars.ordenarAlfabeticamente.title())
    order_by_col = request.post_vars.ordenarPor

    listado_de_solicitudes.cambiar_ordenamiento(order_by_asc)
    listado_de_solicitudes.cambiar_columna(order_by_col)

    if request.post_vars.cambiarPagina:
        listado_de_solicitudes.cambiar_pagina(int(request.post_vars.cambiarPagina))

    listado_de_solicitudes.orden_y_filtrado()

    firstpage=listado_de_solicitudes.boton_principio
    lastpage=listado_de_solicitudes.boton_fin
    nextpage=listado_de_solicitudes.boton_siguiente
    prevpage=listado_de_solicitudes.boton_anterior

    # ----- FIN LISTAR SOLICITUDES -----#
    return dict(grid=listado_de_solicitudes.solicitudes_a_mostrar,
                pages=listado_de_solicitudes.rango_paginas,
                actualpage=listado_de_solicitudes.pagina_central,
                nextpage=nextpage, prevpage=prevpage,
                firstpage=firstpage, lastpage=lastpage)


# Certificaciones de Terceros

# Certificaciones Personales

# Historial de Servicios Ejecutados/Certificados

#------------------------------------------------------------------------------
#
# Controladores de los Reportes a Imprimir
#
#------------------------------------------------------------------------------

@auth.requires_login(otherwise=URL('modulos', 'login'))
def pdf_solicitud():
    session.forget(response)
    # Solicitud
    if request.vars.solicitud:
        solicitud = Solicitud(db, auth)

        try:
            solicitud.instanciar(int(request.vars.solicitud))
        except:
            solicitud.instanciar(0)

    elif request.vars.historial:
        solicitud = Historial(db, auth)

        try:
            solicitud.instanciar(int(request.vars.historial))
        except:
            solicitud.instanciar(0)

        solicitud.generacion_pdf()



    return dict(solicitud = solicitud)



@auth.requires_login(otherwise=URL('modulos', 'login'))
def pdf_certificado():
    session.forget(response)
    # Certificacion
    if request.vars.solicitud:
        solicitud = Historial(db, auth)

        try:
            solicitud.instanciar(int(request.vars.solicitud))
        except:
            solicitud.instanciar(0)

        solicitud.generacion_pdf()

    return dict(solicitud = solicitud)

# Funcion para enviar un correo de notificacion 
def __enviar_correo(destinatario, asunto, cuerpo):
    mail = auth.settings.mailer
    mail.settings.sender = 'sat-laba@usb.ve'
    mail.send(destinatario, asunto, cuerpo)


def __queries_enviar_correo():

    # OJO: QUITAR EL TRY EXCEPT 

    idDependencia = db(auth.user_id == db.t_Personal.f_usuario).select(db.t_Personal.ALL)[0].f_dependencia

    dependencia = db(idDependencia == db.dependencias.id).select(db.dependencias.ALL)[0]

    jefe_dependencia = db(dependencia.id_jefe_dependencia == db.auth_user.id).select(db.auth_user.ALL)[0]
        
    nombre_y_apellido = "%s %s" % (jefe_dependencia.first_name, jefe_dependencia.last_name)

    nombre_anade = "%s %s" % (auth.user.first_name, auth.user.last_name)

    return [nombre_y_apellido, nombre_anade, dependencia, jefe_dependencia]

def __obtener_priviliegios():
    # Obtener Privilegios del usuario (rol y dependencia)
    grupo_lab = db(db.auth_group.role == "JEFE DE LABORATORIO").select(db.auth_group.id)[0].id
    grupo_dir = db(db.auth_group.role == "DIRECTOR").select(db.auth_group.id)[0].id
    grupo_asistdir = db(db.auth_group.role == "ASISTENTE DEL DIRECTOR").select(db.auth_group.id)[0].id
    grupo_admin = db(db.auth_group.role == "WEBMASTER").select(db.auth_group.id)[0].id
    grupo_secc = db(db.auth_group.role == "JEFE DE SECCIÓN").select(db.auth_group.id)[0].id
    grupo_coord = db(db.auth_group.role == "COORDINADOR").select(db.auth_group.id)[0].id

    info_membership = db(db.auth_membership.user_id == auth.user_id).select()[0]
    user_group_id = info_membership.group_id

    dependencia = info_membership.dependencia_asociada

    rol = 0
    if user_group_id == grupo_dir or user_group_id == grupo_asistdir or user_group_id == grupo_admin or auth.user.email == "ulab-calidad@usb.ve":
        rol = 2
    elif user_group_id == grupo_lab or user_group_id == grupo_secc or user_group_id == grupo_coord:
        rol = 1
    if request.vars.serv is None:
        return redirect(URL('modulos', 'login'))

    return [rol, dependencia]

def __obtener_jerarquia():

    # Conseguir dependencia y si su rol es suficiente para ver servicios ocultos
    grupo_lab = db(db.auth_group.role == "JEFE DE LABORATORIO").select(db.auth_group.id)[0].id
    grupo_dir = db(db.auth_group.role == "DIRECTOR").select(db.auth_group.id)[0].id
    grupo_asistdir = db(db.auth_group.role == "ASISTENTE DEL DIRECTOR").select(db.auth_group.id)[0].id
    grupo_admin = db(db.auth_group.role == "WEBMASTER").select(db.auth_group.id)[0].id

    info_membership = db(db.auth_membership.user_id == auth.user_id).select()[0]
    user_group_id = info_membership.group_id

    dependencia = info_membership.dependencia_asociada

    rol = 0
    if user_group_id == grupo_dir or user_group_id == grupo_asistdir or \
     user_group_id == grupo_admin or auth.user.email == "ulab-calidad@usb.ve":
        rol = 2
    elif user_group_id == grupo_lab:
        rol = 1

    return [rol, dependencia]

