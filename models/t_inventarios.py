# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# AppConfig configuration made easy. Look inside private/appconfig.ini
# Auth is for authenticaiton and access control
# -------------------------------------------------------------------------

###Bien mueble###
db.define_table(
    'bien_mueble',
    Field('bm_nombre','string',notnull=True,label=T('Nombre del Bien Mueble'),requires=IS_NOT_EMPTY()),
    Field('bm_num','string',notnull=True,unique=True,requires = IS_MATCH('^[0-9]{6}'), label = T('Número Bien Nacional')),
    Field('bm_placa','string',label=T('Número de Placa del Bien'),requires = IS_EMPTY_OR(IS_MATCH('^s/n$|^[0-9]{4,6}$'))),
    #No son obligatorios para mobiliario
    Field('bm_marca','string',label=T('Marca')),
    Field('bm_modelo','string',label=T('Modelo')),
    Field('bm_serial','string',label=T('Serial')),
    #
    Field('bm_descripcion','text',notnull=True,label=T('Descripción'),requires=IS_NOT_EMPTY()),
    Field('bm_material','string',notnull=True,label=T('Material Predominante'), requires=IS_IN_SET(['Acero','Acrílico','Madera','Metal','Plástico','Tela','Vidrio', 'Otro'])),
    Field('bm_color','string',notnull=True,label=T('Color'),requires=IS_IN_SET(['Amarillo','Azul','Beige','Blanco','Dorado','Gris','Madera','Marrón','Mostaza','Naranja','Negro','Plateado','Rojo','Rosado','Verde','Vinotinto','Otro color'])),
    #Solo lo poseen los equipos
    Field('bm_calibrar', 'string', label = T('Requiere calibración'), requires = IS_EMPTY_OR(IS_IN_SET(['Si', 'No']))),
    Field('bm_fecha_calibracion','date',label=T('Fecha de Calibracion')),
    #
    Field('bm_unidad','string',label=T('Unidad de Medida'),requires=IS_EMPTY_OR(IS_IN_SET(['cm','m']))),
    Field('bm_ancho','double',label=T('Ancho'),requires=IS_EMPTY_OR(IS_FLOAT_IN_RANGE(0.1,999.99))),
    Field('bm_largo','double',label=T('Largo'),requires=IS_EMPTY_OR(IS_FLOAT_IN_RANGE(0.1,999.99))),
    Field('bm_alto','double',label=T('Alto'),requires=IS_EMPTY_OR(IS_FLOAT_IN_RANGE(0.1,999.99))),
    Field('bm_diametro','double',label=T('Diametro'),requires=IS_EMPTY_OR(IS_FLOAT_IN_RANGE(0.1,999.99))),

    Field('bm_movilidad','string',notnull=True,label=T('Movilidad'),requires=IS_IN_SET(['Fijo','Portátil'])),
    Field('bm_uso','string',notnull=True,label=T('Uso'),requires=IS_IN_SET(['Docencia','Investigación','Extensión','Apoyo administrativo'])),
    Field('bm_estatus','string',label=T('Estatus'),requires=IS_IN_SET(['Operativo','Inoperativo','En desuso','Inservible'])),
    Field('bm_categoria', 'string', notnull= True, label = T('Nombre de la categoría'), requires = IS_IN_SET(['Maquinaria Construcción',
    'Equipo Transporte', 'Equipo Comunicaciones', 'Equipo Médico', 'Equipo Científico Religioso', 'Equipo Oficina'])),
    Field('bm_subcategoria', 'string', notnull= True, label = T('Nombre de la subcategoría')),
    Field('bm_codigo_localizacion','string',notnull=True,label=T('Código de Localización'), requires=IS_IN_SET(['150301','240107'])),
    Field('bm_localizacion','string',notnull=True,label=T('Localización'), requires=IS_IN_SET(['Edo Miranda, Municipio Baruta, Parroquia Baruta','Edo Vargas, Municipio Vargas, Parroquia Macuto'])),
    #Foraneas
    Field('bm_espacio_fisico', 'reference espacios_fisicos', notnull=True, label=T('Nombre del espacio fisico')),
    Field('bm_unidad_de_adscripcion', 'reference dependencias', notnull=True, label = T('Unidad de Adscripción')),
    Field('bm_depedencia', 'reference dependencias',notnull=True, label = T('Nombre de la dependencia')),
    Field('bm_crea_ficha', 'reference auth_user', notnull = True, label = T('Usuario que crea la ficha')),

    Field('bm_clasificacion', 'string', notnull = True, label = T('Clasificacion del bien mueble'), requires=IS_IN_SET(['Equipo','Mobiliario']))
    #Field('bm_uso_espacio_fisico', 'reference espacios_fisicos',notnull=True, label = T('Uso del espacio fisico'))
    )
