# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# AppConfig configuration made easy. Look inside private/appconfig.ini
# Auth is for authenticaiton and access control
# -------------------------------------------------------------------------

###Bien mueble###
db.define_table(
    'bien_mueble',
    Field('bm_nombre','string',notnull=True,label=T('Nombre del Bien Mueble')),
    Field('bm_num','string',notnull=True,unique=True,requires = IS_MATCH('^[0-9]{6}'), label = T('Número Bien Nacional')),
    Field('bm_placa','string',label=T('Número de Placa del Bien'),requires = IS_EMPTY_OR(IS_MATCH('^s/n$|^[0-9]{4,6}$'))),
    Field('bm_marca','string',notnull=True,label=T('Marca'),requires=IS_NOT_EMPTY()),
    Field('bm_modelo','string',notnull=True,label=T('Modelo'),requires=IS_NOT_EMPTY()),
    Field('bm_serial','string',notnull=True,label=T('Serial'),requires=IS_NOT_EMPTY()),
    Field('bm_descripcion','text',notnull=True,label=T('Descripción'),requires=IS_NOT_EMPTY()),
    Field('bm_material','string',notnull=True,label=T('Material Predominante'), requires=IS_IN_SET(['Acero','Acrílico','Madera','Metal','Plástico','Tela','Vidrio'])),
    Field('bm_color','string',notnull=True,label=T('Color'),requires=IS_IN_SET(['Amarillo','Azul','Beige','Blanco','Dorado','Gris','Madera','Marrón','Mostaza','Naranja','Negro','Plateado','Rojo','Rosado','Verde','Vinotinto','Otro color'])),
    #Se debe ver cuales categorias requieren esto
    Field('bm_unidad','string',label=T('Unidad de Medida'),requires=IS_EMPTY_OR(IS_IN_SET(['cm','m']))),
    Field('bm_ancho','double',label=T('Ancho'),requires=IS_EMPTY_OR(IS_FLOAT_IN_RANGE(0.1,999.99))),
    Field('bm_largo','double',label=T('Largo'),requires=IS_EMPTY_OR(IS_FLOAT_IN_RANGE(0.1,999.99))),
    Field('bm_alto','double',label=T('Alto'),requires=IS_EMPTY_OR(IS_FLOAT_IN_RANGE(0.1,999.99))),
    Field('bm_diametro','double',label=T('Diametro'),requires=IS_EMPTY_OR(IS_FLOAT_IN_RANGE(0.1,999.99))),
    #
    Field('bm_movilidad','string',notnull=True,label=T('Movilidad'),requires=IS_IN_SET(['Fijo','Portátil'])),
    Field('bm_uso','string',notnull=True,label=T('Uso'),requires=IS_IN_SET(['Docencia','Investigación','Extensión','Apoyo administrativo'])),
    Field('bm_estatus','string',label=T('Estatus'),requires=IS_IN_SET(['Operativo','Inoperativo','En desuso','Inservible'])),
    Field('bm_categoria', 'string', notnull= True, label = T('Nombre de la categoría'), requires = IS_IN_SET(['Maquinaria Construccion',
                    'Equipo Transporte', 'Equipo Comunicaciones', 'Equipo Medico', 'Equipo Cientifico Religioso', 'Equipo Oficina'])),
    Field('bm_codigo_localizacion','string',notnull=True,label=T('Código de Localización'), requires=IS_IN_SET(['150301','240107'])),
    Field('bm_localizacion','string',notnull=True,label=T('Localización'), requires=IS_IN_SET(['Edo Miranda, Municipio Baruta, Parroquia Baruta','Edo Vargas, Municipio Vargas, Parroquia Macuto'])),
    #Foraneas
    Field('bm_espacio_fisico', 'reference espacios_fisicos', notnull=True, label=T('Nombre del espacio fisico')),
    Field('bm_unidad_de_adscripcion', 'reference dependencias', notnull=True, label = T('Unidad de Adscripción')),
    Field('bm_depedencia', 'reference dependencias',notnull=True, label = T('Nombre de la dependencia')),
    Field('bm_crea_ficha', 'references auth_user', notnull = True, label = T('Usuario que crea la ficha'))
    #Field('bm_uso_espacio_fisico', 'reference espacios_fisicos',notnull=True, label = T('Uso del espacio fisico'))
    )
db.bien_mueble.bm_crea_ficha.requires = IS_IN_DB(db, db.auth_user, '%(first_name)s %(last_name)s | %(email)s')
db.bien_mueble.bm_espacio_fisico.requires = IS_IN_DB(db, db.espacios_fisicos.id,'%(nombre)s')
db.bien_mueble.bm_unidad_de_adscripcion.requires = IS_IN_DB(db, db.dependencias.id,'%(unidad_de_adscripcion)s')
db.bien_mueble.bm_depedencia.requires = IS_IN_DB(db, db.dependencias.id,'%(nombre)s')

#####No se implementa una tabla para datos de adquisicion#####

### Tablas de categorias ###
### Heredan de bien mueble

