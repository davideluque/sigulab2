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

# Sedes

if db(db.sedes).isempty():
	db.sedes.insert(nombre="Sartenejas")
	db.sedes.insert(nombre="Litoral")

# Dependencias

if db(db.dependencias).isempty():
	
	# Direccion
	user = db(db.auth_user.email == 'ulab@usb.ve').select()[0].id
	db.dependencias.insert(nombre='DIRECCIÓN', id_sede=1, id_jefe_dependencia=user, 
		codigo_registro="UL")

	direccionid = db(db.dependencias.nombre == 'DIRECCIÓN').select()[0].id

	# Laboratorios

	# Laboratorio A
	user = db(db.auth_user.email == 'usb-laba@usb.ve').select()[0].id
	db.dependencias.insert(nombre='LABORATORIO A', id_sede=1, 
		unidad_de_adscripcion=direccionid, id_jefe_dependencia=user, 
		codigo_registro="ULLA")

	# Laboratorio B
	user = db(db.auth_user.email == 'usb-labb@usb.ve').select()[0].id
	db.dependencias.insert(nombre='LABORATORIO B', id_sede=1, 
		unidad_de_adscripcion=direccionid, id_jefe_dependencia=user, 
		codigo_registro="ULLB")

	# Laboratorio C
	user = db(db.auth_user.email == 'usb-labc@usb.ve').select()[0].id	
	db.dependencias.insert(nombre='LABORATORIO C', id_sede=1, 
		unidad_de_adscripcion=direccionid, id_jefe_dependencia=user, 
		codigo_registro="ULLC")

	# Laboratorio D	
	user = db(db.auth_user.email == 'usb-labd@usb.ve').select()[0].id
	db.dependencias.insert(nombre='LABORATORIO D', id_sede=1, 
		unidad_de_adscripcion=direccionid, id_jefe_dependencia=user, 
		codigo_registro="ULLD")
	
	# Laboratorio E
	user = db(db.auth_user.email == 'usb-labe@usb.ve').select()[0].id
	db.dependencias.insert(nombre='LABORATORIO E', id_sede=1, 
		unidad_de_adscripcion=direccionid, id_jefe_dependencia=user, 
		codigo_registro="ULLE")

	# Laboratorio F
	user = db(db.auth_user.email == 'usb-labf@usb.ve').select()[0].id
	db.dependencias.insert(nombre='LABORATORIO F', id_sede=1, 
		unidad_de_adscripcion=direccionid, id_jefe_dependencia=user, 
		codigo_registro="ULLF")

	# Laboratorio G
	user = db(db.auth_user.email == 'usb-labg@usb.ve').select()[0].id
	db.dependencias.insert(nombre='LABORATORIO G', id_sede=2, 
		unidad_de_adscripcion=direccionid, id_jefe_dependencia=user, 
		codigo_registro="ULLG")

	# Coordinaciones

	# Unidad de Administración
	user = db(db.auth_user.email == 'ulab-administracion@usb.ve').select()[0].id
	db.dependencias.insert(nombre='UNIDAD DE ADMINISTRACIÓN', id_sede=1, 
		unidad_de_adscripcion=direccionid, id_jefe_dependencia=user, 
		codigo_registro="UL03")

	# Coordinación de Adquisiciones
	user = db(db.auth_user.email == 'ulab-adquisicion@usb.ve').select()[0].id	
	db.dependencias.insert(nombre='COORDINACIÓN DE ADQUISICIONES', id_sede=1, 
		unidad_de_adscripcion=direccionid, id_jefe_dependencia=user, 
		codigo_registro="UL01")

	# Coordinación de Importaciones
	user = db(db.auth_user.email == 'ulab-importaciones@usb.ve').select()[0].id
	db.dependencias.insert(nombre='COORDINACIÓN DE IMPORTACIONES', id_sede=1, 
		unidad_de_adscripcion=direccionid, id_jefe_dependencia=user, 
		codigo_registro="UL02")

	# Coordinación de la Calidad
	user = db(db.auth_user.email == 'ulab-calidad@usb.ve').select()[0].id
	db.dependencias.insert(nombre='COORDINACIÓN DE LA CALIDAD', id_sede=1, 
		unidad_de_adscripcion=direccionid, id_jefe_dependencia=user, 
		codigo_registro="UL04")

	# Protección Radiológica
	user = db(db.auth_user.email == 'ulab-pradiologica@usb.ve').select()[0].id
	db.dependencias.insert(nombre='OFICINA DE PROTECCIÓN RADIOLÓGICA', id_sede=1, 
		unidad_de_adscripcion=direccionid, id_jefe_dependencia=user, 
		codigo_registro="UL05")

	