db.bien_mueble.bm_crea_ficha.requires = IS_IN_DB(db, db.auth_user, '%(first_name)s %(last_name)s | %(email)s')
db.bien_mueble.bm_espacio_fisico.requires = IS_IN_DB(db, db.espacios_fisicos.id,'%(nombre)s')
db.bien_mueble.bm_unidad_de_adscripcion.requires = IS_IN_DB(db, db.dependencias.id,'%(unidad_de_adscripcion)s')
db.bien_mueble.bm_depedencia.requires = IS_IN_DB(db, db.dependencias.id,'%(nombre)s')

#####No se implementa una tabla para datos de adquisicion#####

### Mantenimiento ###
#Hay que preguntar cuales son obligatorios
db.define_table(
    'mantenimiento',
    Field('m_NroBM', 'reference bien_mueble', unique=True, notnull=True, label = T('Número Bien Nacional')),
    #Claves
    Field('m_dependencia','reference dependencias',notnull=True,requires=IS_IN_DB(db,db.dependencias.nombre,'%(nombre)s'),label=T('Dependencia')),
    Field('m_anio','integer',unique=True,notnull=True,label=T('Año'),requires=IS_INT_IN_RANGE(1,100)),
    Field('m_num_correlativo','integer',unique=True,notnull=True,label=T('Número de registro'),requires=IS_INT_IN_RANGE(1,1000)),
    #
    Field('m_fecha','date',notnull=True,label=T('Fecha'), requires = IS_DATE(format=('%d-%m-%Y'))), ###Hay que ver el formato, se quiere dd/mm/aaaa
    Field('m_O_S','string',label=T('O/S'),requires=IS_LENGTH(8)),
    Field('m_proveedor','string',label=T('Proveedor')),
    Field('m_tipo_servicio','string',label=T('Tipo de servicio'), requires=IS_IN_SET(['Mantenimiento preventivo','Mantenimiento correctivo','Calibración','Verificación','Otro'])),
    Field('m_descripcion','text',label=T('Descripción')),
    Field('m_fecha_inicio','date',label=T('Fecha de inicio'),requires=IS_DATE(format=('%d-%m-%Y'))),
    Field('m_fecha_fin','date',label=T('Fecha de culminación'), requires=IS_DATE(format=('%d-%m-%Y'))),
    Field('m_observaciones','text',label=T('Observaciones'))
    )
db.mantenimiento.m_NroBM.requires = IS_IN_DB(db,db.bien_mueble.id,'%(first_name)s %(last_name)s | %(email)s') 

