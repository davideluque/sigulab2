# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# AppConfig configuration made easy. Look inside private/appconfig.ini
# Auth is for authenticaiton and access control
# -------------------------------------------------------------------------

#Tabla para bien mueble

db.define_table(
    'bien_mueble',
    Field('bm_nombre','string',notnull=True,label=T('Nombre del Bien Mueble')),
    Field('bm_num','integer',notnull=True,unique=True,requires = IS_INT_IN_RANGE(1, 999999), label = T('Número Bien Nacional')),
    Field('bm_placa','integer',label=T('Número de Placa del Bien'),requires = IS_INT_IN_RANGE(1, 99999)),
    Field('bm_marca','string',notnull=True,label=T('Marca')),
    Field('bm_modelo','string',notnull=True,label=T('Modelo')),
    Field('bm_serial','string',notnull=True,label=T('Serial')),
    Field('bm_descripcion','text',notnull=True,label=T('Descripción')),
    Field('bm_material','string',notnull=True,label=T('Material Predominante'), requires=IS_IN_SET(['Acero','Acrílico','Madera','Metal','Plástico','Tela'])),
    Field('bm_color','string',notnull=True,label=T('Color'),requires=IS_IN_SET(['Amarillo','Azul','Beige','Blanco','Dorado','Gris','Madera','Marrón','Mostaza','Naranja','Negro','Plateado','Rojo','Rosado','Verde','Vinotinto','Otro color'])),
    Field('bm_unidad','string',label=T('Unidad de Medida'),requires=IS_IN_SET(['cm','m'])),
    Field('bm_ancho','double',label=T('Ancho'),requires=IS_FLOAT_IN_RANGE(0.1,999.99)),
    Field('bm_largo','double',label=T('Largo'),requires=IS_FLOAT_IN_RANGE(0.1,999.99)),
    Field('bm_alto','double',label=T('Alto'),requires=IS_FLOAT_IN_RANGE(0.1,999.99)),
    Field('bm_diametro','double',label=T('Diametro'),requires=IS_FLOAT_IN_RANGE(0.1,999.99)),
    Field('bm_movilidad','string',notnull=True,label=T('Movilidad'),requires=IS_IN_SET(['Fijo','Portátil'])),
    Field('bm_uso','string',notnull=True,label=T('Uso'),requires=IS_IN_SET(['Docencia','Investigación','Extensión','Apoyo administrativo'])),
    Field('bm_categoria', 'string', notnull= True, label = T('Nombre de la categoria'), requires = IS_IN_SET(['maquinaria_construccion',
                    'equipo_transporte', 'equipo_comunicaciones', 'equipo_medico', 'equipo_cientifico_reigioso', 'equipo_oficina'])),
    #Field('bm_sudebip','',notnull=,label=T()),
    #Field('','',notnull=,label=T())

    )

####FALTA CODIGO DE LOCALIZACION Y LOCALIZACION DE PESTANA SUDEBIP

### Tablas de categorias ###

#Maquinaria y demas equipos de construccion, campo, industria y taller
db.define_table(
    'maquinaria_construccion',
    Field('mc_NroBM', 'reference bien_mueble', unique=True, notnull=True, label = T('Número Bien Nacional')),
    Field('mc_nombre','string', notnull=True,label=T('Maquinaria y demás equipos de construcción, campo, industria y taller')),
    Field('mc_subcategoria','string',notnull=True,label=T('Subcategoría'),
        requires=IS_IN_SET(['Maquinaria y equipos de construcción y mantenimiento','Maquinaria y equipos para mantenimiento de automotores','Maquinaria y equipos agrículas y pecuarios',
            'Maquinaria y equipos de artes gráficas y reproducción','Maquinaria y equipos industriales y de taller','Maquinaria y equipos de energía',
            'Maquinaria y equipos de riego y acueductos','Equipos de almacen','Otras maquinarias y demás equipos de construcción, campo, industria y taller']))
    )
db.maquinaria_construccion.mc_NroBM.requires = IS_IN_DB(db, db.bien_mueble.bm_num,'%(bm_num)s') 


