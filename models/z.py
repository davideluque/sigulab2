##############################################################################
#
# ESTE ARCHIVO SE ENCARGARA DE POBLAR LA BASE DE DATOS CON DATOS BASICOS.
# EL NOMBRE ES "Z" DEBIDO A QUE ESTE ES EL ULTIMO MODELO QUE DEBE CORRER.
# (ALFABETICAMENTE)
##############################################################################

if db(db.auth_user).isempty():
    """
    Usuario Básico y obligatorio: Super usuario
    El resto de los usuarios son necesarios para la creación de dependencias y
    asignación de roles.

    La inserción de los usuarios registrados en auth_user en la tabla de
    t_Personal es estrictamente necesaria pues los objetos del modulo de Servicios
    buscan  las dependencias de los usuarios buscando una coincidencia del
    usuario con la tabla de Personal ya que esta tabla es la que guarda el
    registro y no auth_user"""

    """ Super Usuario """
    db.auth_user.insert(first_name="Super Usuario", last_name="", email='sigulabusb@gmail.com',
                                            password=db.auth_user.password.validate('s1gul4bu5b')[0])

    """ Cliente Interno """
    db.auth_user.insert(first_name="Funindes", last_name="", email='funindes@usb.ve',
        password=db.auth_user.password.validate('0000')[0])

    """ Asistente del Director """
    db.auth_user.insert(first_name="Asistente Dirección", last_name="",
        email='asis-ulab@usb.ve', password=db.auth_user.password.validate('0000')[0])

    """ Gestor de Sustancias """
    db.auth_user.insert(first_name="Gestor de Sustancias", last_name="", email='ulab-smdp@usb.ve',
        password=db.auth_user.password.validate('0000')[0])

    """Usuarios representantes de dependencias. Es necesario añadir estos
    usuarios mediante este servicio automatizado hasta que se tenga la gestión
    de dependencias. En ese caso solo hará falta añadir la dirección y
    posteriormente todas las dependencias se podrán registrar desde la
    dirección hacia abajo y de igual forma los usuarios. Por favor, al
    realizar el módulo de gestión de dependencias eliminar todos los registros
    innecesarios aquí encontrados para aumentar los niveles de seguridad de
    este sistema."""

    # ---- Dirección
    db.auth_user.insert(first_name="Dirección", last_name="", email='ulab@usb.ve',
                                            password=db.auth_user.password.validate('0000')[0])

    # ---- Coordinaciones

    # Coordinación de Adquisiciones
    db.auth_user.insert(first_name="Coordinación de Adquisiciones", last_name="",
        email='ulab-adquisicion@usb.ve',password=db.auth_user.password.validate('0000')[0])
    # Coordinación de la Calidad
    db.auth_user.insert(first_name="Coordinación de la Calidad", last_name="",
        email='ulab-calidad@usb.ve', password=db.auth_user.password.validate('0000')[0])
    # Coordinación de Importaciones
    db.auth_user.insert(first_name="Coordinación de Importaciones", last_name="",
        email='ulab-importaciones@usb.ve', password=db.auth_user.password.validate('0000')[0])
    # Unidad de Administración
    db.auth_user.insert(first_name="Unidad de Administración", last_name="",
        email='ulab-administracion@usb.ve', password=db.auth_user.password.validate('0000')[0])
    # Oficina de Proteccion Radiologica
    db.auth_user.insert(first_name="Oficina de Proteccion Radiológica", last_name="",
        email='ulab-pradiologica@usb.ve', password=db.auth_user.password.validate('0000')[0])

    # ---- Laboratorios

    # Laboratorio A
    db.auth_user.insert(first_name="Laboratorio A", last_name="", email='usb-laba@usb.ve',
                        password=db.auth_user.password.validate('0000')[0])
    # Laboratorio B
    db.auth_user.insert(first_name="Laboratorio B", last_name="", email='usb-labb@usb.ve',
                        password=db.auth_user.password.validate('0000')[0])
    # Laboratorio C
    db.auth_user.insert(first_name="Laboratorio C", last_name="", email='usb-labc@usb.ve',
                        password=db.auth_user.password.validate('0000')[0])
    # Laboratorio D
    db.auth_user.insert(first_name="Laboratorio D", last_name="", email='usb-labd@usb.ve',
                        password=db.auth_user.password.validate('0000')[0])
    # Laboratorio E
    db.auth_user.insert(first_name="Laboratorio E", last_name="", email='usb-labe@usb.ve',
                        password=db.auth_user.password.validate('0000')[0])
    # Laboratorio F
    db.auth_user.insert(first_name="Laboratorio F", last_name="", email='usb-labf@usb.ve',
                        password=db.auth_user.password.validate('0000')[0])
    # Laboratorio G
    db.auth_user.insert(first_name="Laboratorio G", last_name="", email='usb-labg@usb.ve',
                        password=db.auth_user.password.validate('0000')[0])

    # ---- Jefes de Laboratorio
    # NOTA: Los correos de los jefes de Laboratorio NO existen. Estos correos deberían ser
    # los de cada jefe en particular. Pero en cualquier caso, estos usuarios deberían agregarse
    # a través del módulo de Personal como usuarios regulares.

    # Jefatura Laboratorio A
    db.auth_user.insert(first_name="Jefe Laboratorio A", last_name="", email='jefe-usb-laba@usb.ve',
                        password=db.auth_user.password.validate('0000')[0])
    # Jefatura Laboratorio B
    db.auth_user.insert(first_name="Jefe Laboratorio B", last_name="", email='jefe-usb-labb@usb.ve',
                        password=db.auth_user.password.validate('0000')[0])
    # Jefatura Laboratorio C
    db.auth_user.insert(first_name="Jefe Laboratorio C", last_name="", email='jefe-usb-labc@usb.ve',
                        password=db.auth_user.password.validate('0000')[0])
    # Jefatura Laboratorio D
    db.auth_user.insert(first_name="Jefe Laboratorio D", last_name="", email='jefe-usb-labd@usb.ve',
                        password=db.auth_user.password.validate('0000')[0])
    # Jefatura Laboratorio E
    db.auth_user.insert(first_name="Jefe Laboratorio E", last_name="", email='jefe-usb-labe@usb.ve',
                        password=db.auth_user.password.validate('0000')[0])
    # Jefatura Laboratorio F
    db.auth_user.insert(first_name="Jefe Laboratorio F", last_name="", email='jefe-usb-labf@usb.ve',
                        password=db.auth_user.password.validate('0000')[0])
    # Jefatura Laboratorio G
    db.auth_user.insert(first_name="Jefe Laboratorio G", last_name="", email='jefe-usb-labg@usb.ve',
                        password=db.auth_user.password.validate('0000')[0])

    # ---- Unidades de apoyo
    # NOTA: Los correos de los usuarios de apoyo de Laboratorio NO existen. Estos correos deberían
    # ser los de cada encargado en particular. Pero en cualquier caso, estos usuarios deberían 
    # agregarse a través del módulo de Personal como usuarios regulares.

    # Apoyo Laboratorio A
    db.auth_user.insert(first_name="Apoyo Laboratorio A", last_name="", email='apoyo-usb-laba@usb.ve',
                        password=db.auth_user.password.validate('0000')[0])
    # Apoyo Laboratorio B
    db.auth_user.insert(first_name="Apoyo Laboratorio B", last_name="", email='apoyo-usb-labb@usb.ve',
                        password=db.auth_user.password.validate('0000')[0])
    # Apoyo Laboratorio C
    db.auth_user.insert(first_name="Apoyo Laboratorio C", last_name="", email='apoyo-usb-labc@usb.ve',
                        password=db.auth_user.password.validate('0000')[0])
    # Apoyo Laboratorio D
    db.auth_user.insert(first_name="Apoyo Laboratorio D", last_name="", email='apoyo-usb-labd@usb.ve',
                        password=db.auth_user.password.validate('0000')[0])
    # Apoyo Laboratorio E
    db.auth_user.insert(first_name="Apoyo Laboratorio E", last_name="", email='apoyo-usb-labe@usb.ve',
                        password=db.auth_user.password.validate('0000')[0])
    # Apoyo Laboratorio F
    db.auth_user.insert(first_name="Apoyo Laboratorio F", last_name="", email='apoyo-usb-labf@usb.ve',
                        password=db.auth_user.password.validate('0000')[0])
    # Apoyo Laboratorio G
    db.auth_user.insert(first_name="Apoyo Laboratorio G", last_name="", email='apoyo-usb-labg@usb.ve',
                        password=db.auth_user.password.validate('0000')[0])