###Solicitudes de prestamo###
db.define_table(
    'solicitud_prestamo_bien_mueble',
    #Claves
    Field('p_anio','integer',unique=True,notnull=True,label=T('Año'),requires=IS_INT_IN_RANGE(1,100)),
    Field('p_num_correlativo','integer',unique=True,notnull=True,label=T('Número de registro'),requires=IS_INT_IN_RANGE(1,1000)),
    Field('p_fecha','date',notnull=True,label=T('Fecha'), requires = IS_DATE(format=('%d-%m-%Y'))),
    Field('p_responsable', 'reference t_Personal', requires=IS_IN_DB(db, db.t_Personal.id, '%(f_nombre)s'), label=T('Responsable')),
    Field('p_prestado','string',notnull=True,label=T('Prestado a'), requires = IS_IN_DB(db, db.t_Personal.f_nombre, '%(f_nombre)s')),
    Field('p_dependencia','reference dependencias', unique=True,requires=IS_IN_DB(db,db.dependencias.nombre,'%(nombre)s'), notnull=True,label=T('Dependencia')),
    Field('p_ubicacion','reference espacios_fisicos', requires=IS_IN_DB(db,db.espacios_fisicos.nombre,'%(nombre)s'), notnull=True,label=T('Ubicación')),
    ##A los campos de depedencia y ubicacon se le deben añadir lo siguiente en lineas separadas
    Field('p_devolucion','date',notnull=True,label=T('Fecha de devolución'),requires=IS_DATE(format=('%d-%m-%Y'))),
    Field('p_observaciones','text',label=T('Observaciones')),
    
    # Estado = -1 :Denegado
    # Estado = 0  :Por validación
    # Estado = 1  :Aceptado
    Field('estado','integer', default=0, label=T('Estado de Solicitud'), requires=IS_INT_IN_RANGE(-1,2))
    )
db.solicitud_prestamo_bien_mueble.p_prestado.requires = IS_IN_DB(db,db.t_Personal.id,'%(f_usuario)s') 

### Servicios ###
db.define_table(
    'servicio_bien_mueble',
    Field('s_NroBM', 'reference bien_mueble', unique=True, notnull=True, label = T('Número Bien Nacional')),
    Field('s_fecha','reference historial_solicitudes',notnull=True,label=T('Fecha'),requires=IS_IN_DB(db,db.historial_solicitudes.registro_solicitud,'%(registro_solicitud)s')),
    Field('s_dependencia','reference dependencias',notnull=True,requires=IS_IN_DB(db,db.dependencias.nombre,'%(nombre)s'),label=T('Dependencia')),
    Field('s_cliente_final','reference solicitudes',requires=IS_IN_DB(db,db.solicitudes.proposito_cliente_final,'%(proposito_cliente_final)s'), notnull=True,label=T('Cliente final')),
    #Fecha de inicio y fecha de culminacion deben preguntarse pues en historial de solicitudes aparecen 3 fechas
    #En servicios no se tiene nada sobre horas, hay que preguntar esto
    )
db.servicio_bien_mueble.s_NroBM.requires = IS_IN_DB(db,db.bien_mueble.id,'%(bm_num)s') 

### Solicitud de eliminacion ###
db.define_table(
    'solicitud_eliminar_bien_mueble',
    # Estado = -1 :Denegado
    # Estado = 0  :Por validación
    # Estado = 1  :Aceptado
    Field('eliminar_NroBM', 'reference bien_mueble', unique=True, notnull=True, label = T('Número Bien Nacional')),
    Field('estado','integer', default=0, label=T('Estado de Solicitud'), requires=IS_INT_IN_RANGE(-1,2))
    )
db.solicitud_eliminar_bien_mueble.eliminar_NroBM.requires = IS_IN_DB(db,db.bien_mueble.id,'%(bm_num)s')

###Solicitud de modificacion###
######ACOMODAR

