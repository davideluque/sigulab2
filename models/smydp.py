#----------- Modulo de Sustancias, materiales y desechos peligrosos ------------

################################################################################
#
#                     TABLAS DEL CATALOGO DE SUSTANCIAS
#
################################################################################

#t_Unidades_de_medida: Tabla de unidades de medida de las sustancias (ml, l, g, kg, etc.)
db.define_table(
    #Nombre de la entidad
    't_Unidad_de_medida',

    #Atributos;
    Field('f_nombre', 'string', requires=IS_NOT_EMPTY(), label=T('Nombre')),
    Field('f_abreviatura', 'string', requires=IS_NOT_EMPTY(), label=T('Abreviatura'))
    )

#t_Sustancia: Tabla de sustancias de la cual se obtiene informacion del listado (catalogo de sustancias)
db.define_table(
    #Nombre de la entidad
    't_Sustancia',

    #Atributos;
    Field('f_nombre', 'string', requires=IS_NOT_EMPTY(), label=T('Nombre')),

    Field('f_cas', 'string', requires=[IS_NOT_EMPTY(), IS_MATCH('^[0-9]+\-[0-9]+\-[0-9]+$',
          error_message='El CAS debe contener tres números separados entre sí por guiones. Por ejemplo, 7732-18-5')],
          unique=True, label=T('CAS')),

    Field('f_pureza', 	'integer',	requires=IS_INT_IN_RANGE(0, 101), label=T('Pureza')),

    Field('f_estado', 'list:string',requires=IS_IN_SET(['Sólido','Líquido','Gaseoso']), 
          widget=SQLFORM.widgets.options.widget, label=T('Estado')),

    Field('f_control', 'list:string',requires=IS_IN_SET(['N/A','RL4','RL7', 'RL4 y RL7']), 
          widget=SQLFORM.widgets.options.widget, label=T('Control')),

    # *!* La unidad no va aqui, porque alguien podria querer solicitar la sustancia 
    # en ml porque es muy poca y estaria obligada a usar una unidad 
    #Field('f_unidad', 'list:string',requires=IS_IN_SET(['kg','g','l', 'ml']), 
    # widget=SQLFORM.widgets.options.widget, label=T('Unidad')),

    Field('f_peligrosidad', 'list:string',
          requires=IS_IN_SET(['Inflamable','Tóxico','Tóxico para el ambiente',
                    'Corrosivo','Comburente','Nocivo','Explosivo','Irritante'],
          multiple = True), widget=SQLFORM.widgets.checkboxes.widget, 
          label=T('Peligrosidad')),
    
    # Hoja de seguridad (archivo pdf)
    Field('f_hds','upload',requires=IS_NULL_OR(IS_UPLOAD_FILENAME(extension='pdf')),
          label=T('Hoja de seguridad')),
    # Agrega los campos adicionales created_by, created_on, modified_by, modified_on para los logs de la tabla
    auth.signature
    )

db.t_Sustancia.id.readable=False
db.t_Sustancia.id.writable=False
db.t_Sustancia.f_hds.readable=(auth.has_membership('GESTOR DE SMyDP') or \
                               auth.has_membership('WEBMASTER')) #*!* Chequear permisos aqui
db.t_Sustancia._singular='Catálogo de Sustancias'
db.t_Sustancia._plural='Catálogo de Sustancias'


################################################################################
#
#                     TABLAS DEL MODULO DE COMPRAS
#
################################################################################

# Esto deberia estar en un modulo separado, pero eso hace que se ejecute luego  
# del models/db.py o del models/smydp.py y genera un error

#t_Compra: Tabla con las compras de sustancias o materiales
db.define_table(
    #Nombre de la entidad
    't_Compra',

    #Atributos:

    Field('f_cantidad', 'double', requires=IS_NOT_EMPTY(), label=T('Cantidad')),

    Field('f_nro_factura', 'string', requires=IS_NOT_EMPTY(), label=T('Nro. Factura'), 
          notnull=True),

    Field('f_institucion', 'string', requires=IS_NOT_EMPTY(), notnull=True, 
          label=T('Intistitución')),
    
    Field('f_rif', 'string', label=T('RIF')),
    
    Field('f_fecha', 'string', notnull=True, label=T('Fecha de compra')),
    
    # Referencias a otras tablas
    Field('f_sustancia', 'reference t_Sustancia',
          requires=IS_IN_DB(db, db.t_Sustancia.id, '%(f_nombre)s', zero=None), 
          label=T('Sustancia comprada'), notnull=True),

    # Unidad de medida de la cantidad de sustancia comprada
    Field('f_medida', 'reference t_Unidad_de_medida',
          requires=IS_IN_DB(db, db.t_Unidad_de_medida.id, '%(f_nombre)s', zero=None), 
          label=T('Unidad de medida'), notnull=True),

    auth.signature
    )