# Sedes

if db(db.sedes).isempty():
	db.sedes.insert(nombre="Sartenejas")
	db.sedes.insert(nombre="Litoral")

# Dependencias

if db(db.dependencias).isempty():

	sartenejas = db(db.sedes.nombre=="Sartenejas").select(db.sedes.ALL).first().id
	litoral = db(db.sedes.nombre=="Litoral").select(db.sedes.ALL).first().id
	# Direccion
	user = db(db.auth_user.email == 'ulab@usb.ve').select()[0].id
	db.dependencias.insert(nombre='DIRECCIÓN', id_sede=sartenejas, id_jefe_dependencia=user,
		codigo_registro="UL")

	direccionid = db(db.dependencias.nombre == 'DIRECCIÓN').select()[0].id

	# Laboratorios

	# Laboratorio A
	user = db(db.auth_user.email == 'usb-laba@usb.ve').select()[0].id
	db.dependencias.insert(nombre='LABORATORIO A', id_sede=sartenejas,
		unidad_de_adscripcion=direccionid, id_jefe_dependencia=user,
		codigo_registro="ULLA")

	# Laboratorio B
	user = db(db.auth_user.email == 'usb-labb@usb.ve').select()[0].id
	db.dependencias.insert(nombre='LABORATORIO B', id_sede=sartenejas,
		unidad_de_adscripcion=direccionid, id_jefe_dependencia=user,
		codigo_registro="ULLB")

	# Laboratorio C
	user = db(db.auth_user.email == 'usb-labc@usb.ve').select()[0].id
	db.dependencias.insert(nombre='LABORATORIO C', id_sede=sartenejas,
		unidad_de_adscripcion=direccionid, id_jefe_dependencia=user,
		codigo_registro="ULLC")

	# Laboratorio D
	user = db(db.auth_user.email == 'usb-labd@usb.ve').select()[0].id
	db.dependencias.insert(nombre='LABORATORIO D', id_sede=sartenejas,
		unidad_de_adscripcion=direccionid, id_jefe_dependencia=user,
		codigo_registro="ULLD")

	# Laboratorio E
	user = db(db.auth_user.email == 'usb-labe@usb.ve').select()[0].id
	db.dependencias.insert(nombre='LABORATORIO E', id_sede=sartenejas,
		unidad_de_adscripcion=direccionid, id_jefe_dependencia=user,
		codigo_registro="ULLE")

	# Laboratorio F
	user = db(db.auth_user.email == 'usb-labf@usb.ve').select()[0].id
	db.dependencias.insert(nombre='LABORATORIO F', id_sede=sartenejas,
		unidad_de_adscripcion=direccionid, id_jefe_dependencia=user,
		codigo_registro="ULLF")

	# Laboratorio G
	user = db(db.auth_user.email == 'usb-labg@usb.ve').select()[0].id
	db.dependencias.insert(nombre='LABORATORIO G', id_sede=litoral,
		unidad_de_adscripcion=direccionid, id_jefe_dependencia=user,
		codigo_registro="ULLG")

    # Jefaturas
	labaid = db(db.dependencias.nombre == 'LABORATORIO A').select()[0].id
	labbid = db(db.dependencias.nombre == 'LABORATORIO B').select()[0].id
	labcid = db(db.dependencias.nombre == 'LABORATORIO C').select()[0].id
	labdid = db(db.dependencias.nombre == 'LABORATORIO D').select()[0].id
	labeid = db(db.dependencias.nombre == 'LABORATORIO E').select()[0].id
	labfid = db(db.dependencias.nombre == 'LABORATORIO F').select()[0].id
	labgid = db(db.dependencias.nombre == 'LABORATORIO G').select()[0].id

	# Jefatura Laboratorio A
	user = db(db.auth_user.email == 'jefe-usb-laba@usb.ve').select()[0].id
	db.dependencias.insert(nombre='JEFATURA LABORATORIO A', id_sede=sartenejas,
		unidad_de_adscripcion=labaid, id_jefe_dependencia=user,
		codigo_registro="ULLAJ")

    # Jefatura Laboratorio B
	user = db(db.auth_user.email == 'jefe-usb-labb@usb.ve').select()[0].id
	db.dependencias.insert(nombre='JEFATURA LABORATORIO B', id_sede=sartenejas,
		unidad_de_adscripcion=labbid, id_jefe_dependencia=user,
		codigo_registro="ULLBJ")

	# Jefatura Laboratorio C
	user = db(db.auth_user.email == 'jefe-usb-labc@usb.ve').select()[0].id
	db.dependencias.insert(nombre='JEFATURA LABORATORIO C', id_sede=sartenejas,
		unidad_de_adscripcion=labcid, id_jefe_dependencia=user,
		codigo_registro="ULLCJ")

	# Jefatura Laboratorio D
	user = db(db.auth_user.email == 'jefe-usb-labd@usb.ve').select()[0].id
	db.dependencias.insert(nombre='JEFATURA LABORATORIO D', id_sede=sartenejas,
		unidad_de_adscripcion=labdid, id_jefe_dependencia=user,
		codigo_registro="ULLDJ")

	# Jefatura Laboratorio E
	user = db(db.auth_user.email == 'jefe-usb-labe@usb.ve').select()[0].id
	db.dependencias.insert(nombre='JEFATURA LABORATORIO E', id_sede=sartenejas,
		unidad_de_adscripcion=labeid, id_jefe_dependencia=user,
		codigo_registro="ULLEJ")

	# Jefatura Laboratorio F
	user = db(db.auth_user.email == 'jefe-usb-labf@usb.ve').select()[0].id
	db.dependencias.insert(nombre='JEFATURA LABORATORIO F', id_sede=sartenejas,
		unidad_de_adscripcion=labfid, id_jefe_dependencia=user,
		codigo_registro="ULLFJ")

	# Jefatura Laboratorio G
	user = db(db.auth_user.email == 'jefe-usb-labg@usb.ve').select()[0].id
	db.dependencias.insert(nombre='JEFATURA LABORATORIO G', id_sede=litoral,
		unidad_de_adscripcion=labgid, id_jefe_dependencia=user,
		codigo_registro="ULLGJ")

	# Unidades de Apoyo

	# Unidad de Apoyo Laboratorio A
	user = db(db.auth_user.email == 'apoyo-usb-laba@usb.ve').select()[0].id
	db.dependencias.insert(nombre='UNIDAD DE APOYO LABORATORIO A', id_sede=sartenejas,
		unidad_de_adscripcion=labaid, id_jefe_dependencia=user,
		codigo_registro="ULLAA")

    # Unidad de Apoyo Laboratorio B
	user = db(db.auth_user.email == 'apoyo-usb-labb@usb.ve').select()[0].id
	db.dependencias.insert(nombre='UNIDAD DE APOYO LABORATORIO B', id_sede=sartenejas,
		unidad_de_adscripcion=labbid, id_jefe_dependencia=user,
		codigo_registro="ULLBA")

	# Unidad de Apoyo Laboratorio C
	user = db(db.auth_user.email == 'apoyo-usb-labc@usb.ve').select()[0].id
	db.dependencias.insert(nombre='UNIDAD DE APOYO LABORATORIO C', id_sede=sartenejas,
		unidad_de_adscripcion=labcid, id_jefe_dependencia=user,
		codigo_registro="ULLCA")

	# Unidad de Apoyo Laboratorio D
	user = db(db.auth_user.email == 'apoyo-usb-labd@usb.ve').select()[0].id
	db.dependencias.insert(nombre='UNIDAD DE APOYO LABORATORIO D', id_sede=sartenejas,
		unidad_de_adscripcion=labdid, id_jefe_dependencia=user,
		codigo_registro="ULLDA")

	# Unidad de Apoyo Laboratorio E
	user = db(db.auth_user.email == 'apoyo-usb-labe@usb.ve').select()[0].id
	db.dependencias.insert(nombre='UNIDAD DE APOYO LABORATORIO E', id_sede=sartenejas,
		unidad_de_adscripcion=labeid, id_jefe_dependencia=user,
		codigo_registro="ULLEA")

	# Unidad de Apoyo Laboratorio F
	user = db(db.auth_user.email == 'apoyo-usb-labf@usb.ve').select()[0].id
	db.dependencias.insert(nombre='UNIDAD DE APOYO LABORATORIO F', id_sede=sartenejas,
		unidad_de_adscripcion=labfid, id_jefe_dependencia=user,
		codigo_registro="ULLFA")

	# Unidad de Apoyo Laboratorio G
	user = db(db.auth_user.email == 'apoyo-usb-labg@usb.ve').select()[0].id
	db.dependencias.insert(nombre='UNIDAD DE APOYO LABORATORIO G', id_sede=litoral,
		unidad_de_adscripcion=labgid, id_jefe_dependencia=user,
		codigo_registro="ULLGA")

	# Coordinaciones

	# Unidad de Administración
	user = db(db.auth_user.email == 'ulab-administracion@usb.ve').select()[0].id
	db.dependencias.insert(nombre='UNIDAD DE ADMINISTRACIÓN', id_sede=sartenejas,
		unidad_de_adscripcion=direccionid, id_jefe_dependencia=user,
		codigo_registro="UL03")

	# Coordinación de Adquisiciones
	user = db(db.auth_user.email == 'ulab-adquisicion@usb.ve').select()[0].id
	db.dependencias.insert(nombre='COORDINACIÓN DE ADQUISICIONES', id_sede=sartenejas,
		unidad_de_adscripcion=direccionid, id_jefe_dependencia=user,
		codigo_registro="UL01")

	# Coordinación de Importaciones
	user = db(db.auth_user.email == 'ulab-importaciones@usb.ve').select()[0].id
	db.dependencias.insert(nombre='COORDINACIÓN DE IMPORTACIONES', id_sede=sartenejas,
		unidad_de_adscripcion=direccionid, id_jefe_dependencia=user,
		codigo_registro="UL02")

	# Coordinación de la Calidad
	user = db(db.auth_user.email == 'ulab-calidad@usb.ve').select()[0].id
	db.dependencias.insert(nombre='COORDINACIÓN DE LA CALIDAD', id_sede=sartenejas,
		unidad_de_adscripcion=direccionid, id_jefe_dependencia=user,
		codigo_registro="UL04")

	# Protección Radiológica
	user = db(db.auth_user.email == 'ulab-pradiologica@usb.ve').select()[0].id
	db.dependencias.insert(nombre='OFICINA DE PROTECCIÓN RADIOLÓGICA', id_sede=sartenejas,
		unidad_de_adscripcion=direccionid, id_jefe_dependencia=user,
		codigo_registro="UL05")

	######## MODIFICACION INVENTARIO PRUEBA
	# Se agrega una seccion y un espacio para el Lab A para poder realizar pruebas
	# Esto se debe borrar antes de pasar a produccion

	labA = db(db.dependencias.codigo_registro == "ULLA").select()[0].id
	user = db(db.auth_user.email == 'usb-laba@usb.ve').select()[0].id

	db.dependencias.insert(nombre='Alta Tension', id_sede=sartenejas, 
		unidad_de_adscripcion=labA, id_jefe_dependencia=user, 
		codigo_registro="ALT")
	alt = db(db.dependencias.codigo_registro == "ALT").select()[0].id

	db.dependencias.insert(nombre='Mecanica de Fluidos', id_sede=sartenejas, 
		unidad_de_adscripcion=labA, id_jefe_dependencia=user, 
		codigo_registro="MCF")
	mcf = db(db.dependencias.codigo_registro == "MCF").select()[0].id

	db.espacios_fisicos.insert(codigo="ALT1", uso="Clases", 
		dependencia=alt)
	db.espacios_fisicos.insert(codigo="ALT2", uso="Clases", 
		dependencia=alt)
	db.espacios_fisicos.insert(codigo="ALT3", uso="Clases", 
		dependencia=alt)

	db.espacios_fisicos.insert(codigo="MCF1", uso="Clases", 
		dependencia=mcf)
	db.espacios_fisicos.insert(codigo="MCF2", uso="Clases", 
		dependencia=mcf)
	######## MODIFICACION INVENTARIO PRUEBA


