#------------------------------------ Modulo de compras de SyM -------------------------------------------
# El archivo deberia llamarse compras, pero eso hace que se ejecute luego del db.py y genera un error

#t_Compra: Tabla con las compras de sustancias o materiales
db.define_table(
    #Nombre de la entidad
    't_Compra',

    #Atributos;
    Field('f_nro_factura', 'string', requires=IS_NOT_EMPTY(), label=T('Nombre'), 
    	  notnull=True),

    Field('f_intistitucion', 'string', requires=IS_NOT_EMPTY(), notnull=True, 
    	  label=T('Intistitución')),
    
    Field('f_nif',          'string', requires=IS_NOT_EMPTY(), label=T('NIF')),
    
    Field('f_fecha_compra', 'datetime', requires=IS_DATE(format=T('%d/%m/%Y'), 
    	  error_message='Debe tener el siguiente formato: dd/mm/yyyy'), notnull=True, 
          label=T('Fecha de compra')),
    
    auth.signature
    )