################################################################################
#
#                     TABLAS DE SOLICITUDES DE SUSTANCIAS
#
################################################################################

# *!* revisar todos los campos y sus contraints
# *!* poner los mismos nombres en el pdf UL04-18-049 Inf complementaria sobre Solicitudes  Sust

#t_Solicitud: Tabla con los datos de solicitudes de sustancias entre espacios fisicos
db.define_table(
    #Nombre de la entidad
    't_Solicitud_smydp',

    #Atributos;

    # Cantidad de sustancia solicitada
    Field('f_cantidad', 'double', requires=IS_NOT_EMPTY(), label=T('Cantidad')),

    # Codigo del registro
    Field('f_cod_registro', 'string', label=T('Codigo del registro')),

    # Cantidad de sustancia que ya ha sido prometida por otros espacios al aceptar
    # la solicitud
    Field('f_cantidad_conseguida', 'double', label=T('Cantidad conseguida')),

    Field('f_estatus', 'list:string', widget=SQLFORM.widgets.options.widget, 
          requires=IS_IN_SET(['Caducada','En espera','Completada', 'Por entregar', 
                            'Por recibir', 'Prestamo por devolver']), 
          label=T('Estatus de la solicitud'), notnull=True),
    
    Field('f_uso', 'list:string',requires=IS_IN_SET(['Docencia','Investigación','Extensión']), 
          widget=SQLFORM.widgets.options.widget, label=T('Uso de la sustancia')),
    
    Field('f_justificacion', 'string', label=T('Justificación')),
    
    Field('f_fecha_caducidad', 'datetime', requires=IS_DATE(format=T('%d/%m/%Y'), 
          error_message='Debe tener el siguiente formato: dd/mm/yyyy'), notnull=True, 
          label=T('Fecha de caducidad')),
    
    # Referencias a otras tablas

    # Unidad de medida de la cantidad solicitada
    Field('f_medida', 'reference t_Unidad_de_medida',
          requires=IS_IN_DB(db, db.t_Unidad_de_medida.id, '%(f_nombre)s', zero=None), 
          label=T('Unidad de medida'), notnull=True),

    # Espacio fisico solicitante
    Field('f_espacio', 'reference espacios_fisicos',
          requires=IS_IN_DB(db, db.espacios_fisicos.id, '%(nombre)s', zero=None), 
          label=T('Espacio solicitante'), notnull=True),
    
    # Sustancia solicitada
    Field('f_sustancia', 'reference t_Sustancia',
          requires=IS_IN_DB(db, db.t_Sustancia.id, '%(f_nombre)s', zero=None), 
          label=T('Sustancia'), notnull=True),

    # Responsable que entrega la sustancia
    Field('f_responsable_solicitud', 'reference t_Personal', 
          requires=IS_EMPTY_OR(IS_IN_DB(db, db.t_Personal.id, '%(f_email)s', zero=None))),
    
    auth.signature
    )