#Equipos de transporte, traccion y elevacion
db.define_table(
    'equipo_transporte',
    Field('et_NroBM', 'reference bien_mueble', unique=True, notnull=True, label = T('Número Bien Nacional')),
    Field('et_nombre','string', notnull=True,label=T('Equipos de transporte, tracción y elevación')),
    Field('et_subcategoria','string',notnull=True,label=T('Subcategoría'),
        requires=IS_IN_SET(['Vehículos automotores y terrestes','Equipos ferroviarios y de cables aéreos','Equipos marítimos de transporte','Equipos aéreos de transporte',
            'Vehículos de tracción no motorizados','Equipos auxiliares de transporte','Otros equipos de transporte, tracción y elevación']))
    )
db.equipo_transporte.et_NroBM.requires = IS_IN_DB(db,db.bien_mueble.id,'%(bm_num)s')

#Equipos de comunicaciones y de senalamiento
db.define_table(
    'equipo_comunicaciones',
    Field('ec_NroBM', 'reference bien_mueble', unique=True, notnull=True, label = T('Número Bien Nacional')),
    Field('ec_nombre','string' ,notnull=True,label=T('Equipos de comunicaciones y de señalamiento')),
    Field('ec_subcategoria','string',notnull=True,label=T('Subcategoría'),
        requires=IS_IN_SET(['Equipos de telecomunicaciones','Equipos de señalamiento','Equipos de control de tráfico aéreo','Equipos de corrreo',
            'Otros equipos de comunicaciones y de señalamiento']))
    )
db.equipo_comunicaciones.ec_NroBM.requires = IS_IN_DB(db,db.bien_mueble.bm_num,'%(bm_num)s') 

#Equipos medicos-quirurgicos, dentales y veterinarios
db.define_table(
    'equipo_medico',
    Field('em_NroBM', 'reference bien_mueble', unique=True, notnull=True, label = T('Número Bien Nacional')),
    Field('em_nombre','string', notnull=True,label=T('Equipos médicos-quirúrgicos, dentales y veterinarios')),
    Field('em_subcategoria','string',notnull=True,label=T('Subcategoría'),
        requires=IS_IN_SET(['Equipos médicos-quirúrgicos, dentales y veterinarios','Otros equipos médicos-quirúrgicos, dentales y veterinarios']))
    )
db.equipo_medico.em_NroBM.requires = IS_IN_DB(db,db.bien_mueble.bm_num,'%(bm_num)s') 

#Equipos cientificos, religiosos, de ensenanza y recreacion
db.define_table(
    'equipo_cientifico_religioso',
    Field('ecr_NroBM', 'reference bien_mueble', unique=True, notnull=True, label = T('Número Bien Nacional')),
    Field('ecr_nombre','string', notnull=True,label=T('Equipos científicos, religiosos, de enseñanza y recreación')),
    Field('ecr_subcategoria','string',notnull=True,label=T('Subcategoría'),
        requires=IS_IN_SET(['Equipos científicos y de laboratorio','Equipos de enseñanza, deporte y recreación','Obras de arte','Libros y revistas','Equipos religiosos',
            'Instrumentos musicales','Otros equipos científicos, religiosos, de enseñanza y recreación']))    
    )
db.equipo_cientifico_religioso.ecr_NroBM.requires = IS_IN_DB(db,db.bien_mueble.bm_num,'%(bm_num)s') 


#Maquinas, muebles y demas equiposde oficina y de alojamiento
db.define_table(
    'equipo_oficina',
    Field('eo_NroBM', 'reference bien_mueble', unique=True, notnull=True, label = T('Número Bien Nacional')),
    Field('eo_nombre','string', notnull=True,label=T('Máquinas, muebles y demás equipos de oficina y de alojamiento')),
    Field('eo_subcategoria','string',notnull=True,label=T('Subcategoría'),
        requires=IS_IN_SET(['Mobiliario y equipos de oficina','Equipos de procesamiento de datos','Mobiliario y equipos de alojamiento',
            'Otras máquinas, muebles y demás equipos de oficina y de alojamiento']))
    )