modificacion=db.Table(
    db,
    'modificacion',
    Field('m_nombre','string',label=T('Nombre del Bien Mueble')),
    Field('bm_num','string',notnull=True,unique=True,requires = IS_MATCH('^[0-9]{6}$'), label = T('Número Bien Nacional')),
    Field('m_placa','string',label=T('Número de Placa del Bien'),requires = IS_EMPTY_OR(IS_MATCH('^s/n$|^[0-9]{4,6}$'))),
    Field('m_marca','string',label=T('Marca')),
    Field('m_modelo','string',label=T('Modelo')),
    Field('m_serial','string',label=T('Serial')),
    Field('m_descripcion','text',label=T('Descripción')),
    Field('m_material','string',label=T('Material Predominante'), requires=IS_EMPTY_OR(IS_IN_SET(['Acero','Acrílico','Madera','Metal','Plástico','Tela','Vidrio']))),
    Field('m_color','string',label=T('Color'),requires=IS_EMPTY_OR(IS_IN_SET(['Amarillo','Azul','Beige','Blanco','Dorado','Gris','Madera','Marrón','Mostaza','Naranja','Negro','Plateado','Rojo','Rosado','Verde','Vinotinto','Otro color']))),
    #Se debe ver cuales categorias requieren esto
    Field('m_unidad','string',label=T('Unidad de Medida'),requires=IS_EMPTY_OR(IS_IN_SET(['cm','m']))),
    Field('m_ancho','double',label=T('Ancho'),requires=IS_EMPTY_OR(IS_FLOAT_IN_RANGE(0.1,999.99))),
    Field('m_largo','double',label=T('Largo'),requires=IS_EMPTY_OR(IS_FLOAT_IN_RANGE(0.1,999.99))),
    Field('m_alto','double',label=T('Alto'),requires=IS_EMPTY_OR(IS_FLOAT_IN_RANGE(0.1,999.99))),
    Field('m_diametro','double',label=T('Diametro'),requires=IS_EMPTY_OR(IS_FLOAT_IN_RANGE(0.1,999.99))),
    Field('m_movilidad','string',label=T('Movilidad'),requires=IS_EMPTY_OR(IS_IN_SET(['Fijo','Portátil']))),
    Field('m_uso','string',label=T('Uso'),requires=IS_EMPTY_OR(IS_IN_SET(['Docencia','Investigación','Extensión','Apoyo administrativo']))),
    Field('m_categoria', 'string', label = T('Nombre de la categoría'), requires = IS_EMPTY_OR(IS_IN_SET(['Maquinaria Construccion',
                        'Equipo Transporte', 'Equipo Comunicaciones', 'Equipo Medico', 'Equipo Cientifico Religioso', 'Equipo Oficina']))),
    Field('m_codigo_localizacion','string',label=T('Código de Localización'), requires=IS_EMPTY_OR(IS_IN_SET(['150301','240107']))),
    Field('m_localizacion','string',label=T('Localización'), requires=IS_EMPTY_OR(IS_IN_SET(['Edo Miranda, Municipio Baruta, Parroquia Baruta','Edo Vargas, Municipio Vargas, Parroquia Macuto']))),
    #Foraneas
    Field('m_espacio_fisico', 'reference espacios_fisicos', label=T('Nombre del espacio fisico'),requires = IS_EMPTY_OR(IS_IN_DB(db, db.espacios_fisicos.id,'%(nombre)s'))),
    Field('m_unidad_de_adscripcion', 'reference dependencias', label = T('Unidad de Adscripción'),requires = IS_EMPTY_OR(IS_IN_DB(db, db.dependencias.id,'%(unidad_de_adscripcion)s'))),
    Field('m_depedencia', 'reference dependencias', label = T('Nombre de la dependencia'),requires = IS_EMPTY_OR(IS_IN_DB(db, db.dependencias.id,'%(nombre)s'))),
    Field('m_crea_ficha', 'references auth_user', label = T('Usuario que crea la ficha'),requires = IS_EMPTY_OR(IS_IN_DB(db, db.auth_user, '%(first_name)s %(last_name)s | %(email)s')))
    #Field('bm_uso_espacio_fisico', 'reference espacios_fisicos',notnull=True, label = T('Uso del espacio fisico'))
    )

db.define_table(
    'solicitud_modificar_bien_mueble',
    Field('modificar_NroBM', 'reference bien_mueble', notnull=True, label = T('Número Bien Nacional del Bien Mueble que desea modificar')),
    modificacion,
    # Estado = -1 :Denegado
    # Estado = 0  :Por validación
    # Estado = 1  :Aceptado
    Field('estado','integer', default=0, label=T('Estado de Solicitud'), requires=IS_INT_IN_RANGE(-1,2))
    )
db.solicitud_modificar_bien_mueble.modificar_NroBM.requires = IS_IN_DB(db,db.bien_mueble.id,'%(bm_num)s') 

### Tabla general para bienes muebles que no poseen numero de bien nacional ###