#Maquinaria y demas equipos de construccion, campo, industria y taller
db.define_table(
    'maquinaria_construccion',
    #db.bien_mueble,
    Field('mc_NroBM', 'reference bien_mueble', unique=True, notnull=True, label = T('Número Bien Nacional')),
    Field('mc_nombre','string', notnull=True,label=T('Maquinaria y demás equipos de construcción, campo, industria y taller')),
    Field('mc_subcategoria','string',notnull=True,label=T('Subcategoría'),
        requires=IS_IN_SET(['Maquinaria y equipos de construcción y mantenimiento','Maquinaria y equipos para mantenimiento de automotores','Maquinaria y equipos agrículas y pecuarios',
            'Maquinaria y equipos de artes gráficas y reproducción','Maquinaria y equipos industriales y de taller','Maquinaria y equipos de energía',
            'Maquinaria y equipos de riego y acueductos','Equipos de almacen','Otras maquinarias y demás equipos de construcción, campo, industria y taller']))
    )
#db.maquinaria_construccion.mc_NroBM.requires = IS_IN_DB(db, db.bien_mueble.id,'%(bm_num)s') 


#Equipos de transporte, traccion y elevacion
db.define_table(
    'equipo_transporte',
    #db.bien_mueble,
    Field('et_NroBM', 'reference bien_mueble', unique=True, notnull=True, label = T('Número Bien Nacional')),
    Field('et_nombre','string', notnull=True,label=T('Equipos de transporte, tracción y elevación')),
    Field('et_subcategoria','string',notnull=True,label=T('Subcategoría'),
        requires=IS_IN_SET(['Vehículos automotores y terrestes','Equipos ferroviarios y de cables aéreos','Equipos marítimos de transporte','Equipos aéreos de transporte',
            'Vehículos de tracción no motorizados','Equipos auxiliares de transporte','Otros equipos de transporte, tracción y elevación']))
    )
#db.equipo_transporte.et_NroBM.requires = IS_IN_DB(db,db.bien_mueble.id,'%(bm_num)s')

#Equipos de comunicaciones y de senalamiento
db.define_table(
    'equipo_comunicaciones',
    #db.bien_mueble,
    Field('ec_NroBM', 'reference bien_mueble', unique=True, notnull=True, label = T('Número Bien Nacional')),
    Field('ec_nombre','string' ,notnull=True,label=T('Equipos de comunicaciones y de señalamiento')),
    Field('ec_subcategoria','string',notnull=True,label=T('Subcategoría'),
        requires=IS_IN_SET(['Equipos de telecomunicaciones','Equipos de señalamiento','Equipos de control de tráfico aéreo','Equipos de corrreo',
            'Otros equipos de comunicaciones y de señalamiento']))
    )
#db.equipo_comunicaciones.ec_NroBM.requires = IS_IN_DB(db,db.bien_mueble.id,'%(bm_num)s') 

#Equipos medicos-quirurgicos, dentales y veterinarios
db.define_table(
    'equipo_medico',
    #db.bien_mueble,
    Field('em_NroBM', 'reference bien_mueble', unique=True, notnull=True, label = T('Número Bien Nacional')),
    Field('em_nombre','string', notnull=True,label=T('Equipos médicos-quirúrgicos, dentales y veterinarios')),
    Field('em_subcategoria','string',notnull=True,label=T('Subcategoría'),
        requires=IS_IN_SET(['Equipos médicos-quirúrgicos, dentales y veterinarios','Otros equipos médicos-quirúrgicos, dentales y veterinarios']))
    )
#db.equipo_medico.em_NroBM.requires = IS_IN_DB(db,db.bien_mueble.id,'%(bm_num)s') 

#Equipos cientificos, religiosos, de ensenanza y recreacion
db.define_table(
    'equipo_cientifico_religioso',
    #db.bien_mueble,
    Field('ecr_NroBM', 'reference bien_mueble', unique=True, notnull=True, label = T('Número Bien Nacional')),
    Field('ecr_nombre','string', notnull=True,label=T('Equipos científicos, religiosos, de enseñanza y recreación')),
    Field('ecr_subcategoria','string',notnull=True,label=T('Subcategoría'),
        requires=IS_IN_SET(['Equipos científicos y de laboratorio','Equipos de enseñanza, deporte y recreación','Obras de arte','Libros y revistas','Equipos religiosos',
            'Instrumentos musicales','Otros equipos científicos, religiosos, de enseñanza y recreación']))    
    )
#db.equipo_cientifico_religioso.ecr_NroBM.requires = IS_IN_DB(db,db.bien_mueble.id,'%(bm_num)s') 


#Maquinas, muebles y demas equiposde oficina y de alojamiento
db.define_table(
    'equipo_oficina',
    #db.bien_mueble,
    Field('eo_NroBM', 'reference bien_mueble', unique=True, notnull=True, label = T('Número Bien Nacional')),
    Field('eo_nombre','string', notnull=True,label=T('Máquinas, muebles y demás equipos de oficina y de alojamiento')),
    Field('eo_subcategoria','string',notnull=True,label=T('Subcategoría'),
        requires=IS_IN_SET(['Mobiliario y equipos de oficina','Equipos de procesamiento de datos','Mobiliario y equipos de alojamiento',
            'Otras máquinas, muebles y demás equipos de oficina y de alojamiento']))
    )
#db.equipo_oficina.eo_NroBM.requires = IS_IN_DB(db,db.bien_mueble.id,'%(bm_num)s') 

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

# Estructura seguira para las clasificaciones: La tabla de bien_mueble posee un campo llamado "categoria" y uno para el numero
# de bien nacional. La tabla de cada categoria cuenta con un campo que referencia al numero de bien nacional del bien mueble
# y posee otro para el nombre de la categoria. Si queremos matchear ambas tablas con un join podemos hacerlo utlizando esos dos campos