db.equipo_oficina.eo_NroBM.requires = IS_IN_DB(db,db.bien_mueble.bm_num,'%(bm_num)s') 

### Mantenimiento ###
#Hay que preguntar cuales son obligatorios
db.define_table(
    'mantenimiento',
    #Claves
    Field('m_dependencia','string',unique=True,notnull=True,label=T('Dependencia'),requires=IS_LENGTH(4)),
    Field('m_anio','integer',unique=True,notnull=True,label=T('Año'),requires=IS_INT_IN_RANGE(1,99)),
    Field('m_num_correlativo','integer',unique=True,notnull=True,label=T('Número de registro'),requires=IS_INT_IN_RANGE(1,999)),
    #
    Field('m_fecha','date',notnull=True,label=T('Fecha'), requires = IS_DATE(format=('%d-%m-%Y'))), ###Hay que ver el formato, se quiere dd/mm/aaaa
    Field('m_O_S','string',label=T('O/S'),requires=IS_LENGTH(8)),
    Field('m_proveedor','string',label=T('Proveedor')),
    Field('m_tipo_servicio','string',label=T('Tipo de servicio'), requires=IS_IN_SET(['Mantenimiento preventivo','Mantenimiento correctivo','Calibración','Verificación','Otro'])),
    Field('m_descripcion','text',label=T('Descripción')),
    Field('m_fecha_inicio','date',label=T('Fecha de inicio')),
    Field('m_fecha_fin','date',label=T('Fecha de culminación')),
    Field('m_observaciones','text',label=T('Observaciones')),
    Field('m_estatus','string',label=T('Estatus'),requires=IS_IN_SET(['Operativo','Inoperativo','En desuso','Inservible']))
    )

###Solicitudes de prestamo###
db.define_table(
    'prestamo',
    #Claves
    #Field('dependencia','string',unique=True,notnull=True,label=T('Dependencia'),requires=IS_LENGTH(4)),
    Field('p_anio','integer',unique=True,notnull=True,label=T('Año'),requires=IS_INT_IN_RANGE(1,99)),
    Field('p_num_correlativo','integer',unique=True,notnull=True,label=T('Número de registro'),requires=IS_INT_IN_RANGE(1,999)),
    #
    Field('p_fecha','date',notnull=True,label=T('Fecha'), requires = IS_DATE(format=('%d-%m-%Y'))), ###Hay que ver el formato, se quiere dd/mm/aaaa
    Field('p_responsable','text',notnull=True,label=T('Responsable')),
    Field('p_prestado','text',notnull=True,label=T('Prestado a')),
    ##Los pongo aqui para que no lo olvidemos pero esto deberia ser referencia a espacio fisico, con el bien mueble
    Field('p_dependencia','reference dependencias', requires=IS_IN_DB(db,db.dependencias.id,'%(nombre)s'), notnull=True,label=T('Dependencia')),
    ##Field('p_ubicacion','reference espacio_fisicos', requires=IS_IN_DB(db,db.espacio_fisico.id,'%(ubicacion)s'), notnull=True,label=T('Ubicación')),
    ##A los campos de depedencia y ubicacon se le deben añadir lo siguiente en lineas separadas
    Field('p_devolucion','date',notnull=True,label=T('Fecha de devolución')),
    Field('p_observaciones','text',label=T('Observaciones')),
    Field('p_almacen', 'reference espacios_fisicos',
          requires=IS_EMPTY_OR(IS_IN_DB(db, db.espacios_fisicos.id, '%(nombre)s', zero=None)), 
          label=T('Almacén'))
    )

# Estructura seguira para las clasificaciones: La tablade bien_mueble posee un campo llamado "categoria" y uno para el numero
# de bien nacional. La tabla de cada categoria cuenta con un campo que referencia al numero de bien nacional del bien mueble
# y posee otr para el nombre de la categoria. Si queremos matchear ambas tablas con un join podemos hacerlo utlizando esos dos campos