#t_Respuesta: Respuestas a la solicitud de sustancias
db.define_table(
    #Nombre de la entidad
    't_Respuesta',

    #Atributos;

    # Codigo del registro
    Field('f_cod_registro', 'string', label=T('Codigo del registro')),

    # Cantidad a suministrar. Vacio si la respuesta es una negacion
    Field('f_cantidad', 'double', label=T('Cantidad')),

    # Unidad de medida de la cantidad indicada (None si f_cantidad lo es y viceversa *!*)
    Field('f_medida', 'reference t_Unidad_de_medida',
          requires=IS_IN_DB(db, db.t_Unidad_de_medida.id, '%(f_nombre)s', zero=None), 
          label=T('Unidad de medida')),
    
    # Indica si la solicitud fue aceptada o rechazada
    Field('f_tipo_respuesta', 'list:string', requires=IS_IN_SET(['Negación','Aceptación']), 
        label=T('Respuesta a la solicitud')),
    
    # Almacena información como la causa de la negación de la solicitud
    Field('f_justificacion', 'string', label=T('Justificación')),

    # En que terminos se esta aceptando dar la sustancia
    Field('f_calidad', 'list:string',requires=IS_IN_SET(['Cesión','Préstamo']), 
          widget=SQLFORM.widgets.options.widget, label=T('Calidad')),
    
    # Fecha en que se recibe la sustancia solicitada
    Field('f_fecha_recepcion', 'datetime', requires = IS_EMPTY_OR(IS_DATE(format=('%d-%m-%Y'))),
          label=T('Fecha de recepción')),

    # Fecha en que se hace constar la devolucion de la sustancia
    Field('f_fecha_devolucion', 'datetime', requires = IS_EMPTY_OR(IS_DATE(format=('%d-%m-%Y'))),
          label=T('Fecha de devolución')),

    # Indica la fecha tope en que debe devolverse el material prestado (solo si 
    # f_calidad es "prestamo" *!*)
    Field('f_fecha_tope_devolucion', 'datetime', requires=IS_EMPTY_OR(IS_DATE(format=T('%d/%m/%Y'), 
          error_message='Debe tener el siguiente formato: dd/mm/yyyy')),
          label=T('Fecha tope para la devolución')),

    # Referencias a otras tablas
    
    # Espacio que responde a la solicitud
    Field('f_espacio', 'reference espacios_fisicos',
          requires=IS_IN_DB(db, db.espacios_fisicos.id, '%(nombre)s', zero=None), 
          label=T('Espacio solicitante'), notnull=True),

    # Responsable que entrega la sustancia
    Field('f_responsable_entrega', 'reference t_Personal', 
          requires=IS_EMPTY_OR(IS_IN_DB(db, db.t_Personal.id, '%(f_email)s', zero=None))),

    # Responsable que hace constar la recepcion de la sustancia solicitada
    Field('f_responsable_recepcion', 'reference t_Personal', 
          requires=IS_EMPTY_OR(IS_IN_DB(db, db.t_Personal.id, '%(f_email)s', zero=None))),

    # Responsable que hace constar la devolucion
    Field('f_responsable_devolucion', 'reference t_Personal', 
          requires=IS_EMPTY_OR(IS_IN_DB(db, db.t_Personal.id, '%(f_email)s', zero=None))),

    # ID de la solicitud a la que se esta dando respuesta
    Field('f_solicitud', 'reference t_Solicitud_smydp',
          requires=IS_IN_DB(db, db.t_Solicitud_smydp.id, zero=None), 
          label=T('Solicitud'), notnull=True),
    
    # Almacena el id del responsable que acepta o niega la solicitud y fecha en que lo hace
    auth.signature
    )

##############################################################################
#
#                     TABLAS DEL INVENTARIO Y BITACORA
#
###############################################################################

#t_Inventario: Tabla de la entidad debil Inventario que contiene la existencia de 
# cada sustancia en cada espacio fisico
db.define_table(
    #Nombre de la entidad
    't_Inventario',

    #Atributos;

    # Cantidades (el excedente es calculado dinamicamente como existencia - uso interno)
    Field('f_existencia', 'double', requires=IS_NOT_EMPTY(), label=T('Existencia')),

    Field('f_uso_interno', 'double', requires=IS_NOT_EMPTY(), label=T('Uso interno')),
    
    Field('f_medida', 'reference t_Unidad_de_medida',
          requires=IS_IN_DB(db, db.t_Unidad_de_medida.id, '%(f_nombre)s', zero=None), 
          label=T('Unidad de medida'), notnull=True),
    
    # Referencias a otras tablas
    Field('espacio', 'reference espacios_fisicos',
          requires=IS_IN_DB(db, db.espacios_fisicos.id, '%(codigo)s', zero=None), 
          label=T('Espacio Físico'), notnull=True),
    
    Field('sustancia', 'reference t_Sustancia',
          requires=IS_IN_DB(db, db.t_Sustancia.id, '%(f_nombre)s', zero=None), 
          label=T('Sustancia'), notnull=True),

    # Agrega los campos adicionales created_by, created_on, modified_by, modified_on 
    # para los logs de la tabla
    auth.signature
    )