# Cargos
if db(db.auth_group).isempty():

        db.auth_group.insert(role='WEBMASTER',description='Super Usuario')
        db.auth_group.insert(role='DIRECTOR',description='Director')
        db.auth_group.insert(role='ASISTENTE DEL DIRECTOR',description='Asistente del Director')
        db.auth_group.insert(role='COORDINADOR',description='Coordinación')
        db.auth_group.insert(role='JEFE DE LABORATORIO',description='Jefe de Laboratorio')
        db.auth_group.insert(role='JEFE DE SECCIÓN',description='Jefe de Sección')
        db.auth_group.insert(role='TÉCNICO',description='Técnico')
        db.auth_group.insert(role='PERSONAL DE DEPENDENCIA',description='Personal de dependencia')
        db.auth_group.insert(role='GESTOR DE SMyDP',description='Gestor de SMyDP')
        db.auth_group.insert(role='GESTOR DE PERSONAL',description='Gestor de Personal')
        db.auth_group.insert(role='CLIENTE INTERNO',description='Cliente Interno')
        db.auth_group.insert(role='PERSONAL INTERNO',description='Personal Interno')

# Fichas de personal
if db(db.t_Personal).isempty():
    """La inserción de los usuarios registrados en auth_user en la tabla de
    Personal es estrictamente necesaria pues los objetos del modulo de Servicios
    buscan las dependencias de los usuarios a través de una coincidencia del
    usuario con la tabla de Personal ya que esta tabla es la que guarda el
    la dependencia de cada usuario y no auth_user"""

    dep = db(db.dependencias.nombre == 'DIRECCIÓN').select()[0].id

    """ Super Usuario """
    user = db(db.auth_user.email == 'sigulabusb@gmail.com').select()[0].id
    rol = db(db.auth_group.role=='WEBMASTER').select()[0].id

    db.t_Personal.insert(
        f_nombre="Super", f_apellido="", f_gremio="Administrativo", f_cargo="Super Usuario",
        f_ci="0", f_telefono="0", f_celular="0", f_contacto_emergencia=None,
        f_email="sigulabusb@gmail.com", f_direccion=None, f_ubicacion=None, f_pagina_web=None,
        f_estatus=None, f_categoria=None, f_fecha_ingreso=None, f_fecha_salida=None,
        f_fecha_ingreso_usb=None, f_fecha_ingreso_ulab=None, f_fecha_ingreso_admin_publica=None,
        f_condicion=None, f_rol=rol, f_usuario=user, f_dependencia=dep, f_validado=True, f_es_supervisor=True
    )
    """ Cliente Interno """
    user = db(db.auth_user.email == 'funindes@usb.ve').select()[0].id
    db.t_Personal.insert(
        f_nombre="Funindes", f_apellido="", f_gremio="Administrativo", f_cargo="Cliente Interno",
        f_ci="1", f_telefono="1", f_celular="1", f_contacto_emergencia=None,
        f_email='funindes@usb.ve', f_direccion=None, f_ubicacion=None, f_pagina_web=None,
        f_estatus=None, f_categoria=None, f_fecha_ingreso=None, f_fecha_salida=None,
        f_fecha_ingreso_usb=None, f_fecha_ingreso_ulab=None, f_fecha_ingreso_admin_publica=None,
        f_condicion=None, f_rol=rol, f_usuario=user, f_dependencia=dep, f_validado=True, f_es_supervisor=True
    )

    """ Asistente Dirección """
    user = db(db.auth_user.email == 'asis-ulab@usb.ve').select()[0].id
    db.t_Personal.insert(
        f_nombre="Asistente Dirección", f_apellido="", f_gremio="Administrativo", f_cargo="Cliente Interno",
        f_ci="2", f_telefono="2", f_celular="2", f_contacto_emergencia=None,
        f_email='asis-ulab@usb.ve', f_direccion=None, f_ubicacion=None, f_pagina_web=None,
        f_estatus=None, f_categoria=None, f_fecha_ingreso=None, f_fecha_salida=None,
        f_fecha_ingreso_usb=None, f_fecha_ingreso_ulab=None, f_fecha_ingreso_admin_publica=None,
        f_condicion=None, f_rol=rol, f_usuario=user, f_dependencia=dep, f_validado=True, f_es_supervisor=True
        )


    """ Gestor de Sustancias """
    user = db(db.auth_user.email == 'ulab-smdp@usb.ve').select()[0].id
    db.t_Personal.insert(
        f_nombre="Gestor de Sustancias", f_apellido="", f_gremio="Administrativo", f_cargo="Gestor de Sustancias",
        f_ci="3", f_telefono="3", f_celular="3", f_contacto_emergencia=None,
        f_email='ulab-smdp@usb.ve', f_direccion=None, f_ubicacion=None, f_pagina_web=None,
        f_estatus=None, f_categoria=None, f_fecha_ingreso=None, f_fecha_salida=None,
        f_fecha_ingreso_usb=None, f_fecha_ingreso_ulab=None, f_fecha_ingreso_admin_publica=None,
        f_condicion=None, f_rol=rol, f_usuario=user, f_dependencia=dep, f_validado=True, f_es_supervisor=True
        )

    """ Gestor de Personal """
    user = db(db.auth_user.email == 'asis-ulab@usb.ve').select()[0].id
    db.t_Personal.insert(
        f_nombre="Gestor de Personal", f_apellido="", f_gremio="Administrativo", f_cargo="Gestor de Personal",
        f_ci="3", f_telefono="3", f_celular="3", f_contacto_emergencia=None,
        f_email='asis-ulab@usb.ve', f_direccion=None, f_ubicacion=None, f_pagina_web=None,
        f_estatus=None, f_categoria=None, f_fecha_ingreso=None, f_fecha_salida=None,
        f_fecha_ingreso_usb=None, f_fecha_ingreso_ulab=None, f_fecha_ingreso_admin_publica=None,
        f_condicion=None, f_rol=rol, f_usuario=user, f_dependencia=dep, f_validado=True, f_es_supervisor=True
        )

    """ Director """
    user = db(db.auth_user.email == 'ulab@usb.ve').select()[0].id
    db.t_Personal.insert(
        f_nombre="Director", f_apellido="", f_gremio="Administrativo", f_cargo="Director",
        f_ci="4", f_telefono="4", f_celular="4", f_contacto_emergencia=None,
        f_email='ulab@usb.ve', f_direccion=None, f_ubicacion=None, f_pagina_web=None,
        f_estatus=None, f_categoria=None, f_fecha_ingreso=None, f_fecha_salida=None,
        f_fecha_ingreso_usb=None, f_fecha_ingreso_ulab=None, f_fecha_ingreso_admin_publica=None,
        f_condicion=None, f_rol=rol, f_usuario=user, f_dependencia=dep, f_validado=True, f_es_supervisor=True
        )

    """ Coordinaciones """

    # Coordinación de Adquisiciones
    dep = db(db.dependencias.nombre == 'COORDINACIÓN DE ADQUISICIONES').select()[0].id
    user = db(db.auth_user.email == 'ulab-adquisicion@usb.ve').select()[0].id
    db.t_Personal.insert(
        f_nombre="Coordinador de Adquisiciones", f_apellido="", f_gremio="Administrativo", f_cargo="Coordinador",
        f_ci="5", f_telefono="5", f_celular="5", f_contacto_emergencia=None,
        f_email='ulab-adquisicion@usb.ve', f_direccion=None, f_ubicacion=None, f_pagina_web=None,
        f_estatus=None, f_categoria=None, f_fecha_ingreso=None, f_fecha_salida=None,
        f_fecha_ingreso_usb=None, f_fecha_ingreso_ulab=None, f_fecha_ingreso_admin_publica=None,
        f_condicion=None, f_rol=rol, f_usuario=user, f_dependencia=dep, f_validado=True, f_es_supervisor=True
        )

    # Coordinación de la Calidad
    dep = db(db.dependencias.nombre == 'COORDINACIÓN DE LA CALIDAD').select()[0].id
    user = db(db.auth_user.email == 'ulab-calidad@usb.ve').select()[0].id
    db.t_Personal.insert(
        f_nombre="Coordinador de Calidad", f_apellido="", f_gremio="Administrativo", f_cargo="Coordinador",
        f_ci="6", f_telefono="6", f_celular="6", f_contacto_emergencia=None,
        f_email='ulab-calidad@usb.ve', f_direccion=None, f_ubicacion=None, f_pagina_web=None,
        f_estatus=None, f_categoria=None, f_fecha_ingreso=None, f_fecha_salida=None,
        f_fecha_ingreso_usb=None, f_fecha_ingreso_ulab=None, f_fecha_ingreso_admin_publica=None,
        f_condicion=None, f_rol=rol, f_usuario=user, f_dependencia=dep, f_validado=True, f_es_supervisor=True
    )


    # Coordinación de Importaciones
    dep = db(db.dependencias.nombre == 'COORDINACIÓN DE IMPORTACIONES').select()[0].id
    user = db(db.auth_user.email == 'ulab-importaciones@usb.ve').select()[0].id
    db.t_Personal.insert(
        f_nombre="Coordinador de Importaciones", f_apellido="", f_gremio="Administrativo", f_cargo="Coordinador",
        f_ci="7", f_telefono="7", f_celular="7", f_contacto_emergencia=None,
        f_email='ulab-importaciones@usb.ve', f_direccion=None, f_ubicacion=None, f_pagina_web=None,
        f_estatus=None, f_categoria=None, f_fecha_ingreso=None, f_fecha_salida=None,
        f_fecha_ingreso_usb=None, f_fecha_ingreso_ulab=None, f_fecha_ingreso_admin_publica=None,
        f_condicion=None, f_rol=rol, f_usuario=user, f_dependencia=dep, f_validado=True, f_es_supervisor=True
        )

    """ Unidades """

    # Unidad de Administración
    dep = db(db.dependencias.nombre == 'UNIDAD DE ADMINISTRACIÓN').select()[0].id
    user = db(db.auth_user.email == 'ulab-administracion@usb.ve').select()[0].id
    db.t_Personal.insert(
        f_nombre="Unidad de Administración", f_apellido="", f_gremio="Administrativo", f_cargo="Coordinador",
        f_ci="8", f_telefono="8", f_celular="8", f_contacto_emergencia=None,
        f_email='ulab-administracion@usb.ve', f_direccion=None, f_ubicacion=None, f_pagina_web=None,
        f_estatus=None, f_categoria=None, f_fecha_ingreso=None, f_fecha_salida=None,
        f_fecha_ingreso_usb=None, f_fecha_ingreso_ulab=None, f_fecha_ingreso_admin_publica=None,
        f_condicion=None, f_rol=rol, f_usuario=user, f_dependencia=dep, f_validado=True, f_es_supervisor=True
    )
    # Oficina de Proteccion Radiologica
    dep = db(db.dependencias.nombre == 'DIRECCIÓN').select()[0].id
    user = db(db.auth_user.email == 'ulab-pradiologica@usb.ve').select()[0].id
    db.t_Personal.insert(
        f_nombre="Encargado de la Oficina de Proteccion Radiológica", f_apellido="", f_gremio="Administrativo", f_cargo="Coordinador",
        f_ci="9", f_telefono="9", f_celular="9", f_contacto_emergencia=None,
        f_email='ulab-pradiologica@usb.ve', f_direccion=None, f_ubicacion=None, f_pagina_web=None,
        f_estatus=None, f_categoria=None, f_fecha_ingreso=None, f_fecha_salida=None,
        f_fecha_ingreso_usb=None, f_fecha_ingreso_ulab=None, f_fecha_ingreso_admin_publica=None,
        f_condicion=None, f_rol=rol, f_usuario=user, f_dependencia=dep, f_validado=True, f_es_supervisor=True
    )


    """ Jefes de Laboratorios --- Tenian de categoria Tecnico, se cambio a gremio administrativo"""

    # Laboratorio A
    dep = db(db.dependencias.nombre == 'LABORATORIO A').select()[0].id
    user = db(db.auth_user.email == 'usb-laba@usb.ve').select()[0].id
    db.t_Personal.insert(
        f_nombre="Jefe del Laboratorio A", f_apellido="", f_gremio="Administrativo", f_cargo="Jefe de Laboratorio",
        f_ci="10", f_telefono="10", f_celular="10", f_contacto_emergencia=None,
        f_email='usb-laba@usb.ve', f_direccion=None, f_ubicacion=None, f_pagina_web=None,
        f_estatus=None, f_categoria=None, f_fecha_ingreso=None, f_fecha_salida=None,
        f_fecha_ingreso_usb=None, f_fecha_ingreso_ulab=None, f_fecha_ingreso_admin_publica=None,
        f_condicion=None, f_rol=rol, f_usuario=user, f_dependencia=dep, f_validado=True, f_es_supervisor=True
    )

    # Laboratorio B
    dep = db(db.dependencias.nombre == 'LABORATORIO B').select()[0].id
    user = db(db.auth_user.email == 'usb-labb@usb.ve').select()[0].id
    db.t_Personal.insert(
        f_nombre="Jefe del Laboratorio B", f_apellido="", f_gremio="Administrativo", f_cargo="Jefe de Laboratorio",
        f_ci="11", f_telefono="11", f_celular="11", f_contacto_emergencia=None,
        f_email='usb-labb@usb.ve', f_direccion=None, f_ubicacion=None, f_pagina_web=None,
        f_estatus=None, f_categoria=None, f_fecha_ingreso=None, f_fecha_salida=None,
        f_fecha_ingreso_usb=None, f_fecha_ingreso_ulab=None, f_fecha_ingreso_admin_publica=None,
        f_condicion=None, f_rol=rol, f_usuario=user, f_dependencia=dep, f_validado=True, f_es_supervisor=True
    )

    # Laboratorio C
    dep = db(db.dependencias.nombre == 'LABORATORIO C').select()[0].id
    user = db(db.auth_user.email == 'usb-labc@usb.ve').select()[0].id
    db.t_Personal.insert(
        f_nombre="Jefe del Laboratorio C", f_apellido="", f_gremio="Administrativo", f_cargo="Jefe de Laboratorio",
        f_ci="12", f_telefono="12", f_celular="12", f_contacto_emergencia=None,
        f_email='usb-labc@usb.ve', f_direccion=None, f_ubicacion=None, f_pagina_web=None,
        f_estatus=None, f_categoria=None, f_fecha_ingreso=None, f_fecha_salida=None,
        f_fecha_ingreso_usb=None, f_fecha_ingreso_ulab=None, f_fecha_ingreso_admin_publica=None,
        f_condicion=None, f_rol=rol, f_usuario=user, f_dependencia=dep, f_validado=True, f_es_supervisor=True
    )

    # Laboratorio D
    dep = db(db.dependencias.nombre == 'LABORATORIO D').select()[0].id
    user = db(db.auth_user.email == 'usb-labd@usb.ve').select()[0].id
    db.t_Personal.insert(
        f_nombre="Jefe del Laboratorio D", f_apellido="", f_gremio="Administrativo", f_cargo="Jefe de Laboratorio",
        f_ci="13", f_telefono="13", f_celular="13", f_contacto_emergencia=None,
        f_email='usb-labd@usb.ve', f_direccion=None, f_ubicacion=None, f_pagina_web=None,
        f_estatus=None, f_categoria=None, f_fecha_ingreso=None, f_fecha_salida=None,
        f_fecha_ingreso_usb=None, f_fecha_ingreso_ulab=None, f_fecha_ingreso_admin_publica=None,
        f_condicion=None, f_rol=rol, f_usuario=user, f_dependencia=dep, f_validado=True, f_es_supervisor=True
    )

    # Laboratorio E
    dep = db(db.dependencias.nombre == 'LABORATORIO E').select()[0].id
    user = db(db.auth_user.email == 'usb-labe@usb.ve').select()[0].id
    db.t_Personal.insert(
        f_nombre="Jefe del Laboratorio E", f_apellido="", f_gremio="Administrativo", f_cargo="Jefe de Laboratorio",
        f_ci="14", f_telefono="14", f_celular="14", f_contacto_emergencia=None,
        f_email='usb-labe@usb.ve', f_direccion=None, f_ubicacion=None, f_pagina_web=None,
        f_estatus=None, f_categoria=None, f_fecha_ingreso=None, f_fecha_salida=None,
        f_fecha_ingreso_usb=None, f_fecha_ingreso_ulab=None, f_fecha_ingreso_admin_publica=None,
        f_condicion=None, f_rol=rol, f_usuario=user, f_dependencia=dep, f_validado=True, f_es_supervisor=True
    )

    # Laboratorio F
    dep = db(db.dependencias.nombre == 'LABORATORIO F').select()[0].id
    user = db(db.auth_user.email == 'usb-labf@usb.ve').select()[0].id
    db.t_Personal.insert(
        f_nombre="Jefe del Laboratorio F", f_apellido="", f_gremio="Administrativo", f_cargo="Jefe de Laboratorio",
        f_ci="15", f_telefono="15", f_celular="15", f_contacto_emergencia=None,
        f_email='usb-labf@usb.ve', f_direccion=None, f_ubicacion=None, f_pagina_web=None,
        f_estatus=None, f_categoria=None, f_fecha_ingreso=None, f_fecha_salida=None,
        f_fecha_ingreso_usb=None, f_fecha_ingreso_ulab=None, f_fecha_ingreso_admin_publica=None,
        f_condicion=None, f_rol=rol, f_usuario=user, f_dependencia=dep, f_validado=True, f_es_supervisor=True
    )

    # Laboratorio G
    dep = db(db.dependencias.nombre == 'LABORATORIO G').select()[0].id
    user = db(db.auth_user.email == 'usb-labg@usb.ve').select()[0].id
    db.t_Personal.insert(
        f_nombre="Jefe del Laboratorio G", f_apellido="", f_gremio="Administrativo", f_cargo="Jefe de Laboratorio",
        f_ci="16", f_telefono="16", f_celular="16", f_contacto_emergencia=None,
        f_email='usb-labg@usb.ve', f_direccion=None, f_ubicacion=None, f_pagina_web=None,
        f_estatus=None, f_categoria=None, f_fecha_ingreso=None, f_fecha_salida=None,
        f_fecha_ingreso_usb=None, f_fecha_ingreso_ulab=None, f_fecha_ingreso_admin_publica=None,
        f_condicion=None, f_rol=rol, f_usuario=user, f_dependencia=dep, f_validado=True, f_es_supervisor=True
    )


