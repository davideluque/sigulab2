#------------------------------------ Modulo de Sustancias, materiales y desechos peligrosos-------------------------------------------


#t_Sustancia: Tabla de sustancias de la cual se obtiene informacion del listado (catalogo de sustancias)
db.define_table(
    #Nombre de la entidad
    't_Sustancia', 
    #Atributos;
    Field('f_nombre', 	'string',	requires=IS_NOT_EMPTY(), label=T('Nombre')),
    Field('f_cas', 		'string',	requires=IS_NOT_EMPTY(), unique=True, label=T('CAS')),
    Field('f_pureza', 	'integer',	requires=IS_INT_IN_RANGE(0, 101), label=T('Pureza')),
    Field('f_estado', 'list:string',requires=IS_IN_SET(['Sólido','Líquido','Gaseoso']), 
    widget=SQLFORM.widgets.checkboxes.widget, label=T('Estado')),
    Field('f_control', 'list:string',requires=IS_IN_SET(['N/A','RL4','RL7', 'RL4 y RL7']), 
    widget=SQLFORM.widgets.checkboxes.widget, label=T('Control')),
    Field('f_peligrosidad', 'list:string',requires=IS_IN_SET(['Inflamable','Tóxico','Tóxico para el ambiente','Corrosivo','Comburente','Nocivo','Explosivo','Irritante'],multiple = True),
    widget=SQLFORM.widgets.checkboxes.widget, label=T('Peligrosidad')),
    # Hoja de seguridad (archivo pdf)
    Field('f_hds','upload',requires=IS_NULL_OR(IS_UPLOAD_FILENAME(extension='pdf')),label=T('Hoja de seguridad'), format='%(f_nombre)s'),
    auth.signature) # Agrega los campos adicionales created_by, created_on, modified_by, modified_on para los logs de la tabla

#db.t_sustancias.id.readable=False #Si se muestra en la forma, descomentar
#db.t_sustancias.id.writable=False
db.t_Sustancia.f_hds.readable=(auth.has_membership('Gestor de SMyDP') or auth.has_membership('WEBMASTER')) #-*-* Chequear permisos aqui
db.t_Sustancia._singular='Catálogo de Sustancias'
db.t_Sustancia._plural='Catálogo de Sustancias'