db.t_Inventario._singular='Inventario'
db.t_Inventario._plural='Inventario'


# *!* Ver not nulls y constraints de t_Balance

#t_Balance: Tabla de la bitacora de los movimientos en los inventarios de todos 
# los espacios fisicos
db.define_table(
    #Nombre de la entidad
    't_Balance',

    #Atributos;

    # Cantidad ingresada o egresada
    Field('f_cantidad', 'double', requires=IS_NOT_EMPTY(), label=T('Cantidad modificada')),

    # Cantidad total luego del ingreso o egreso
    Field('f_cantidad_total', 'double', requires=IS_NOT_EMPTY(), label=T('Total')),

    # Concepto del ingreso, egreso o cambio en el inventario *!* COnsumo x egreso
    Field('f_concepto', 'list:string', label=T('Calidad'),
          requires=IS_IN_SET(['Ingreso','Consumo']), 
          widget=SQLFORM.widgets.options.widget),
    
    # Tipo de ingreso de la sustancia (Null si f_concepto no es Ingreso) *!*
    Field('f_tipo_ingreso', 'list:string', label=T('Tipo de ingreso'),
          requires=IS_EMPTY_OR(IS_IN_SET(['Compra','Almacén','Solicitud','Ingreso inicial','Prestamo'])), 
          widget=SQLFORM.widgets.options.widget),

    # Tipo de egreso de la sustancia. Otorgado si fue cedido o prestadeo a otra
    # seccion como respuesta a usa solicitud 
    # (Null si f_concepto no es Egreso) *!*
    Field('f_tipo_egreso', 'list:string', label=T('Tipo de egreso'),
          requires=IS_EMPTY_OR(IS_IN_SET(['Docencia','Investigación','Extensión','Gestión','Prestamo','Cesión'])), 
          widget=SQLFORM.widgets.options.widget),
    
    # Descripcion del registro para ser mostrada en la tabla de la bitacora
    Field('f_descripcion', 'string', label=T('Descripción')),

    # Fecha de la modificacion esta fecha es cuando se uso la sustancia para asi llevar un calculo mas completo 
    Field('f_fechaUso', 'date', requires=IS_NOT_EMPTY(), label=T('Fecha de uso')),
    # Referencias a otras tablas

    # Referencias obligatorias

    # Unidad de medida de la cantidad ingresada o egresada 
    Field('f_medida', 'reference t_Unidad_de_medida',
          requires=IS_IN_DB(db, db.t_Unidad_de_medida.id, '%(f_nombre)s', zero=None), 
          label=T('Unidad de medida'), notnull=True),
    
    # Referencia hacia el inventario al cual pertenece el registro de la bitacora
    Field('f_inventario', 'reference t_Inventario',
          requires=IS_IN_DB(db, db.t_Inventario.id, zero=None), 
          label=T('Inventario'), notnull=True),

    # Sustancia ingresada o consumida. Sirve para el reporte mensual RL4 y 7
    Field('f_sustancia', 'reference t_Sustancia',
          requires=IS_IN_DB(db, db.t_Sustancia.id, '%(f_nombre)s', zero=None), 
          label=T('Sustancia'), notnull=True),

    # Referencias opcionales (dependiendo del tipo de entrada o salida)

    # Instancia del servicio en el que se empleara la sustancia egresada
    # Requiere "f_concepto" = "egreso" *!* Null de lo contrario
    Field('f_servicio', 'reference servicios',
          requires=IS_EMPTY_OR(IS_IN_DB(db, db.servicios.id, '%(nombre)s', zero=None)), 
          label=T('Servicio')),
    
    # Referencia hacia la tabla espacios fisicos con el id del almacen surtidor
    # Requiere "f_concepto" = "ingreso" y "f_tipo_ingreso = "Almacen" *!* Null de lo contrario
    Field('f_almacen', 'reference espacios_fisicos',
          requires=IS_EMPTY_OR(IS_IN_DB(db, db.espacios_fisicos.id, '%(nombre)s', zero=None)), 
          label=T('Almacén')),

    # Referencia hacia la tabla de compras (*!* Null si no es un ingreso por compra)
    # Requiere "f_concepto" = "egreso" *!* Null de lo contrario
    Field('f_compra', 'reference t_Compra',
          requires=IS_EMPTY_OR(IS_IN_DB(db, db.t_Compra.id, '%(f_institucion)s', zero=None)), 
          label=T('Compra')),

    # Referencia hacia la tabla de respuestas a solicitudes (*!* Null si no es un 
    # ingreso por compra)
    # Requiere "f_concepto" = "ingreso" y "f_tipo_ingreso = "Solicitud" 
    # *!* Null de lo contrario
    Field('f_respuesta_solicitud', 'reference t_Respuesta',
          requires=IS_EMPTY_OR(IS_IN_DB(db, db.t_Respuesta.id, '%(f_tipo_respuesta)s', zero=None)), 
          label=T('Respuesta de solicitud')),

    # Agrega los campos adicionales created_by, created_on, modified_by, modified_on 
    # para los logs de la tabla
    auth.signature
    )


    ## Desechos peligrosos

    # Tabla de Categorías de Desechos peligrosos. Cada desecho peligroso pertenece a un cierto categoria (tipo), los cuáles