# Propositos de una solicitud

if db(db.propositos).isempty():
	db.propositos.insert(tipo='Docencia')
	db.propositos.insert(tipo='Investigación')
	db.propositos.insert(tipo='Extensión')
	db.propositos.insert(tipo='Gestión')

# Tipos de servicios

if db(db.tipos_servicios).isempty():
	db.tipos_servicios.insert(nombre='Ensayo')
	db.tipos_servicios.insert(nombre='Inspección')
	db.tipos_servicios.insert(nombre='Calibración')
	db.tipos_servicios.insert(nombre='Desarrollo de prototipos y piezas')
	db.tipos_servicios.insert(nombre='Consultoría / Asesoría Técnica y Proyectos')
	db.tipos_servicios.insert(nombre='Formación / Capacitación / Transferencia Tecnológica')
	db.tipos_servicios.insert(nombre='Sala de Computadoras')
	db.tipos_servicios.insert(nombre='Sala de Videos')
	db.tipos_servicios.insert(nombre='Verificación')

# Categorias de servicios

if db(db.categorias_servicios).isempty():
	db.categorias_servicios.insert(nombre='Alimentos')
	db.categorias_servicios.insert(nombre='Ambiente')
	db.categorias_servicios.insert(nombre='Arquitectura, Urbanismo y Arte')
	db.categorias_servicios.insert(nombre='Biología')
	db.categorias_servicios.insert(nombre='Energía')
	db.categorias_servicios.insert(nombre='Manufactura, Instrumentación y Control')
	db.categorias_servicios.insert(nombre='Matemáticas y Estadísticas')
	db.categorias_servicios.insert(nombre='Mecánica y Materiales')
	db.categorias_servicios.insert(nombre='Química')
	db.categorias_servicios.insert(nombre='Física')
	db.categorias_servicios.insert(nombre='Informática, Computación, Comunicación e Información')
	db.categorias_servicios.insert(nombre='Música')
	db.categorias_servicios.insert(nombre='Salud')
	db.categorias_servicios.insert(nombre='Otros')