"""
if db(db.t_Sustancia).isempty():
    db.t_Sustancia.insert(f_nombre='Acetato de Etilo', f_cas='141-78-6', f_pureza='99', f_estado='Líquido', f_control='RL4', f_peligrosidad=['Inflamable','Irritante'])
    db.t_Sustancia.insert(f_nombre='Acetona', f_cas='67-64-1', f_pureza='99', f_estado='Líquido', f_control='RL4', f_peligrosidad=['Inflamable','Tóxico'])
    db.t_Sustancia.insert(f_nombre='Ácido Antranílico', f_cas='118-92-3', f_pureza='99', f_estado='Líquido', f_control='RL4', f_peligrosidad=['Inflamable','Comburente'])
    db.t_Sustancia.insert(f_nombre='Ácido Clorhídrico', f_cas='7647-01-0', f_pureza='37', f_estado='Líquido', f_control='RL4', f_peligrosidad=['Tóxico','Corrosivo'])
    db.t_Sustancia.insert(f_nombre='Ácido Fenilacético y sus sales', f_cas='103-82-2', f_pureza='99', f_estado='Líquido', f_control='RL4', f_peligrosidad=['Comburente'])
    db.t_Sustancia.insert(f_nombre='Ácido Nítrico', f_cas='7697-37-2', f_pureza='5', f_estado='Líquido', f_control='RL7', f_peligrosidad=['Tóxico','Irritante'])
    db.t_Sustancia.insert(f_nombre='Ácido Pícrico (trinitrofenol)', f_cas='88-89-1', f_pureza='3', f_estado='Sólido', f_control='RL7', f_peligrosidad=['Explosivo','Tóxico'])
    db.t_Sustancia.insert(f_nombre='Ácido Sulfúrico', f_cas='7664-93-9', f_pureza='97', f_estado='Líquido', f_control='RL4 y RL7', f_peligrosidad=['Corrosivo','Irritante'])
    db.t_Sustancia.insert(f_nombre='Aluminio en polvo', f_cas='7429-90-5', f_pureza='99', f_estado='Sólido', f_control='RL7', f_peligrosidad=['Inflamable'])
    db.t_Sustancia.insert(f_nombre='Amoníaco Anhídrico', f_cas='7664-41-7', f_pureza='99', f_estado='Líquido', f_control='RL4', f_peligrosidad=['Nocivo','Inflamable'])
    db.t_Sustancia.insert(f_nombre='Amoníaco en disolución acuosa', f_cas='001336-21-6', f_pureza='25', f_estado='Líquido', f_control='RL4', f_peligrosidad=['Tóxico','Corrosivo'])
    db.t_Sustancia.insert(f_nombre='Anhídrico acético', f_cas='108-24-7', f_pureza='99', f_estado='Líquido', f_control='RL4', f_peligrosidad=['Inflamable','Nocivo'])
    db.t_Sustancia.insert(f_nombre='Azidas (de sodio)', f_cas='26628-22-8', f_pureza='99', f_estado='Sólido', f_control='RL7', f_peligrosidad=['Tóxico'])
    db.t_Sustancia.insert(f_nombre='Benceno', f_cas='71-43-2', f_pureza='99', f_estado='Líquido', f_control='RL7', f_peligrosidad=['Tóxico','Inflamable'])
    db.t_Sustancia.insert(f_nombre='Butanona (metilcetona)', f_cas='78-93-3', f_pureza='99', f_estado='Líquido', f_control='RL4', f_peligrosidad=['Inflamable','Tóxico'])
    db.t_Sustancia.insert(f_nombre='Carbonato de Sodio', f_cas='497-19-8', f_pureza='99', f_estado='Sólido', f_control='RL4', f_peligrosidad=['Corrosivo','Irritante'])
    db.t_Sustancia.insert(f_nombre='Clorato de Potasio', f_cas='3811-04-9', f_pureza='99', f_estado='Sólido', f_control='RL7', f_peligrosidad=['Comburente','Tóxico'])
    db.t_Sustancia.insert(f_nombre='Clorato de Sodio', f_cas='7775-09-9', f_pureza='99', f_estado='Sólido', f_control='RL7', f_peligrosidad=['Comburente','Tóxico'])
    db.t_Sustancia.insert(f_nombre='Cloroformo', f_cas='67-66-3', f_pureza='99', f_estado='Líquido', f_control='RL4', f_peligrosidad=['Nocivo','Tóxico'])
    db.t_Sustancia.insert(f_nombre='Diclorometano', f_cas='75-09-2', f_pureza='99', f_estado='Líquido', f_control='RL4', f_peligrosidad=['Nocivo','Inflamable'])
    db.t_Sustancia.insert(f_nombre='Dinitrofenol', f_cas='51-28-5', f_pureza='99', f_estado='Sólido', f_control='RL7', f_peligrosidad=['Nocivo','Tóxico'])
    db.t_Sustancia.insert(f_nombre='Dinitrotolueno', f_cas='606-20-2', f_pureza='99', f_estado='Sólido', f_control='RL7', f_peligrosidad=['Nocivo'])
    db.t_Sustancia.insert(f_nombre='Etanol', f_cas='64-17-5', f_pureza='99', f_estado='Líquido', f_control='RL4', f_peligrosidad=['Inflamable','Irritante'])
    db.t_Sustancia.insert(f_nombre='Eter Etílico', f_cas='60-29-7', f_pureza='99', f_estado='Líquido', f_control='RL4', f_peligrosidad=['Explosivo','Nocivo'])
    db.t_Sustancia.insert(f_nombre='Fósforo blanco', f_cas='7723-14-0', f_pureza='99', f_estado='Sólido', f_control='RL7', f_peligrosidad=['Inflamable','Nocivo'])
    db.t_Sustancia.insert(f_nombre='Fulminato de Mercurio', f_cas='', f_pureza='', f_estado='', f_control='RL7', f_peligrosidad=['N/A'])
    db.t_Sustancia.insert(f_nombre='Heptano', f_cas='142-82-5', f_pureza='99', f_estado='Líquido', f_control='RL4', f_peligrosidad=['Inflamable','Irritante'])
    db.t_Sustancia.insert(f_nombre='Hexano', f_cas='110-54-3', f_pureza='99', f_estado='Líquido', f_control='RL4', f_peligrosidad=['Inflamable'])
    db.t_Sustancia.insert(f_nombre='Hidrogenocarbonato (Bicarbonato) de Sodio', f_cas='144-55-8', f_pureza='99', f_estado='Sólido', f_control='RL4', f_peligrosidad=['Irritante'])
    db.t_Sustancia.insert(f_nombre='Hipoclorito de calcio', f_cas='7778-54-3', f_pureza='68', f_estado='Sólido', f_control='RL7', f_peligrosidad=['Corrosivo','Irritante'])
    db.t_Sustancia.insert(f_nombre='Hipoclorito de Sodio', f_cas='7681-52-9', f_pureza='', f_estado='Líquido', f_control='RL7', f_peligrosidad=['Corrosivo','Tóxico'])
    db.t_Sustancia.insert(f_nombre='Metanol', f_cas='67-56-1', f_pureza='99', f_estado='Líquido', f_control='RL4', f_peligrosidad=['Inflamable','Irritante'])
    db.t_Sustancia.insert(f_nombre='Nitrato de Amonio (salitre de chile)', f_cas='6484-52-2', f_pureza='99', f_estado='Sólido', f_control='RL7', f_peligrosidad=['Explosivo'])
    db.t_Sustancia.insert(f_nombre='Nitrato de Bismuto', f_cas='7697-37-2', f_pureza='99', f_estado='Sólido', f_control='RL7', f_peligrosidad=['Corrosivo','Tóxico'])
    db.t_Sustancia.insert(f_nombre='Nitrato de Calcio', f_cas='13477-34-4', f_pureza='99', f_estado='Sólido', f_control='RL7', f_peligrosidad=['Tóxico'])
    db.t_Sustancia.insert(f_nombre='Nitrato de Plata', f_cas='7761-88-8', f_pureza='99', f_estado='Sólido', f_control='RL7', f_peligrosidad=['Corrosivo','Tóxico'])
    db.t_Sustancia.insert(f_nombre='Nitrato de Plomo', f_cas='10099-74-8', f_pureza='99', f_estado='Sólido', f_control='RL7', f_peligrosidad=['Tóxico'])
    db.t_Sustancia.insert(f_nombre='Nitrato de Potasio', f_cas='7757-79-1', f_pureza='99', f_estado='Sólido', f_control='RL7', f_peligrosidad=['Comburente','Tóxico'])
    db.t_Sustancia.insert(f_nombre='Nitrato de Sodio', f_cas='7631-99-4', f_pureza='99', f_estado='Sólido', f_control='RL7', f_peligrosidad=['Comburente','Tóxico'])
    db.t_Sustancia.insert(f_nombre='Nitrito de Sodio', f_cas='7632-00-0', f_pureza='99', f_estado='Sólido', f_control='RL7', f_peligrosidad=['Comburente','Tóxico'])
    db.t_Sustancia.insert(f_nombre='Nitrobenceno', f_cas='98-95-3', f_pureza='99', f_estado='Líquido', f_control='RL7', f_peligrosidad=['Nocivo','Tóxico'])
    db.t_Sustancia.insert(f_nombre='Nitrocelulosa', f_cas='9004-70-0', f_pureza='12', f_estado='Sólido', f_control='RL7', f_peligrosidad=['Inflamable'])
    db.t_Sustancia.insert(f_nombre='Nitroglicerina', f_cas='55-63-0', f_pureza='1', f_estado='Sólido', f_control='RL7', f_peligrosidad=['Explosivo'])
    db.t_Sustancia.insert(f_nombre='Perclorato de Potasio', f_cas='7778-74-7', f_pureza='99', f_estado='Sólido', f_control='RL7', f_peligrosidad=['Comburente','Tóxico'])
    db.t_Sustancia.insert(f_nombre='Perclorato de Sodio', f_cas='7601-89-0', f_pureza='99', f_estado='Sólido', f_control='RL7', f_peligrosidad=['Comburente','Nocivo'])
    db.t_Sustancia.insert(f_nombre='Permanganato de Potasio', f_cas='7722-64-7', f_pureza='99', f_estado='Sólido', f_control='RL4 y RL7', f_peligrosidad=['Comburente','Corrosivo'])
    db.t_Sustancia.insert(f_nombre='Sesquicarbonato de Sodio', f_cas='6106-20-3', f_pureza='99', f_estado='Sólido', f_control='RL4', f_peligrosidad=['Corrosivo','Irritante'])
    db.t_Sustancia.insert(f_nombre='Sulfato de Amonio', f_cas='7783-20-2', f_pureza='99', f_estado='Sólido', f_control='RL7', f_peligrosidad=['Corrosivo','Irritante'])
    db.t_Sustancia.insert(f_nombre='Sulfato de Magnesio', f_cas='7487-88-9', f_pureza='65', f_estado='Sólido', f_control='RL7', f_peligrosidad=['Irritante'])
    db.t_Sustancia.insert(f_nombre='Sulfuro de Potasio', f_cas='1312-73-8', f_pureza='99', f_estado='Sólido', f_control='RL7', f_peligrosidad=['Inflamable','Corrosivo'])
    db.t_Sustancia.insert(f_nombre='Tetrahidrofurano', f_cas='109-99-9', f_pureza='99', f_estado='Líquido', f_control='RL4', f_peligrosidad=['Inflamable','Irritante'])
    db.t_Sustancia.insert(f_nombre='Tolueno', f_cas='108-88-3', f_pureza='99', f_estado='Líquido', f_control='RL4', f_peligrosidad=['Inflamable','Tóxico'])
    db.t_Sustancia.insert(f_nombre='Trinitrotolueno (TNT)', f_cas='118-96-7', f_pureza='99', f_estado='Sólido', f_control='RL7', f_peligrosidad=['Explosivo','Nocivo'])
    db.t_Sustancia.insert(f_nombre='Urea', f_cas='57-13-6 ', f_pureza='', f_estado='Sólido', f_control='RL7', f_peligrosidad=['Irritante','Comburente'])
    db.t_Sustancia.insert(f_nombre='4-metilpentan-2-ona (Metilisobutilcetona)', f_cas='108-10-1', f_pureza='99', f_estado='Líquido', f_control='RL4', f_peligrosidad=['Tóxico'])
    db.t_Sustancia.insert(f_nombre='Fósforos rojos o amorfos', f_cas='7723-14-0', f_pureza='99', f_estado='Sólido', f_control='N/A', f_peligrosidad=['Inflamable','Nocivo'])
"""