if db(db.t_Personal).isempty():
	"""La inserción de los usuarios registrados en auth_user en la tabla de 
	Personal es estrictamente necesaria pues los objetos del modulo de Servicios
	buscan las dependencias de los usuarios a través de una coincidencia del
	usuario con la tabla de Personal ya que esta tabla es la que guarda el 
	la dependencia de cada usuario y no auth_user"""
	
	dep = db(db.dependencias.nombre == 'DIRECCIÓN').select()[0].id

	""" Super Usuario """
	user = db(db.auth_user.email == 'sigulabusb@gmail.com').select()[0].id
	db.t_Personal.insert(f_nombre="Super", f_apellido = "", f_categoria="N/A", 
		f_cargo="Super Usuario", f_ci=0, f_email='sigulabusb@gmail.com', f_estatus='Activo',
		f_usuario=user, f_dependencia=dep)

	""" Cliente Interno """
	user = db(db.auth_user.email == 'funindes@usb.ve').select()[0].id
	db.t_Personal.insert(f_nombre="Funindes",f_apellido = "", 
		f_categoria = "Administrativo", f_cargo = "Cliente Interno",
		f_ci = 0, f_email='funindes@usb.ve', f_estatus='Activo',
		f_usuario=user, f_dependencia=dep)

	""" Asistente Dirección """
	user = db(db.auth_user.email == 'asis-ulab@usb.ve').select()[0].id
	db.t_Personal.insert(f_nombre="Asistente Dirección",f_apellido = "", 
		f_categoria = "Administrativo", f_cargo = "Asistente Dirección",
		f_ci = 0, f_email='asis-ulab@usb.ve', f_estatus='Activo',
		f_usuario=user, f_dependencia=dep)

	""" Gestor de Sustancias """
	user = db(db.auth_user.email == 'ulab-smdp@usb.ve').select()[0].id
	db.t_Personal.insert(f_nombre="Gestor de Sustancias", f_apellido = "", 
											 f_categoria="Administrativo", f_cargo="Gestor de Sustancias",
											 f_ci=0, f_email='ulab-smdp@usb.ve', f_estatus='Activo',
											 f_usuario=user, f_dependencia=dep)

	""" Director """
	user = db(db.auth_user.email == 'ulab@usb.ve').select()[0].id
	db.t_Personal.insert(f_nombre="Director", f_apellido = "", 
		f_categoria="Administrativo", f_cargo="Director",
		f_ci=0, f_email='ulab@usb.ve', f_estatus='Activo',
		f_usuario=user, f_dependencia=dep)

	""" Coordinaciones """

	# Coordinación de Adquisiciones
	dep = db(db.dependencias.nombre == 'COORDINACIÓN DE ADQUISICIONES').select()[0].id
	user = db(db.auth_user.email == 'ulab-adquisicion@usb.ve').select()[0].id
	db.t_Personal.insert(f_nombre="Coordinador de Adquisiciones", f_apellido = "", 
		f_categoria="Administrativo", f_cargo="Coordinador",
		f_ci=0, f_email='ulab-adquisicion@usb.ve', f_estatus='Activo',
		f_usuario=user, f_dependencia=dep)

	# Coordinación de la Calidad
	dep = db(db.dependencias.nombre == 'COORDINACIÓN DE LA CALIDAD').select()[0].id
	user = db(db.auth_user.email == 'ulab-calidad@usb.ve').select()[0].id
	db.t_Personal.insert(f_nombre="Coordinador de Calidad", f_apellido = "", 
		f_categoria="Administrativo", f_cargo="Coordinador",
		f_ci=0, f_email='ulab-calidad@usb.ve', f_estatus='Activo',
		f_usuario=user, f_dependencia=dep)

	# Coordinación de Importaciones
	dep = db(db.dependencias.nombre == 'COORDINACIÓN DE IMPORTACIONES').select()[0].id
	user = db(db.auth_user.email == 'ulab-importaciones@usb.ve').select()[0].id
	db.t_Personal.insert(f_nombre="Coordinador de Importaciones", f_apellido = "", 
		f_categoria="Administrativo", f_cargo="Coordinador",
		f_ci=0, f_email='ulab-importaciones@usb.ve', f_estatus='Activo',
		f_usuario=user, f_dependencia=dep)

	""" Unidades """

	# Unidad de Administración
	dep = db(db.dependencias.nombre == 'UNIDAD DE ADMINISTRACIÓN').select()[0].id
	user = db(db.auth_user.email == 'ulab-administracion@usb.ve').select()[0].id
	db.t_Personal.insert(f_nombre="Unidad de Administración", f_apellido = "", 
		f_categoria="Administrativo", f_cargo="Coordinador",f_ci=0, 
		f_email='ulab-administracion@usb.ve', f_estatus='Activo', f_usuario=user, 
		f_dependencia=dep)

	# Oficina de Proteccion Radiologica
	dep = db(db.dependencias.nombre == 'DIRECCIÓN').select()[0].id
	user = db(db.auth_user.email == 'ulab-pradiologica@usb.ve').select()[0].id
	db.t_Personal.insert(f_nombre="Encargado de la Oficina de Proteccion Radiológica", 
		f_apellido = "", f_categoria="Administrativo", f_cargo="Coordinador",
		f_ci=0, f_email='ulab-pradiologica@usb.ve', f_estatus='Activo',
		f_usuario=user, f_dependencia=dep)


	""" Jefes de Laboratorios """

	# Laboratorio A
	dep = db(db.dependencias.nombre == 'LABORATORIO A').select()[0].id
	user = db(db.auth_user.email == 'usb-laba@usb.ve').select()[0].id
	db.t_Personal.insert(f_nombre="Jefe del Laboratorio A", f_apellido = "", 
		f_categoria="Técnico", f_cargo="Jefe de Laboratorio",f_ci=0, 
		f_email='usb-laba@usb.ve', f_estatus='Activo',f_usuario=user, 
		f_dependencia=dep)

	# Laboratorio B
	dep = db(db.dependencias.nombre == 'LABORATORIO B').select()[0].id
	user = db(db.auth_user.email == 'usb-labb@usb.ve').select()[0].id
	db.t_Personal.insert(f_nombre="Jefe del Laboratorio B", f_apellido = "", 
		f_categoria="Técnico", f_cargo="Jefe de Laboratorio",f_ci=0, 
		f_email='usb-labb@usb.ve', f_estatus='Activo',f_usuario=user, 
		f_dependencia=dep)

	# Laboratorio C
	dep = db(db.dependencias.nombre == 'LABORATORIO C').select()[0].id
	user = db(db.auth_user.email == 'usb-labc@usb.ve').select()[0].id
	db.t_Personal.insert(f_nombre="Jefe del Laboratorio C", f_apellido = "", 
		f_categoria="Técnico", f_cargo="Jefe de Laboratorio",
						 f_ci=0, f_email='usb-labc@usb.ve', f_estatus='Activo',
						 f_usuario=user, f_dependencia=dep)

	# Laboratorio D
	dep = db(db.dependencias.nombre == 'LABORATORIO D').select()[0].id
	user = db(db.auth_user.email == 'usb-labd@usb.ve').select()[0].id
	db.t_Personal.insert(f_nombre="Jefe del Laboratorio D", f_apellido = "", 
		f_categoria="Técnico", f_cargo="Jefe de Laboratorio",
						 f_ci=0, f_email='usb-labd@usb.ve', f_estatus='Activo',
						 f_usuario=user, f_dependencia=dep)

	# Laboratorio E
	dep = db(db.dependencias.nombre == 'LABORATORIO E').select()[0].id
	user = db(db.auth_user.email == 'usb-labe@usb.ve').select()[0].id
	db.t_Personal.insert(f_nombre="Jefe del Laboratorio E", f_apellido = "", 
		f_categoria="Técnico", f_cargo="Jefe de Laboratorio",
						 f_ci=0, f_email='usb-labe@usb.ve', f_estatus='Activo',
						 f_usuario=user, f_dependencia=dep)

	# Laboratorio F
	dep = db(db.dependencias.nombre == 'LABORATORIO F').select()[0].id
	user = db(db.auth_user.email == 'usb-labf@usb.ve').select()[0].id
	db.t_Personal.insert(f_nombre="Jefe del Laboratorio F", f_apellido = "", 
		f_categoria="Técnico", f_cargo="Jefe de Laboratorio",
						 f_ci=0, f_email='usb-labf@usb.ve', f_estatus='Activo',
						 f_usuario=user, f_dependencia=dep)

	# Laboratorio G
	dep = db(db.dependencias.nombre == 'LABORATORIO G').select()[0].id
	user = db(db.auth_user.email == 'usb-labg@usb.ve').select()[0].id
	db.t_Personal.insert(f_nombre="Jefe del Laboratorio G", f_apellido = "", 
		f_categoria="Técnico", f_cargo="Jefe de Laboratorio",
						 f_ci=0, f_email='usb-labg@usb.ve', f_estatus='Activo',
						 f_usuario=user, f_dependencia=dep)


# Cargos
if db(db.auth_group).isempty():

		db.auth_group.insert(role='WEBMASTER',description='Super Usuario')
		db.auth_group.insert(role='DIRECTOR',description='Director')
		db.auth_group.insert(role='ASISTENTE DEL DIRECTOR',description='Asistente del Director')
		db.auth_group.insert(role='COORDINADOR',description='Coordinación')
		db.auth_group.insert(role='JEFE DE LABORATORIO',description='Jefe de Laboratorio')
		db.auth_group.insert(role='JEFE DE SECCIÓN',description='Jefe de Sección')
		db.auth_group.insert(role='TÉCNICO',description='Técnico')
		db.auth_group.insert(role='PERSONAL DE COORDINACIÓN',description='Personal de Coordinación')
		db.auth_group.insert(role='GESTOR DE SMyDP',description='Gestor de SMyDP')
		db.auth_group.insert(role='CLIENTE INTERNO',description='Cliente Interno')

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