# Asignacion de roles
if db(db.auth_membership).isempty():
    # Asignacion de roles
    user = db(db.auth_user.email == 'funindes@usb.ve').select()[0].id
    dep = db(db.dependencias.nombre == 'DIRECCIÓN').select()[0].id
    role = db(db.auth_group.role == 'CLIENTE INTERNO').select()[0].id

    db.auth_membership.insert(user_id=user, group_id=role)

    user = db(db.auth_user.email == 'sigulabusb@gmail.com').select()[0].id
    dep = db(db.dependencias.nombre == 'DIRECCIÓN').select()[0].id
    role = db(db.auth_group.role == 'WEBMASTER').select()[0].id

    db.auth_membership.insert(user_id=user, group_id=role)

    user = db(db.auth_user.email == 'ulab-smdp@usb.ve').select()[0].id
    dep = db(db.dependencias.nombre == 'DIRECCIÓN').select()[0].id
    role = db(db.auth_group.role == 'GESTOR DE SMyDP').select()[0].id

    db.auth_membership.insert(user_id=user, group_id=role, dependencia_asociada=dep)

    user = db(db.auth_user.email == 'asis-ulab@usb.ve').select()[0].id
    dep = db(db.dependencias.nombre == 'DIRECCIÓN').select()[0].id
    role = db(db.auth_group.role == 'ASISTENTE DEL DIRECTOR').select()[0].id

    db.auth_membership.insert(user_id=user, group_id=role, dependencia_asociada=dep)

    dep = None
    role = db(db.auth_group.role == 'GESTOR DE PERSONAL').select()[0].id

    db.auth_membership.insert(user_id=user, group_id=role, dependencia_asociada=dep)


    # Director

    user = db(db.auth_user.email == 'ulab@usb.ve').select()[0].id
    dep = db(db.dependencias.nombre == 'DIRECCIÓN').select()[0].id
    role = db(db.auth_group.role == 'DIRECTOR').select()[0].id

    db.auth_membership.insert(user_id=user, group_id=role, dependencia_asociada=dep)

    # Coordinadores

    user = db(db.auth_user.email == 'ulab-adquisicion@usb.ve').select()[0].id
    dep = db(db.dependencias.nombre == 'COORDINACIÓN DE ADQUISICIONES').select()[0].id
    role = db(db.auth_group.role == 'COORDINADOR').select()[0].id

    db.auth_membership.insert(user_id=user, group_id=role, dependencia_asociada=dep)

    user = db(db.auth_user.email == 'ulab-calidad@usb.ve').select()[0].id
    dep = db(db.dependencias.nombre == 'COORDINACIÓN DE LA CALIDAD').select()[0].id
    role = db(db.auth_group.role == 'COORDINADOR').select()[0].id

    db.auth_membership.insert(user_id=user, group_id=role, dependencia_asociada=dep)

    user = db(db.auth_user.email == 'ulab-importaciones@usb.ve').select()[0].id
    dep = db(db.dependencias.nombre == 'COORDINACIÓN DE IMPORTACIONES').select()[0].id
    role = db(db.auth_group.role == 'COORDINADOR').select()[0].id

    db.auth_membership.insert(user_id=user, group_id=role, dependencia_asociada=dep)


    user = db(db.auth_user.email == 'ulab-administracion@usb.ve').select()[0].id
    dep = db(db.dependencias.nombre == 'UNIDAD DE ADMINISTRACIÓN').select()[0].id
    role = db(db.auth_group.role == 'COORDINADOR').select()[0].id

    db.auth_membership.insert(user_id=user, group_id=role, dependencia_asociada=dep)

    user = db(db.auth_user.email == 'ulab-pradiologica@usb.ve').select()[0].id
    dep = db(db.dependencias.nombre == 'OFICINA DE PROTECCIÓN RADIOLÓGICA').select()[0].id
    role = db(db.auth_group.role == 'COORDINADOR').select()[0].id

    db.auth_membership.insert(user_id=user, group_id=role, dependencia_asociada=dep)

    # Laboratorios

    user = db(db.auth_user.email == 'usb-laba@usb.ve').select()[0].id
    dep = db(db.dependencias.nombre == 'LABORATORIO A').select()[0].id
    role = db(db.auth_group.role == 'JEFE DE LABORATORIO').select()[0].id

    db.auth_membership.insert(user_id=user, group_id=role, dependencia_asociada=dep)

    user = db(db.auth_user.email == 'usb-labb@usb.ve').select()[0].id
    dep = db(db.dependencias.nombre == 'LABORATORIO B').select()[0].id
    role = db(db.auth_group.role == 'JEFE DE LABORATORIO').select()[0].id

    db.auth_membership.insert(user_id=user, group_id=role, dependencia_asociada=dep)

    user = db(db.auth_user.email == 'usb-labc@usb.ve').select()[0].id
    dep = db(db.dependencias.nombre == 'LABORATORIO C').select()[0].id
    role = db(db.auth_group.role == 'JEFE DE LABORATORIO').select()[0].id

    db.auth_membership.insert(user_id=user, group_id=role, dependencia_asociada=dep)

    user = db(db.auth_user.email == 'usb-labd@usb.ve').select()[0].id
    dep = db(db.dependencias.nombre == 'LABORATORIO D').select()[0].id
    role = db(db.auth_group.role == 'JEFE DE LABORATORIO').select()[0].id

    db.auth_membership.insert(user_id=user, group_id=role, dependencia_asociada=dep)

    user = db(db.auth_user.email == 'usb-labe@usb.ve').select()[0].id
    dep = db(db.dependencias.nombre == 'LABORATORIO E').select()[0].id
    role = db(db.auth_group.role == 'JEFE DE LABORATORIO').select()[0].id

    db.auth_membership.insert(user_id=user, group_id=role, dependencia_asociada=dep)

    user = db(db.auth_user.email == 'usb-labf@usb.ve').select()[0].id
    dep = db(db.dependencias.nombre == 'LABORATORIO F').select()[0].id
    role = db(db.auth_group.role == 'JEFE DE LABORATORIO').select()[0].id

    db.auth_membership.insert(user_id=user, group_id=role, dependencia_asociada=dep)

    user = db(db.auth_user.email == 'usb-labg@usb.ve').select()[0].id
    dep = db(db.dependencias.nombre == 'LABORATORIO G').select()[0].id
    role = db(db.auth_group.role == 'JEFE DE LABORATORIO').select()[0].id

    db.auth_membership.insert(user_id=user, group_id=role, dependencia_asociada=dep)