db.define_table(
	'sin_bn',
	Field('sb_nombre', 'string', notnull = True, label = T('Nombre del elemento')),
	Field('sb_marca', 'string', label = T('Marca del elemento')),
	Field('sb_modelo', 'string', label = T('Modelo/código del elemento')),
	Field('sb_cantidad', 'integer', notnull = True, label = T('Cantidad'), requires = IS_INT_IN_RANGE(0,99999999)),
	Field('sb_espacio', 'reference espacios_fisicos', notnull = True, label = T('Espacio físico al que pertenece')), 
	Field('sb_ubicacion', 'string', notnull = True, label = T('Ubicacion interna'), requires = IS_IN_SET(['Estante', 'Anaquel', 'Gaveta', 'Mesón', 'Archivo', 'Otro'])),
	Field('sb_descripcion', 'text', label = T('Descripción del elemento')),
	Field('sb_aforado', 'string', label = T('Condición de aforado'), requires = IS_EMPTY_OR(IS_IN_SET(['Si', 'No', 'N/A']))),
	Field('sb_calibrar', 'string', label = T('Requiere calibración'), requires = IS_EMPTY_OR(IS_IN_SET(['Si', 'No']))),
	Field('sb_capacidad', 'string', label = T('Capacidad'), requieres = IS_EMPTY_OR(IS_MATCH('^[0-9]{5},[0-9]{2}$'))),
	Field('sb_unidad', 'string', label = T('Unidad de medida de capacidad'), requires = IS_EMPTY_OR(IS_IN_SET(['m³','l','ml','μl','kg','g','mg','μg','galón','oz','cup','lb']))),
	Field('sb_unidad_dim', 'string', label = T('Unidad de medida de dimensiones'), requires = IS_EMPTY_OR(IS_IN_SET(['m', 'cm']))),
    Field('sb_ancho','double',label=T('Ancho'),requires=IS_EMPTY_OR(IS_FLOAT_IN_RANGE(0.1,999.99))),
    Field('sb_largo','double',label=T('Largo'),requires=IS_EMPTY_OR(IS_FLOAT_IN_RANGE(0.1,999.99))),
    Field('sb_alto','double',label=T('Alto'),requires=IS_EMPTY_OR(IS_FLOAT_IN_RANGE(0.1,999.99))),
    Field('sb_diametro','double',label=T('Diametro'),requires=IS_EMPTY_OR(IS_FLOAT_IN_RANGE(0.1,999.99))),
    Field('sb_material', 'string', label = T('Material predominante')),
    Field('sb_material_sec', 'string', label = T('Material secundario'), requires = IS_EMPTY_OR(IS_IN_SET(['Acero', 'Acrílico', 'Cerámica', 'Cuarzo', 'Madera',
                                                                                                        'Metal', 'Plástico', 'Tela', 'Vidrio', 'Otro']))),
   	Field('sb_presentacion', 'string', label = T('Presentación')),
	Field('sb_unidades', 'string', label = T('Unidades por presentación'), requires = IS_EMPTY_OR(IS_MATCH('^[0-9]{5}$'))),
	Field('sb_total', 'integer', label = T('Total de unidades')),
    Field('sb_clasificacion', 'string', notnull = True, label = T('Clasificacion del consumible/material'), requires=IS_IN_SET(['Material de Laboratorio','Consumible']))
	#primarykey = ['sb_nombre', 'sb_espacio']
	)

db.sin_bn.sb_espacio.requires = IS_IN_DB(db, db.espacios_fisicos.id,'%(nombre)s')
db.sin_bn.sb_nombre.requires=IS_NOT_IN_DB(db(db.sin_bn.sb_espacio==request.vars.sb_espacio),'sin_bn.sb_nombre')

# Nota: Cantidad para consumibles debe tener una longitud de 4 dígitos
#		Colocar la opción de especificar dede el front para el field "prsentacion" en sin_bn y en "material" en sin_bn
# 		Calculo de la cantidad total de unidades que se hace multiplicando el número de unidades por la cantidad 
#		sb_unidad es obligatorio si se rellena sb_capacidad