# se definen en esta tabla. Contiene los campos: categoria de desecho, estado, peligrosidad.
db.define_table(
    't_categoria_desechos',
    #Atributos;
    Field('categoria', 'string', unique=True, notnull=True, label=T('Categoría')),
    Field('descripcion', 'string', label=T('Descripción'))
)


db.t_categoria_desechos._plural = 'Categoría de Desecho'
db.t_categoria_desechos._singular = 'Categorías de Desechos'

    # Tabla de envases en donde serán almacenados los desechos peligrosos
db.define_table(
    't_envases',
    #Atributos;
    Field('identificacion', 'string', notnull=True, unique=True, requires=IS_NOT_EMPTY(), label=T('Identificación')),

    Field('capacidad', 'double', requires=IS_NOT_EMPTY(), label=T('Capacidad'), notnull=True),

    Field('unidad_medida', 'reference t_Unidad_de_medida',
          requires=IS_IN_DB(db, db.t_Unidad_de_medida.id, '%(f_abreviatura)s', zero=None), label=T('Unidad de medida'), notnull=True,
          represent=lambda id, r: db.t_Unidad_de_medida[id].f_nombre),

    Field('forma', 'string', requires=IS_IN_SET(['Cilíndrica', 'Cuadrada', 'Rectangular', 'Otra']), notnull=True, label=T('Forma')),

    Field('material', 'string', requires=IS_IN_SET(['Plástico', 'Polietileno (HDPE)', 'Polietileno (PE)', 'Vidrio', 'Metal', 'Acero', 'Otro']), notnull=True, label=T('Material')),
    
    Field('tipo_boca', 'string', requires=IS_IN_SET(['Boca ancha', 'Boca angosta', 'Cerrados con abertura de trasvase', 'Otra']), notnull=True, label=T('Tipo de boca')),

    Field('descripcion', 'string', notnull=False, label=T('Descripción')),

    Field('composicion', 'string', notnull=False, label=T('Composición')),

    Field('espacio_fisico', 'reference espacios_fisicos', 
            requires=IS_IN_DB(db, db.espacios_fisicos.id, '%(codigo)s', zero=None), 
            notnull=True, 
            label=T('Espacio físico'),
            represent=lambda id, r: db.espacios_fisicos[id].nombre
            ), 

    Field('categoria', 'reference t_categoria_desechos', 
            requires=IS_IN_DB(db, db.t_categoria_desechos.id, '%(categoria)s', zero=None), 
            notnull=True, label=T('Categoría de Desecho'),
            represent=lambda id, r: db.t_categoria_desechos[id].categoria
        
    ),


)

db.t_envases._plural = 'Envases'
db.t_envases._singular = 'Envase'