# Unidades de medida (*!* Si se agregan nuevas unidades se debera modificar la funcion
# __sumar_cantidad del controlador __agregar_inventarios de smydp)
if db(db.t_Unidad_de_medida).isempty():
    db.t_Unidad_de_medida.insert(f_nombre='Mililitros', f_abreviatura='ml')
    db.t_Unidad_de_medida.insert(f_nombre='Litros', f_abreviatura='l')
    db.t_Unidad_de_medida.insert(f_nombre='Gramos', f_abreviatura='g')
    db.t_Unidad_de_medida.insert(f_nombre='Kilogramos', f_abreviatura='kg')


# Catalogo de sustancias

if db(db.t_Sustancia).isempty():
    db.t_Sustancia.insert(f_nombre='Acetato de Etilo', f_cas='141-78-6', f_pureza='99',
    	f_estado='Líquido', f_control='RL4', f_peligrosidad=['Inflamable','Irritante'])
    db.t_Sustancia.insert(f_nombre='Acetona', f_cas='67-64-1', f_pureza='99',
    	f_estado='Líquido', f_control='RL4', f_peligrosidad=['Inflamable','Tóxico'])
    db.t_Sustancia.insert(f_nombre='Ácido Antranílico', f_cas='118-92-3', f_pureza='99',
    	f_estado='Líquido', f_control='RL4', f_peligrosidad=['Inflamable','Comburente'])
    db.t_Sustancia.insert(f_nombre='Ácido Clorhídrico', f_cas='7647-01-0', f_pureza='37',
    	f_estado='Líquido', f_control='RL4', f_peligrosidad=['Tóxico','Corrosivo'])
    db.t_Sustancia.insert(f_nombre='Ácido Fenilacético y sus sales', f_cas='103-82-2', f_pureza='99',
    	f_estado='Líquido', f_control='RL4', f_peligrosidad=['Comburente'])
    db.t_Sustancia.insert(f_nombre='Ácido Nítrico', f_cas='7697-37-2', f_pureza='5',
    	f_estado='Líquido', f_control='RL7', f_peligrosidad=['Tóxico','Irritante'])
    db.t_Sustancia.insert(f_nombre='Ácido Pícrico (trinitrofenol)', f_cas='88-89-1', f_pureza='3',
    	f_estado='Sólido', f_control='RL7', f_peligrosidad=['Explosivo','Tóxico'])
    db.t_Sustancia.insert(f_nombre='Ácido Sulfúrico', f_cas='7664-93-9', f_pureza='97',
    	f_estado='Líquido', f_control='RL4 y RL7', f_peligrosidad=['Corrosivo','Irritante'])
    db.t_Sustancia.insert(f_nombre='Aluminio en polvo', f_cas='7429-90-5', f_pureza='99',
    	f_estado='Sólido', f_control='RL7', f_peligrosidad=['Inflamable'])
    db.t_Sustancia.insert(f_nombre='Amoníaco Anhídrico', f_cas='7664-41-7', f_pureza='99',
    	f_estado='Líquido', f_control='RL4', f_peligrosidad=['Nocivo','Inflamable'])
    db.t_Sustancia.insert(f_nombre='Amoníaco en disolución acuosa', f_cas='001336-21-6', f_pureza='25',
    	f_estado='Líquido', f_control='RL4', f_peligrosidad=['Tóxico','Corrosivo'])
    db.t_Sustancia.insert(f_nombre='Anhídrico acético', f_cas='108-24-7', f_pureza='99',
    	f_estado='Líquido', f_control='RL4', f_peligrosidad=['Inflamable','Nocivo'])
    db.t_Sustancia.insert(f_nombre='Azidas (de sodio)', f_cas='26628-22-8', f_pureza='99',
    	f_estado='Sólido', f_control='RL7', f_peligrosidad=['Tóxico'])
    db.t_Sustancia.insert(f_nombre='Benceno', f_cas='71-43-2', f_pureza='99',
    	f_estado='Líquido', f_control='RL7', f_peligrosidad=['Tóxico','Inflamable'])
    db.t_Sustancia.insert(f_nombre='Butanona (metilcetona)', f_cas='78-93-3', f_pureza='99',
    	f_estado='Líquido', f_control='RL4', f_peligrosidad=['Inflamable','Tóxico'])
    db.t_Sustancia.insert(f_nombre='Carbonato de Sodio', f_cas='497-19-8', f_pureza='99',
    	f_estado='Sólido', f_control='RL4', f_peligrosidad=['Corrosivo','Irritante'])
    db.t_Sustancia.insert(f_nombre='Clorato de Potasio', f_cas='3811-04-9', f_pureza='99',
    	f_estado='Sólido', f_control='RL7', f_peligrosidad=['Comburente','Tóxico'])
    db.t_Sustancia.insert(f_nombre='Clorato de Sodio', f_cas='7775-09-9', f_pureza='99',
    	f_estado='Sólido', f_control='RL7', f_peligrosidad=['Comburente','Tóxico'])
    db.t_Sustancia.insert(f_nombre='Cloroformo', f_cas='67-66-3', f_pureza='99',
    	f_estado='Líquido', f_control='RL4', f_peligrosidad=['Nocivo','Tóxico'])
    db.t_Sustancia.insert(f_nombre='Diclorometano', f_cas='75-09-2', f_pureza='99',
    	f_estado='Líquido', f_control='RL4', f_peligrosidad=['Nocivo','Inflamable'])
    db.t_Sustancia.insert(f_nombre='Dinitrofenol', f_cas='51-28-5', f_pureza='99',
    	f_estado='Sólido', f_control='RL7', f_peligrosidad=['Nocivo','Tóxico'])
    db.t_Sustancia.insert(f_nombre='Dinitrotolueno', f_cas='606-20-2', f_pureza='99',
    	f_estado='Sólido', f_control='RL7', f_peligrosidad=['Nocivo'])
    db.t_Sustancia.insert(f_nombre='Etanol', f_cas='64-17-5', f_pureza='99',
    	f_estado='Líquido', f_control='RL4', f_peligrosidad=['Inflamable','Irritante'])
    db.t_Sustancia.insert(f_nombre='Eter Etílico', f_cas='60-29-7', f_pureza='99',
    	f_estado='Líquido', f_control='RL4', f_peligrosidad=['Explosivo','Nocivo'])
    db.t_Sustancia.insert(f_nombre='Fósforo blanco', f_cas='7723-14-0', f_pureza='99',
    	f_estado='Sólido', f_control='RL7', f_peligrosidad=['Inflamable','Nocivo'])
    db.t_Sustancia.insert(f_nombre='Fulminato de Mercurio', f_cas='628-86-4', f_pureza='',
    	f_estado='', f_control='RL7', f_peligrosidad=['N/A'])
    db.t_Sustancia.insert(f_nombre='Heptano', f_cas='142-82-5', f_pureza='99',
    	f_estado='Líquido', f_control='RL4', f_peligrosidad=['Inflamable','Irritante'])
    db.t_Sustancia.insert(f_nombre='Hexano', f_cas='110-54-3', f_pureza='99',
    	f_estado='Líquido', f_control='RL4', f_peligrosidad=['Inflamable'])
    db.t_Sustancia.insert(f_nombre='Hidrogenocarbonato (Bicarbonato) de Sodio', f_cas='144-55-8', f_pureza='99',
    	f_estado='Sólido', f_control='RL4', f_peligrosidad=['Irritante'])
    db.t_Sustancia.insert(f_nombre='Hipoclorito de calcio', f_cas='7778-54-3', f_pureza='68',
    	f_estado='Sólido', f_control='RL7', f_peligrosidad=['Corrosivo','Irritante'])
    db.t_Sustancia.insert(f_nombre='Hipoclorito de Sodio', f_cas='7681-52-9', f_pureza='',
    	f_estado='Líquido', f_control='RL7', f_peligrosidad=['Corrosivo','Tóxico'])
    db.t_Sustancia.insert(f_nombre='Metanol', f_cas='67-56-1', f_pureza='99',
    	f_estado='Líquido', f_control='RL4', f_peligrosidad=['Inflamable','Irritante'])
    db.t_Sustancia.insert(f_nombre='Nitrato de Amonio (salitre de chile)', f_cas='6484-52-2', f_pureza='99',
    	f_estado='Sólido', f_control='RL7', f_peligrosidad=['Explosivo'])
    # *!* Tenia el mismo CAS que el acido nitrico
    db.t_Sustancia.insert(f_nombre='Nitrato de Bismuto', f_cas='10361-46-3', f_pureza='99',
    	f_estado='Sólido', f_control='RL7', f_peligrosidad=['Corrosivo','Tóxico'])
    db.t_Sustancia.insert(f_nombre='Nitrato de Calcio', f_cas='13477-34-4', f_pureza='99',
    	f_estado='Sólido', f_control='RL7', f_peligrosidad=['Tóxico'])
    db.t_Sustancia.insert(f_nombre='Nitrato de Plata', f_cas='7761-88-8', f_pureza='99',
    	f_estado='Sólido', f_control='RL7', f_peligrosidad=['Corrosivo','Tóxico'])
    db.t_Sustancia.insert(f_nombre='Nitrato de Plomo', f_cas='10099-74-8', f_pureza='99',
    	f_estado='Sólido', f_control='RL7', f_peligrosidad=['Tóxico'])
    db.t_Sustancia.insert(f_nombre='Nitrato de Potasio', f_cas='7757-79-1', f_pureza='99',
    	f_estado='Sólido', f_control='RL7', f_peligrosidad=['Comburente','Tóxico'])
    db.t_Sustancia.insert(f_nombre='Nitrato de Sodio', f_cas='7631-99-4', f_pureza='99',
    	f_estado='Sólido', f_control='RL7', f_peligrosidad=['Comburente','Tóxico'])
    db.t_Sustancia.insert(f_nombre='Nitrito de Sodio', f_cas='7632-00-0', f_pureza='99',
    	f_estado='Sólido', f_control='RL7', f_peligrosidad=['Comburente','Tóxico'])
    db.t_Sustancia.insert(f_nombre='Nitrobenceno', f_cas='98-95-3', f_pureza='99',
    	f_estado='Líquido', f_control='RL7', f_peligrosidad=['Nocivo','Tóxico'])
    db.t_Sustancia.insert(f_nombre='Nitrocelulosa', f_cas='9004-70-0', f_pureza='12',
    	f_estado='Sólido', f_control='RL7', f_peligrosidad=['Inflamable'])
    db.t_Sustancia.insert(f_nombre='Nitroglicerina', f_cas='55-63-0', f_pureza='1',
    	f_estado='Sólido', f_control='RL7', f_peligrosidad=['Explosivo'])
    db.t_Sustancia.insert(f_nombre='Perclorato de Potasio', f_cas='7778-74-7', f_pureza='99',
    	f_estado='Sólido', f_control='RL7', f_peligrosidad=['Comburente','Tóxico'])
    db.t_Sustancia.insert(f_nombre='Perclorato de Sodio', f_cas='7601-89-0', f_pureza='99',
    	f_estado='Sólido', f_control='RL7', f_peligrosidad=['Comburente','Nocivo'])
    db.t_Sustancia.insert(f_nombre='Permanganato de Potasio', f_cas='7722-64-7', f_pureza='99',
    	f_estado='Sólido', f_control='RL4 y RL7', f_peligrosidad=['Comburente','Corrosivo'])
    db.t_Sustancia.insert(f_nombre='Sesquicarbonato de Sodio', f_cas='6106-20-3', f_pureza='99',
    	f_estado='Sólido', f_control='RL4', f_peligrosidad=['Corrosivo','Irritante'])
    db.t_Sustancia.insert(f_nombre='Sulfato de Amonio', f_cas='7783-20-2', f_pureza='99',
    	f_estado='Sólido', f_control='RL7', f_peligrosidad=['Corrosivo','Irritante'])
    db.t_Sustancia.insert(f_nombre='Sulfato de Magnesio', f_cas='7487-88-9', f_pureza='65',
    	f_estado='Sólido', f_control='RL7', f_peligrosidad=['Irritante'])
    db.t_Sustancia.insert(f_nombre='Sulfuro de Potasio', f_cas='1312-73-8', f_pureza='99',
    	f_estado='Sólido', f_control='RL7', f_peligrosidad=['Inflamable','Corrosivo'])
    db.t_Sustancia.insert(f_nombre='Tetrahidrofurano', f_cas='109-99-9', f_pureza='99',
    	f_estado='Líquido', f_control='RL4', f_peligrosidad=['Inflamable','Irritante'])
    db.t_Sustancia.insert(f_nombre='Tolueno', f_cas='108-88-3', f_pureza='99',
    	f_estado='Líquido', f_control='RL4', f_peligrosidad=['Inflamable','Tóxico'])
    db.t_Sustancia.insert(f_nombre='Trinitrotolueno (TNT)', f_cas='118-96-7', f_pureza='99',
    	f_estado='Sólido', f_control='RL7', f_peligrosidad=['Explosivo','Nocivo'])
    db.t_Sustancia.insert(f_nombre='Urea', f_cas='57-13-6 ', f_pureza='',
    	f_estado='Sólido', f_control='RL7', f_peligrosidad=['Irritante','Comburente'])
    db.t_Sustancia.insert(f_nombre='4-metilpentan-2-ona (Metilisobutilcetona)', f_cas='108-10-1', f_pureza='99',
    	f_estado='Líquido', f_control='RL4', f_peligrosidad=['Tóxico'])
    # Tiene el mismo CAS que fosforos blancos
    #db.t_Sustancia.insert(f_nombre='Fósforos rojos o amorfos', f_cas='7723-14-0', f_pureza='99',
    #	f_estado='Sólido', f_control='N/A', f_peligrosidad=['Inflamable','Nocivo'])

# Categorias de desechos

if db(db.t_categoria_desechos).isempty():
	categorias_iniciales = ['Sales Inorgánicas', 'Ácidos', 'Bases', 'Alcoholes', 'Orgánicos halogenados', 'Orgánicos no halogenados', 'Oxidantes']

	for categoria in categorias_iniciales:
		db.t_categoria_desechos.insert(categoria=categoria, descripcion=categoria)


if db(db.espacios_fisicos).isempty():
    db.espacios_fisicos.insert(codigo='ALT-001A', uso='SALA DE EQUIPOS DE INTERCONEXION A INTERNET', ext_USB= ''  ,ext_interna= '', dependencia=5)
    db.espacios_fisicos.insert(codigo='ALT-002A', uso='SALA DE EQUIPOS DE INTERCONEXI', ext_USB= ''  ,ext_interna= '', dependencia=10)