# Tabla de Desechos peligrosos. Contiene los campos: espacio_físico, cantidad, sección, responsable, categoria.
db.define_table(
    't_inventario_desechos',
    #Atributos;
    Field('categoria', 'reference t_categoria_desechos', 
            requires=IS_IN_DB(db, db.t_categoria_desechos.id, '%(categoria)s', zero=None), notnull=True, label=T('Categoría de Desecho')),

    Field('cantidad', 'double', requires=IS_NOT_EMPTY(), label=T('Cantidad'), notnull=True),

    Field('unidad_medida', 'reference t_Unidad_de_medida',
          requires=IS_IN_DB(db, db.t_Unidad_de_medida.id, '%(f_nombre)s', zero=None), label=T('Unidad de medida'), notnull=True),

    Field('composicion', 'string', requires=IS_NOT_EMPTY(), label=T('Composición')),

    Field('concentracion', 'string', requires=IS_NOT_EMPTY(), label=T('Concentración')),

    Field('espacio_fisico', 'reference espacios_fisicos', 
            requires=IS_IN_DB(db, db.espacios_fisicos.id, '%(codigo)s', zero=None), notnull=True, label=T('Espacio físico')), 

    Field('seccion', 'reference dependencias', requires=IS_IN_DB(db, db.dependencias.id, '%(nombre)s', zero=None), label=T('Unidad de Adscripción'), notnull=True),

    Field('responsable', 'reference t_Personal', 
            requires=IS_IN_DB(db, db.t_Personal.id, '%(f_nombre)s | %(f_email)s', zero=None), notnull=True, label=T('Responsable')),

   Field('envase', 'reference t_envases', 
            requires=IS_EMPTY_OR(IS_IN_DB(db, db.t_envases.id, '%(identificacion)s', zero=None)), notnull=True, label=T('Envase')),

    Field('tratamiento', 'string', requires=IS_IN_SET(['Reutilizable', 'Recuperable', 'Tratable', 'Disposición final']), notnull=True, label=T('Tratamiento')),

     Field('peligrosidad', 'list:string', 
          requires=IS_IN_SET(['Sustancia Explosiva (EX)','Sustancia Inflamable (IN)','Sustancia Comburente (CB)', 'Gaso Bajo Presión (GZ)', 
                            'Corrosiva (CR)', 'Toxicidad Aguda (TO)', 'Peligro para la Salud (DA)', 'Peligro Grave para la Salud - Cancerígeno Mutágeno (MU)', 'Dañino para el Medio Ambiente Acuático (EN)'],
          multiple = True), widget=SQLFORM.widgets.checkboxes.widget, label=T('Peligrosidad'), notnull=True)
)


db.t_inventario_desechos._plural = 'Inventarios de Desechos Peligrosos'
db.t_inventario_desechos._singular = 'Inventarios de Desecho Peligrosos'

#Tabla de la Bitacora de los movimientos en los inventarios de todos los espacios fisicos. Contiene los campos:
db.define_table(
    #Nombre de la entidad
    't_Bitacora_desechos',

    #Atributos;
    
    # Fecha registro
    Field('fecha', 'string', notnull=True, label=T('Fecha de movimiento')),

    # Descripción (proceso de generación)
    Field('descripcion', 'string', notnull=True, label=T('Descripcion de movimiento')),

    # Cantidad generada
    Field('cantidad_generada', 'double', requires=IS_NOT_EMPTY(), label=T('Cantidad generada')),

    # Cantidad retirada
    Field('cantidad_retirada', 'double', requires=IS_NOT_EMPTY(), label=T('Cantidad retirada')),

    # Saldo luego del movimiento
    Field('saldo', 'double', requires=IS_NOT_EMPTY(), label=T('Saldo')),

    # Unidad de medida del desecho
    Field('unidad_medida_bitacora', 'reference t_Unidad_de_medida',
          requires=IS_IN_DB(db, db.t_Unidad_de_medida.id, '%(f_nombre)s', zero=None), label=T('Unidad de medida'), notnull=True,
          represent=lambda id, r: db.t_Unidad_de_medida[id].f_nombre),

    # Identificación del recipiente del desecho
    Field('envase', 'reference t_envases', 
            requires=IS_EMPTY_OR(IS_IN_DB(db, db.t_envases.id, '%(identificacion)s', zero=None)), notnull=True, label=T('Envase')),
    
    # Referencia hacia el inventario al cual pertenece el registro de la bitacora
    Field('inventario', 'reference t_inventario_desechos',
          requires=IS_IN_DB(db, db.t_inventario_desechos.id, zero=None), 
          label=T('Inventario'), notnull=True,
          represent=lambda id, r: db.t_inventario_desechos[id].nombre),


    # Agrega los campos adicionales created_by, created_on, modified_by, modified_on 
    # para los logs de la tabla
    auth.signature
    )