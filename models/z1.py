###############################################################################
#
# ESTE ARCHIVO SE ENCARGARA DE POBLAR LA BASE DE DATOS CON DATOS BASICOS.
# EL NOMBRE ES "Z" DEBIDO A QUE ESTE ES EL ULTIMO MODELO QUE DEBE CORRER.
# (ALFABETICAMENTE)
# ToDo Acomodar inserts para las tablas que cambiaron (Dependencias le hace falta jefe principalmente)
###############################################################################

# Usuarios

if db(db.auth_user).isempty():
	# Usuarios basicos (Para probar privilegios)
	#
	# db.auth_user.insert(first_name="Personal", last_name="ULAB", email='personal@usb.ve',
	#										 password=db.auth_user.password.validate('0000')[0])
	#
	# db.auth_user.insert(first_name="Técnico", last_name="ULAB", email='tecnico@usb.ve',
	#										 password=db.auth_user.password.validate('0000')[0])
	#
	db.auth_user.insert(first_name="Super", last_name="Usuario", email='webmaster@usb.ve',
											password=db.auth_user.password.validate('0000')[0])
	#
	db.auth_user.insert(first_name="Cliente", last_name="Interno", email='cinterno@usb.ve',
											password=db.auth_user.password.validate('0000')[0])

	db.auth_user.insert(first_name="Asistente del Director", last_name="ULAB", email='directassist@usb.ve',
											password=db.auth_user.password.validate('0000')[0])
	#
	db.auth_user.insert(first_name="Gestor de Sustancias", last_name="ULAB", email='gestor@usb.ve',
											password=db.auth_user.password.validate('0000')[0])
	#
	db.auth_user.insert(first_name="Jefe de Sección", last_name="ULAB", email='jefsecc@usb.ve',
											 password=db.auth_user.password.validate('0000')[0])
	#
	# db.auth_user.insert(first_name="Jefe de Laboratorio", last_name="ULAB", email='jeflab@usb.ve',
	#										 password=db.auth_user.password.validate('0000')[0])
	#
	#
	# db.auth_user.insert(first_name="Coordinador", last_name="ULAB", email='coordinador@usb.ve',
	#										 password=db.auth_user.password.validate('0000')[0])
	#
	# db.auth_user.insert(first_name="Director", last_name="ULAB", email='director@usb.ve',
	#										 password=db.auth_user.password.validate('0000')[0])
	#


	# Usuarios representantes de dependencias

	# ---- Dirección
	db.auth_user.insert(first_name="Dirección", last_name="ULAB", email='ulab@usb.ve',
											password=db.auth_user.password.validate('0000')[0])

	# ---- Coordinaciones

	# Coordinación de Adquisiciones
	db.auth_user.insert(first_name="Coordinación de Adquisiciones", last_name="ULAB", email='ulab-adquisicion@usb.ve',
											password=db.auth_user.password.validate('0000')[0])
	# Coordinación de la Calidad
	db.auth_user.insert(first_name="Coordinación de la Calidad", last_name="ULAB", email='ulab-calidad@usb.ve',
											password=db.auth_user.password.validate('0000')[0])
	# Coordinación de Importaciones
	db.auth_user.insert(first_name="Coordinación de Importaciones", last_name="ULAB", email='ulab-importaciones@usb.ve',
											password=db.auth_user.password.validate('0000')[0])
	# Unidad de Administración
	db.auth_user.insert(first_name="Unidad de Administración", last_name="ULAB", email='ulab-administracion@usb.ve',
											password=db.auth_user.password.validate('0000')[0])
	# Oficina de Proteccion Radiologica
	db.auth_user.insert(first_name="Oficina de Proteccion Radiológica", last_name="ULAB", email='ulab-pradiologica@usb.ve',
											password=db.auth_user.password.validate('0000')[0])

	# ---- Laboratorios

	# Laboratorio A
	db.auth_user.insert(first_name="Laboratorio A", last_name="ULAB", email='usb-laba@usb.ve',
											password=db.auth_user.password.validate('0000')[0])
	# Laboratorio B
	db.auth_user.insert(first_name="Laboratorio B", last_name="ULAB", email='usb-labb@usb.ve',
											password=db.auth_user.password.validate('0000')[0])
	# Laboratorio C
	db.auth_user.insert(first_name="Laboratorio C", last_name="ULAB", email='usb-labc@usb.ve',
											password=db.auth_user.password.validate('0000')[0])
	# Laboratorio D
	db.auth_user.insert(first_name="Laboratorio D", last_name="ULAB", email='usb-labd@usb.ve',
											password=db.auth_user.password.validate('0000')[0])
	# Laboratorio E
	db.auth_user.insert(first_name="Laboratorio E", last_name="ULAB", email='usb-labe@usb.ve',
											password=db.auth_user.password.validate('0000')[0])
	# Laboratorio F
	db.auth_user.insert(first_name="Laboratorio F", last_name="ULAB", email='usb-labf@usb.ve',
											password=db.auth_user.password.validate('0000')[0])
	# Laboratorio G
	db.auth_user.insert(first_name="Laboratorio G", last_name="ULAB", email='usb-labg@usb.ve',
											password=db.auth_user.password.validate('0000')[0])

	# ---- Secciones (2 por Laboratorio)
	# Laboratorio A. Alta Tensión, Conversión de Energía Eléctrica.
	db.auth_user.insert(first_name="Alta Tensión", last_name="Laboratorio A", email='sat-laba@usb.ve',
											password=db.auth_user.password.validate('0000')[0])

	db.auth_user.insert(first_name="Conversión de Energía Eléctrica", last_name="Laboratorio A", email='scee-laba@usb.ve',
											password=db.auth_user.password.validate('0000')[0])


	# Laboratorio B. Alimentos. Biotero.
	db.auth_user.insert(first_name="Alimentos", last_name="Laboratorio B", email='labb-alimentos@usb.ve',
											password=db.auth_user.password.validate('0000')[0])

	db.auth_user.insert(first_name="Bioterio", last_name="Laboratorio B", email='labb-bioterio@usb.ve',
											password=db.auth_user.password.validate('0000')[0])


	# Laboratorio C. Redes, Electrónica Analógica y Digital. Procesamiento de Señales y Sistemas.
	db.auth_user.insert(first_name="Redes, Electrónica Analógica y Digital", last_name="Laboratorio C", email='labc-read@usb.ve',
											password=db.auth_user.password.validate('0000')[0])

	db.auth_user.insert(first_name="Procesamiento de Señales y Sistemas", last_name="Laboratorio C", email='labc-pss@usb.ve',
											password=db.auth_user.password.validate('0000')[0])


	# Laboratorio D. Biofísica. Espectrocopía Laser.
	db.auth_user.insert(first_name="Biofísica", last_name="Laboratorio D", email='labd-biofisica@usb.ve',
											password=db.auth_user.password.validate('0000')[0])

	db.auth_user.insert(first_name="Espectrocopía Laser", last_name="Laboratorio D", email='labd-espectrocopia@usb.ve',
											password=db.auth_user.password.validate('0000')[0])


	# Laboratorio E. Coordinación de Actividades Técnicas. Coordinación de Aseguramiento de la Calidad.
	db.auth_user.insert(first_name="Coordinación de Actividades Técnicas", last_name="Laboratorio E", email='labe-cat@usb.ve',
											password=db.auth_user.password.validate('0000')[0])

	db.auth_user.insert(first_name="Coordinación de Aseguramiento de la Calidad", last_name="Laboratorio E", email='labe-calidad@usb.ve',
											password=db.auth_user.password.validate('0000')[0])


	# Laboratorio F. Aulas Computarizadas. Computacional de Ciencia Política.
	db.auth_user.insert(first_name="Aulas Computarizadas", last_name="Laboratorio F", email='labf-ac@usb.ve',
											password=db.auth_user.password.validate('0000')[0])

	db.auth_user.insert(first_name="Computacional de Ciencia Política", last_name="Laboratorio F", email='labf-ccp@usb.ve',
											password=db.auth_user.password.validate('0000')[0])


	# Laboratorio G. Conversión de Energía Electrica. Conversión de Energía Mecánica.
	db.auth_user.insert(first_name="Conversión de Energía Electrica", last_name="Laboratorio G", email='labg-cee@usb.ve',
											password=db.auth_user.password.validate('0000')[0])

	db.auth_user.insert(first_name="Conversión de Energía Mecánica", last_name="Laboratorio G", email='labg-cem@usb.ve',
											password=db.auth_user.password.validate('0000')[0])

# Sedes

if db(db.sedes).isempty():
	db.sedes.insert(nombre="Sartenejas")
	db.sedes.insert(nombre="Litoral")

# Dependencias

if db(db.dependencias).isempty():
	# Direccion
	user = db(db.auth_user.email == 'ulab@usb.ve').select()[0].id
	db.dependencias.insert(nombre='Dirección', id_sede=1, id_jefe_dependencia=user, codigo_registro="UL")

	direccionid = db(db.dependencias.nombre == 'Dirección').select()[0].id

	# Laboratorios
	user = db(db.auth_user.email == 'usb-laba@usb.ve').select()[0].id
	db.dependencias.insert(nombre='Laboratorio A', id_sede=1, unidad_de_adscripcion=direccionid, id_jefe_dependencia=user, codigo_registro="ULLA")
	user = db(db.auth_user.email == 'usb-labb@usb.ve').select()[0].id
	db.dependencias.insert(nombre='Laboratorio B', id_sede=1, unidad_de_adscripcion=direccionid, id_jefe_dependencia=user, codigo_registro="ULLB")
	user = db(db.auth_user.email == 'usb-labc@usb.ve').select()[0].id
	db.dependencias.insert(nombre='Laboratorio C', id_sede=1, unidad_de_adscripcion=direccionid, id_jefe_dependencia=user, codigo_registro="ULLC")
	user = db(db.auth_user.email == 'usb-labd@usb.ve').select()[0].id
	db.dependencias.insert(nombre='Laboratorio D', id_sede=1, unidad_de_adscripcion=direccionid, id_jefe_dependencia=user, codigo_registro="ULLD")
	user = db(db.auth_user.email == 'usb-labe@usb.ve').select()[0].id
	db.dependencias.insert(nombre='Laboratorio E', id_sede=1, unidad_de_adscripcion=direccionid, id_jefe_dependencia=user, codigo_registro="ULLE")
	user = db(db.auth_user.email == 'usb-labf@usb.ve').select()[0].id
	db.dependencias.insert(nombre='Laboratorio F', id_sede=1, unidad_de_adscripcion=direccionid, id_jefe_dependencia=user, codigo_registro="ULLF")
	user = db(db.auth_user.email == 'usb-labg@usb.ve').select()[0].id
	db.dependencias.insert(nombre='Laboratorio G', id_sede=2, unidad_de_adscripcion=direccionid, id_jefe_dependencia=user, codigo_registro="ULLG")

	# Coordinaciones
	user = db(db.auth_user.email == 'ulab-administracion@usb.ve').select()[0].id
	db.dependencias.insert(nombre='Unidad de Administración', id_sede=1, unidad_de_adscripcion=direccionid, id_jefe_dependencia=user, codigo_registro="UL03")
	user = db(db.auth_user.email == 'ulab-adquisicion@usb.ve').select()[0].id
	db.dependencias.insert(nombre='Coordinación de Adquisiciones', id_sede=1, unidad_de_adscripcion=direccionid, id_jefe_dependencia=user, codigo_registro="UL01")
	user = db(db.auth_user.email == 'ulab-importaciones@usb.ve').select()[0].id
	db.dependencias.insert(nombre='Coordinación de Importaciones', id_sede=1, unidad_de_adscripcion=direccionid, id_jefe_dependencia=user, codigo_registro="UL02")
	user = db(db.auth_user.email == 'ulab-calidad@usb.ve').select()[0].id
	db.dependencias.insert(nombre='Coordinación de la Calidad', id_sede=1, unidad_de_adscripcion=direccionid, id_jefe_dependencia=user, codigo_registro="UL04")
	user = db(db.auth_user.email == 'ulab-pradiologica@usb.ve').select()[0].id
	db.dependencias.insert(nombre='Oficina de Protección Radiológica', id_sede=1, unidad_de_adscripcion=direccionid, id_jefe_dependencia=user, codigo_registro="UL05")

	# Secciones
	user = db(db.auth_user.email == 'jefsecc@usb.ve').select()[0].id

	# Laboratorio A
	laboratorioid = db(db.dependencias.nombre == 'Laboratorio A').select()[0].id

	usere = db(db.auth_user.email == 'sat-laba@usb.ve').select()[0].id
	db.dependencias.insert(nombre='Alta Tensión', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=usere, codigo_registro="UAAT")
	usere = db(db.auth_user.email == 'scee-laba@usb.ve').select()[0].id
	db.dependencias.insert(nombre='Conversión de Energía Eléctrica', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=usere, codigo_registro="UAEE")

	db.dependencias.insert(nombre='Conversión de Energía Mecánica', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user, codigo_registro="UAEM")
	db.dependencias.insert(nombre='Desarrollo de Modelos y Prototipos', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user, codigo_registro="UAMP")
	db.dependencias.insert(nombre='Dinámica de Máquinas', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user, codigo_registro="UADM")
	db.dependencias.insert(nombre='Fenómenos de Transporte', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user, codigo_registro="UAFT")
	db.dependencias.insert(nombre='Mecánica Computacional', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user, codigo_registro="UAMC")
	db.dependencias.insert(nombre='Mecánica de Fluidos', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user, codigo_registro="UAMF")
	db.dependencias.insert(nombre='Operaciones Unitarias', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user, codigo_registro="UAOU")
	db.dependencias.insert(nombre='Sistemas de Potencia', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user, codigo_registro="UASP")

	# Laboratorio B
	laboratorioid = db(db.dependencias.nombre == 'Laboratorio B').select()[0].id

	usere = db(db.auth_user.email == 'labb-alimentos@usb.ve').select()[0].id
	db.dependencias.insert(nombre='Alimentos', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=usere, codigo_registro="UBAL")
	usere = db(db.auth_user.email == 'labb-bioterio@usb.ve').select()[0].id
	db.dependencias.insert(nombre='Bioterio', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=usere, codigo_registro="UBBI")
	db.dependencias.insert(nombre='Biología Celular', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user, codigo_registro="UBBC")
	db.dependencias.insert(nombre='Biología de Organismos', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user, codigo_registro="UBBO")
	db.dependencias.insert(nombre='Biología Marina', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user, codigo_registro="UBBM")
	db.dependencias.insert(nombre='Ecología', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user, codigo_registro="UBEC")
	db.dependencias.insert(nombre='Físico Química', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user, codigo_registro="UBFQ")
	db.dependencias.insert(nombre='Nutrición', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user, codigo_registro="UBNT")
	db.dependencias.insert(nombre='Polímeros', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user, codigo_registro="UBPO")
	db.dependencias.insert(nombre='Procesos Químicos', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user, codigo_registro="UBPQ")
	db.dependencias.insert(nombre='Química Analítica', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user, codigo_registro="UBQA")
	db.dependencias.insert(nombre='Química General', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user, codigo_registro="UBQG")
	db.dependencias.insert(nombre='Química Inorgánica', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user, codigo_registro="UBQI")
	db.dependencias.insert(nombre='Química Orgánica', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user, codigo_registro="UBQO")


	# Laboratorio C
	laboratorioid = db(db.dependencias.nombre == 'Laboratorio C').select()[0].id

	usere = db(db.auth_user.email == 'labc-read@usb.ve').select()[0].id
	db.dependencias.insert(nombre='Redes, Electrónica Analógica y Digital', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=usere, codigo_registro="UCRE")
	usere = db(db.auth_user.email == 'labc-pss@usb.ve').select()[0].id
	db.dependencias.insert(nombre='Procesamiento de Señales y Sistemas', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=usere, codigo_registro="UCPS")
	db.dependencias.insert(nombre='Comunicaciones', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user, codigo_registro="UCCO")
	db.dependencias.insert(nombre='Instrumentación y Control de Procesos y Sistemas', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user, codigo_registro="UCIC")
	db.dependencias.insert(nombre='Centro de Automatización Industrial', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user, codigo_registro="UCCI")
	db.dependencias.insert(nombre='Electrónica de Potencia', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user, codigo_registro="UCEP")
	db.dependencias.insert(nombre='Sistemas Digitales', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user, codigo_registro="UCSD")
	db.dependencias.insert(nombre='Telecomunicaciones', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user, codigo_registro="UCTE")
	db.dependencias.insert(nombre='Mecatrónica', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user, codigo_registro="UCME")
	db.dependencias.insert(nombre='Control Automático', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user, codigo_registro="UCCA")
	db.dependencias.insert(nombre='Acústica y Comunicaciones', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user, codigo_registro="UCAC")
	db.dependencias.insert(nombre='Estado Sólido', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user, codigo_registro="UCES")
	db.dependencias.insert(nombre='Biomecánica', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user, codigo_registro="UCBI")
	db.dependencias.insert(nombre='Sistemas Biomédicos', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user, codigo_registro="UCSB")
	db.dependencias.insert(nombre='Grupo de Redes Electrónicas y Telemática Aplicada (GRETA)', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user, codigo_registro="UCGE")
	db.dependencias.insert(nombre='Grupo de Procesamiento de Señales (GPS)', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user, codigo_registro="UCGP")
	db.dependencias.insert(nombre='Grupo de Telecomunicaciones (GTEL)', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user, codigo_registro="UCGT")
	db.dependencias.insert(nombre='Grupo de Centro y Automatización Industrial (CAI)', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user, codigo_registro="UCGC")
	db.dependencias.insert(nombre='Grupo de Sistemas Industriales de Electrónica de Potencia (SIEP)', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user, codigo_registro="UCGS")
	db.dependencias.insert(nombre='Grupo de Laboratorio de Investigación en Sistemas de Información (LISI)', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user, codigo_registro="UCGL")
	db.dependencias.insert(nombre='Grupo de Mecatrónica', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user, codigo_registro="UCGM")
	db.dependencias.insert(nombre='Grupo de Biomecánica', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user, codigo_registro="UCGB")
	db.dependencias.insert(nombre='Laboratorio de Control Automático (LCA).', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user, codigo_registro="UC")
	db.dependencias.insert(nombre='Grupo de Energía Alternativa (GEA)', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user, codigo_registro="UC")
	db.dependencias.insert(nombre='Grupo de Laboratorio de Electrónica de Estados Sólidos (LEES)', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user, codigo_registro="UCLC")
	db.dependencias.insert(nombre='Grupo de Biomecánica, Rehabilitación y Procesamiento de Señales (GBRPS)', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user, codigo_registro="UCLE")


	# Laboratorio D
	laboratorioid = db(db.dependencias.nombre == 'Laboratorio D').select()[0].id

	usere = db(db.auth_user.email == 'labd-biofisica@usb.ve').select()[0].id
	db.dependencias.insert(nombre='Biofísica', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=usere, codigo_registro="UDBI")
	usere = db(db.auth_user.email == 'labd-espectrocopia@usb.ve').select()[0].id
	db.dependencias.insert(nombre='Espectroscopía Laser', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=usere, codigo_registro="UDEL")
	db.dependencias.insert(nombre='Física de Estado Sólido', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user, codigo_registro="UDFS")
	db.dependencias.insert(nombre='Física Nuclear', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user, codigo_registro="UDFN")
	db.dependencias.insert(nombre='Geofísica', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user, codigo_registro="UDGF")
	db.dependencias.insert(nombre='Laboratorio de Demostraciones', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user, codigo_registro="UDLD")
	db.dependencias.insert(nombre='Simulaciones de la Materia Condensada', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user, codigo_registro="UDMC")
	db.dependencias.insert(nombre='Óptica', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user, codigo_registro="UDOP")
	db.dependencias.insert(nombre='Óptica e Interferometría', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user, codigo_registro="UDOI")
	db.dependencias.insert(nombre='Óptica Moderna y Aplicada', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user, codigo_registro="UDOM")
	db.dependencias.insert(nombre='Plasma Contínua y Pulsada', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user, codigo_registro="UDPC")
	db.dependencias.insert(nombre='Psicofisiología y Conducta Humana', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user, codigo_registro="UDCH")
	db.dependencias.insert(nombre='Fabricación y Caracterización de Nanomateriales', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user, codigo_registro="UDFC")


	# Laboratorio E
	laboratorioid = db(db.dependencias.nombre == 'Laboratorio E').select()[0].id

	usere = db(db.auth_user.email == 'labe-cat@usb.ve').select()[0].id
	db.dependencias.insert(nombre='Coordinación de Actividades Técnicas', id_sede=1, unidad_de_adscripcion=laboratorioid,
												 id_jefe_dependencia=usere, codigo_registro="UECA")
	usere = db(db.auth_user.email == 'labe-calidad@usb.ve').select()[0].id
	db.dependencias.insert(nombre='Coordinación de Aseguramiento de la Calidad', id_sede=1, unidad_de_adscripcion=laboratorioid,
												 id_jefe_dependencia=usere, codigo_registro="UECC")
	db.dependencias.insert(nombre='Cerámica y Suelos', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user, codigo_registro="UECS")
	db.dependencias.insert(nombre='Corrosión', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user, codigo_registro="UECR")
	db.dependencias.insert(nombre='Materiales', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user, codigo_registro="UEMA")
	db.dependencias.insert(nombre='Metalurgia Química', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user, codigo_registro="UEMQ")
	db.dependencias.insert(nombre='Metrología Dimensional', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user, codigo_registro="UEMD")
	db.dependencias.insert(nombre='Microscopía Electrónica', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user, codigo_registro="UEME")
	db.dependencias.insert(nombre='Polímeros', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user, codigo_registro="UEPO")
	db.dependencias.insert(nombre='Procesos Metalmecánicos', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user, codigo_registro="UEPM")
	db.dependencias.insert(nombre='Procesos Metalúrgicos', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user, codigo_registro="UEPR")


	# Laboratorio F
	laboratorioid = db(db.dependencias.nombre == 'Laboratorio F').select()[0].id

	usere = db(db.auth_user.email == 'labf-ac@usb.ve').select()[0].id
	db.dependencias.insert(nombre='Aulas Computarizadas', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=usere, codigo_registro="UFAC")
	usere = db(db.auth_user.email == 'labf-ccp@usb.ve').select()[0].id
	db.dependencias.insert(nombre='Computacional de Ciencia Política', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=usere, codigo_registro="UFCP")
	db.dependencias.insert(nombre='Informática Educativa', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user, codigo_registro="UFIE")
	db.dependencias.insert(nombre='Lengua - José Santos Urriola', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user, codigo_registro="UFLJ")
	db.dependencias.insert(nombre='Computación', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user, codigo_registro="UFCO")
	db.dependencias.insert(nombre='Redes y Bases de Datos', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user, codigo_registro="UFRB")
	db.dependencias.insert(nombre='Diseño Asistido por Computadora', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user, codigo_registro="UFDC")
	db.dependencias.insert(nombre='Matemáticas y Estadísticas Computacionales', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user, codigo_registro="UFME")
	db.dependencias.insert(nombre='Centro de Estadística y Software Matemático', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user, codigo_registro="UFCS")
	db.dependencias.insert(nombre='Bases de Datos', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user, codigo_registro="UFBD")
	db.dependencias.insert(nombre='Computación Gráfica y Multimedia', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user, codigo_registro="UFCG")
	db.dependencias.insert(nombre='Geomática Urbana', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user, codigo_registro="UFGU")
	db.dependencias.insert(nombre='Inteligencia Artificial', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user, codigo_registro="UFIA")
	db.dependencias.insert(nombre='Investigación en Sistemas de Información', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user, codigo_registro="UFIS")
	db.dependencias.insert(nombre='Lenguajes y Algoritmos', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user, codigo_registro="UFLA")
	db.dependencias.insert(nombre='Digital de Música', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user, codigo_registro="UFDM")
	db.dependencias.insert(nombre='Sistemas Paralelos y Distribuidos', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user, codigo_registro="UFSP")
	db.dependencias.insert(nombre='Computación de Alto Rendimiento', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user, codigo_registro="UFCA")
	db.dependencias.insert(nombre='Estudios Tecnológicos', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user, codigo_registro="UFET")
	db.dependencias.insert(nombre='Idiomas Asistido por Computadoras', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user, codigo_registro="UFIA")


	# Laboratorio G
	laboratorioid = db(db.dependencias.nombre == 'Laboratorio G').select()[0].id

	usere = db(db.auth_user.email == 'labg-cee@usb.ve').select()[0].id
	db.dependencias.insert(nombre='Conversión de Energía Eléctrica', id_sede=2, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user, codigo_registro="UGCE")
	usere = db(db.auth_user.email == 'labg-cem@usb.ve').select()[0].id
	db.dependencias.insert(nombre='Conversión de Energía Mecánica', id_sede=2, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user, codigo_registro="UGCM")
	db.dependencias.insert(nombre='Aeronaves', id_sede=2, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user, codigo_registro="UGAE")
	db.dependencias.insert(nombre='Procesos Mecánicos de Fabricación y Materiales', id_sede=2, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user, codigo_registro="UGPM")
	db.dependencias.insert(nombre='Física', id_sede=2, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user, codigo_registro="UGFI")
	db.dependencias.insert(nombre='Fundamentos de Circuitos Eléctricos', id_sede=2, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user, codigo_registro="UGFC")
	db.dependencias.insert(nombre='Digitales', id_sede=2, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user, codigo_registro="UGDG")
	db.dependencias.insert(nombre='Intrumentación y Control', id_sede=2, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user, codigo_registro="UGIC")
	db.dependencias.insert(nombre='Biomédica', id_sede=2, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user, codigo_registro="UGBI")
	db.dependencias.insert(nombre='Tecnologías de la Información', id_sede=2, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user, codigo_registro="UGTI")
	db.dependencias.insert(nombre='Telemática', id_sede=2, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user, codigo_registro="UGTE")
	db.dependencias.insert(nombre='Comunicaciones', id_sede=2, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user, codigo_registro="UGCO")
	db.dependencias.insert(nombre='Idiomas', id_sede=2, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user, codigo_registro="UGID")
	db.dependencias.insert(nombre='Alimentos y Bebidas', id_sede=2, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user, codigo_registro="UGAB")

# Cargos

if db(db.auth_group).isempty():

		db.auth_group.insert(role='WebMaster',description='Super Usuario')
		db.auth_group.insert(role='Director',description='Director')
		db.auth_group.insert(role='Asistente del Director',description='Asistente del Director')
		db.auth_group.insert(role='Coordinador',description='Coordinación')
		db.auth_group.insert(role='Jefe de Laboratorio',description='Jefe de Laboratorio')
		db.auth_group.insert(role='Jefe de Sección',description='Jefe de Sección')
		db.auth_group.insert(role='Técnico',description='Técnico')
		db.auth_group.insert(role='Personal de Coordinación',description='Personal de Coordinación')
		db.auth_group.insert(role='Gestor de SMyDP',description='Gestor de SMyDP')
		db.auth_group.insert(role='Cliente Interno',description='Cliente Interno')

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
	user = db(db.auth_user.email == 'cinterno@usb.ve').select()[0].id
	dep = db(db.dependencias.nombre == 'Dirección').select()[0].id
	role = db(db.auth_group.role == 'Cliente Interno').select()[0].id

	db.auth_membership.insert(user_id=user, group_id=role)

	user = db(db.auth_user.email == 'webmaster@usb.ve').select()[0].id
	dep = db(db.dependencias.nombre == 'Dirección').select()[0].id
	role = db(db.auth_group.role == 'WebMaster').select()[0].id

	db.auth_membership.insert(user_id=user, group_id=role)

	user = db(db.auth_user.email == 'gestor@usb.ve').select()[0].id
	dep = db(db.dependencias.nombre == 'Dirección').select()[0].id
	role = db(db.auth_group.role == 'Gestor de SMyDP').select()[0].id

	db.auth_membership.insert(user_id=user, group_id=role, dependencia_asociada=dep)

	user = db(db.auth_user.email == 'directassist@usb.ve').select()[0].id
	dep = db(db.dependencias.nombre == 'Dirección').select()[0].id
	role = db(db.auth_group.role == 'Asistente del Director').select()[0].id

	db.auth_membership.insert(user_id=user, group_id=role, dependencia_asociada=dep)

	# user = db(db.auth_user.email == 'personal@usb.ve').select()[0].id
	# dep = db(db.dependencias.nombre == 'Unidad de Administración').select()[0].id
	# role = db(db.auth_group.role == 'Personal de Coordinación').select()[0].id
	#
	# db.auth_membership.insert(user_id=user, group_id=role, dependencia_asociada=dep)

	# user = db(db.auth_user.email == 'tecnico@usb.ve').select()[0].id
	# dep = db(db.dependencias.nombre == 'Alta Tensión').select()[0].id
	# role = db(db.auth_group.role == 'Técnico').select()[0].id

	# db.auth_membership.insert(user_id=user, group_id=role, dependencia_asociada=dep)

	# user = db(db.auth_user.email == 'jefsecc@usb.ve').select()[0].id
	# dep = db(db.dependencias.nombre == 'Alta Tensión').select()[0].id
	# role = db(db.auth_group.role == 'Jefe de Sección').select()[0].id
	#
	# db.auth_membership.insert(user_id=user, group_id=role, dependencia_asociada=dep)
	#
	# user = db(db.auth_user.email == 'jeflab@usb.ve').select()[0].id
	# dep = db(db.dependencias.nombre == 'Laboratorio A').select()[0].id
	# role = db(db.auth_group.role == 'Jefe de Laboratorio').select()[0].id
	#
	# db.auth_membership.insert(user_id=user, group_id=role, dependencia_asociada=dep)
	#
	# user = db(db.auth_user.email == 'coordinador@usb.ve').select()[0].id
	# dep = db(db.dependencias.nombre == 'Unidad de Administración').select()[0].id
	# role = db(db.auth_group.role == 'Coordinador').select()[0].id
	#
	# db.auth_membership.insert(user_id=user, group_id=role, dependencia_asociada=dep)

	# user = db(db.auth_user.email == 'director@usb.ve').select()[0].id
	# dep = db(db.dependencias.nombre == 'Dirección').select()[0].id
	# role = db(db.auth_group.role == 'Director').select()[0].id
	#
	# db.auth_membership.insert(user_id=user, group_id=role, dependencia_asociada=dep)

	# Director

	user = db(db.auth_user.email == 'ulab@usb.ve').select()[0].id
	dep = db(db.dependencias.nombre == 'Dirección').select()[0].id
	role = db(db.auth_group.role == 'Director').select()[0].id

	db.auth_membership.insert(user_id=user, group_id=role, dependencia_asociada=dep)

	# Coordinadores

	user = db(db.auth_user.email == 'ulab-adquisicion@usb.ve').select()[0].id
	dep = db(db.dependencias.nombre == 'Coordinación de Adquisiciones').select()[0].id
	role = db(db.auth_group.role == 'Coordinador').select()[0].id

	db.auth_membership.insert(user_id=user, group_id=role, dependencia_asociada=dep)

	user = db(db.auth_user.email == 'ulab-calidad@usb.ve').select()[0].id
	dep = db(db.dependencias.nombre == 'Coordinación de la Calidad').select()[0].id
	role = db(db.auth_group.role == 'Coordinador').select()[0].id

	db.auth_membership.insert(user_id=user, group_id=role, dependencia_asociada=dep)

	user = db(db.auth_user.email == 'ulab-importaciones@usb.ve').select()[0].id
	dep = db(db.dependencias.nombre == 'Coordinación de Importaciones').select()[0].id
	role = db(db.auth_group.role == 'Coordinador').select()[0].id

	db.auth_membership.insert(user_id=user, group_id=role, dependencia_asociada=dep)


	user = db(db.auth_user.email == 'ulab-administracion@usb.ve').select()[0].id
	dep = db(db.dependencias.nombre == 'Unidad de Administración').select()[0].id
	role = db(db.auth_group.role == 'Coordinador').select()[0].id

	db.auth_membership.insert(user_id=user, group_id=role, dependencia_asociada=dep)

	user = db(db.auth_user.email == 'ulab-pradiologica@usb.ve').select()[0].id
	dep = db(db.dependencias.nombre == 'Oficina de Protección Radiológica').select()[0].id
	role = db(db.auth_group.role == 'Coordinador').select()[0].id

	db.auth_membership.insert(user_id=user, group_id=role, dependencia_asociada=dep)

	# Laboratorios

	user = db(db.auth_user.email == 'usb-laba@usb.ve').select()[0].id
	dep = db(db.dependencias.nombre == 'Laboratorio A').select()[0].id
	role = db(db.auth_group.role == 'Jefe de Laboratorio').select()[0].id

	db.auth_membership.insert(user_id=user, group_id=role, dependencia_asociada=dep)

	user = db(db.auth_user.email == 'usb-labb@usb.ve').select()[0].id
	dep = db(db.dependencias.nombre == 'Laboratorio B').select()[0].id
	role = db(db.auth_group.role == 'Jefe de Laboratorio').select()[0].id

	db.auth_membership.insert(user_id=user, group_id=role, dependencia_asociada=dep)

	user = db(db.auth_user.email == 'usb-labc@usb.ve').select()[0].id
	dep = db(db.dependencias.nombre == 'Laboratorio C').select()[0].id
	role = db(db.auth_group.role == 'Jefe de Laboratorio').select()[0].id

	db.auth_membership.insert(user_id=user, group_id=role, dependencia_asociada=dep)

	user = db(db.auth_user.email == 'usb-labd@usb.ve').select()[0].id
	dep = db(db.dependencias.nombre == 'Laboratorio D').select()[0].id
	role = db(db.auth_group.role == 'Jefe de Laboratorio').select()[0].id

	db.auth_membership.insert(user_id=user, group_id=role, dependencia_asociada=dep)

	user = db(db.auth_user.email == 'usb-labe@usb.ve').select()[0].id
	dep = db(db.dependencias.nombre == 'Laboratorio E').select()[0].id
	role = db(db.auth_group.role == 'Jefe de Laboratorio').select()[0].id

	db.auth_membership.insert(user_id=user, group_id=role, dependencia_asociada=dep)

	user = db(db.auth_user.email == 'usb-labf@usb.ve').select()[0].id
	dep = db(db.dependencias.nombre == 'Laboratorio F').select()[0].id
	role = db(db.auth_group.role == 'Jefe de Laboratorio').select()[0].id

	db.auth_membership.insert(user_id=user, group_id=role, dependencia_asociada=dep)

	user = db(db.auth_user.email == 'usb-labg@usb.ve').select()[0].id
	dep = db(db.dependencias.nombre == 'Laboratorio G').select()[0].id
	role = db(db.auth_group.role == 'Jefe de Laboratorio').select()[0].id

	db.auth_membership.insert(user_id=user, group_id=role, dependencia_asociada=dep)

	# Secciones

	user = db(db.auth_user.email == 'sat-laba@usb.ve').select()[0].id
	dep = db(db.dependencias.nombre == 'Alta Tensión').select()[0].id
	role = db(db.auth_group.role == 'Jefe de Sección').select()[0].id

	db.auth_membership.insert(user_id=user, group_id=role, dependencia_asociada=dep)

	user = db(db.auth_user.email == 'scee-laba@usb.ve').select()[0].id
	dep = db(db.dependencias.nombre == 'Conversión de Energía Eléctrica').select()[0].id
	role = db(db.auth_group.role == 'Jefe de Sección').select()[0].id

	db.auth_membership.insert(user_id=user, group_id=role, dependencia_asociada=dep)

	user = db(db.auth_user.email == 'labb-alimentos@usb.ve').select()[0].id
	dep = db(db.dependencias.nombre == 'Alimentos').select()[0].id
	role = db(db.auth_group.role == 'Jefe de Sección').select()[0].id

	db.auth_membership.insert(user_id=user, group_id=role, dependencia_asociada=dep)

	user = db(db.auth_user.email == 'labb-bioterio@usb.ve').select()[0].id
	dep = db(db.dependencias.nombre == 'Bioterio').select()[0].id
	role = db(db.auth_group.role == 'Jefe de Sección').select()[0].id

	db.auth_membership.insert(user_id=user, group_id=role, dependencia_asociada=dep)

	user = db(db.auth_user.email == 'labc-read@usb.ve').select()[0].id
	dep = db(db.dependencias.nombre == 'Redes, Electrónica Analógica y Digital').select()[0].id
	role = db(db.auth_group.role == 'Jefe de Sección').select()[0].id

	db.auth_membership.insert(user_id=user, group_id=role, dependencia_asociada=dep)

	user = db(db.auth_user.email == 'labc-pss@usb.ve').select()[0].id
	dep = db(db.dependencias.nombre == 'Procesamiento de Señales y Sistemas').select()[0].id
	role = db(db.auth_group.role == 'Jefe de Sección').select()[0].id

	db.auth_membership.insert(user_id=user, group_id=role, dependencia_asociada=dep)

	user = db(db.auth_user.email == 'labd-biofisica@usb.ve').select()[0].id
	dep = db(db.dependencias.nombre == 'Biofísica').select()[0].id
	role = db(db.auth_group.role == 'Jefe de Sección').select()[0].id

	db.auth_membership.insert(user_id=user, group_id=role, dependencia_asociada=dep)

	user = db(db.auth_user.email == 'labd-espectrocopia@usb.ve').select()[0].id
	dep = db(db.dependencias.nombre == 'Espectroscopía Laser').select()[0].id
	role = db(db.auth_group.role == 'Jefe de Sección').select()[0].id

	db.auth_membership.insert(user_id=user, group_id=role, dependencia_asociada=dep)

	user = db(db.auth_user.email == 'labe-cat@usb.ve').select()[0].id
	dep = db(db.dependencias.nombre == 'Coordinación de Actividades Técnicas').select()[0].id
	role = db(db.auth_group.role == 'Jefe de Sección').select()[0].id

	db.auth_membership.insert(user_id=user, group_id=role, dependencia_asociada=dep)

	user = db(db.auth_user.email == 'labe-calidad@usb.ve').select()[0].id
	dep = db(db.dependencias.nombre == 'Coordinación de Aseguramiento de la Calidad').select()[0].id
	role = db(db.auth_group.role == 'Jefe de Sección').select()[0].id

	db.auth_membership.insert(user_id=user, group_id=role, dependencia_asociada=dep)

	user = db(db.auth_user.email == 'labf-ac@usb.ve').select()[0].id
	dep = db(db.dependencias.nombre == 'Aulas Computarizadas').select()[0].id
	role = db(db.auth_group.role == 'Jefe de Sección').select()[0].id

	db.auth_membership.insert(user_id=user, group_id=role, dependencia_asociada=dep)

	user = db(db.auth_user.email == 'labf-ccp@usb.ve').select()[0].id
	dep = db(db.dependencias.nombre == 'Computacional de Ciencia Política').select()[0].id
	role = db(db.auth_group.role == 'Jefe de Sección').select()[0].id

	db.auth_membership.insert(user_id=user, group_id=role, dependencia_asociada=dep)

	user = db(db.auth_user.email == 'labg-cee@usb.ve').select()[0].id
	dep = db(db.dependencias.nombre == 'Conversión de Energía Eléctrica').select()[0].id
	role = db(db.auth_group.role == 'Jefe de Sección').select()[0].id

	db.auth_membership.insert(user_id=user, group_id=role, dependencia_asociada=dep)

	user = db(db.auth_user.email == 'labg-cem@usb.ve').select()[0].id
	dep = db(db.dependencias.nombre == 'Conversión de Energía Mecánica').select()[0].id
	role = db(db.auth_group.role == 'Jefe de Sección').select()[0].id

	db.auth_membership.insert(user_id=user, group_id=role, dependencia_asociada=dep)

# Ficha de Personal Permanente

if db(db.t_Personal).isempty():
	# Personal Basico sin dependencia + Jefe de Seccion "de Prueba"
	
	# Cliente Interno
	user = db(db.auth_user.email == 'cinterno@usb.ve').select()[0].id
	dep = db(db.dependencias.nombre == 'Dirección').select()[0].id

	db.t_Personal.insert(f_nombre = "Cliente Interno",f_apellido = "ULAB", f_categoria = "Administrativo", f_cargo = "Cliente Interno",
											 f_ci = 12345678, f_email='cinterno@usb.ve', f_estatus='Activo',
											 f_usuario=user, f_dependencia=dep)
	
	# Super Usuario

	user = db(db.auth_user.email == 'webmaster@usb.ve').select()[0].id
	dep = db(db.dependencias.nombre == 'Dirección').select()[0].id

	db.t_Personal.insert(f_nombre="Super Usuario", f_apellido = "ULAB", f_categoria="Administrativo", f_cargo="Super Usuario",
											 f_ci=12345677, f_email='webmaster@usb.ve', f_estatus='Activo',
											 f_usuario=user, f_dependencia=dep)
	
	# Asistente del Director

	user = db(db.auth_user.email == 'directassist@usb.ve').select()[0].id
	dep = db(db.dependencias.nombre == 'Dirección').select()[0].id

	db.t_Personal.insert(f_nombre="Asistente del Director", f_apellido = "ULAB", f_categoria="Administrativo", f_cargo="Asistente del Director",
											 f_ci=12345676, f_email='directassist@usb.ve', f_estatus='Activo',
											 f_usuario=user, f_dependencia=dep)
	
	# Gestor de Sustancias

	user = db(db.auth_user.email == 'gestor@usb.ve').select()[0].id
	dep = db(db.dependencias.nombre == 'Dirección').select()[0].id

	db.t_Personal.insert(f_nombre="Gestor de Sustancias", f_apellido = "ULAB", f_categoria="Administrativo", f_cargo="Gestor de Sustancias",
											 f_ci=12345675, f_email='gestor@usb.ve', f_estatus='Activo',
											 f_usuario=user, f_dependencia=dep)
	
	# Jefe de Seccion

	user = db(db.auth_user.email == 'jefsecc@usb.ve').select()[0].id
	dep = db(db.dependencias.nombre == 'Dirección').select()[0].id

	db.t_Personal.insert(f_nombre="Jefe de Sección", f_apellido = "ULAB", f_categoria="Administrativo", f_cargo="Jefe de Sección",
											 f_ci=12345674, f_email='jefsecc@usb.ve', f_estatus='Activo',
											 f_usuario=user, f_dependencia=dep)
	
	# Personal Permanente - Representante de Dependencia
	
	# Director

	user = db(db.auth_user.email == 'ulab@usb.ve').select()[0].id
	dep = db(db.dependencias.nombre == 'Dirección').select()[0].id

	db.t_Personal.insert(f_nombre="Director", f_apellido = "ULAB", f_categoria="Administrativo", f_cargo="Director",
						 f_ci=12345674, f_email='ulab@usb.ve', f_estatus='Activo',
						 f_usuario=user, f_dependencia=dep)
	
	# Coordinadores

	# Coordinación de Adquisiciones
	user = db(db.auth_user.email == 'ulab-adquisicion@usb.ve').select()[0].id
	dep = db(db.dependencias.nombre == 'Coordinación de Adquisiciones').select()[0].id

	db.t_Personal.insert(f_nombre="Coordinador de Adquisiciones", f_apellido = "ULAB", f_categoria="Administrativo", f_cargo="Coordinador",
						 f_ci=12345673, f_email='ulab-adquisicion@usb.ve', f_estatus='Activo',
						 f_usuario=user, f_dependencia=dep)

	# Coordinación de la Calidad
	user = db(db.auth_user.email == 'ulab-calidad@usb.ve').select()[0].id
	dep = db(db.dependencias.nombre == 'Coordinación de la Calidad').select()[0].id

	db.t_Personal.insert(f_nombre="Coordinador de Calidad", f_apellido = "ULAB", f_categoria="Administrativo", f_cargo="Coordinador",
						 f_ci=12345674, f_email='ulab-calidad@usb.ve', f_estatus='Activo',
						 f_usuario=user, f_dependencia=dep)

	# Coordinación de Importaciones
	user = db(db.auth_user.email == 'ulab-importaciones@usb.ve').select()[0].id
	dep = db(db.dependencias.nombre == 'Coordinación de Importaciones').select()[0].id

	db.t_Personal.insert(f_nombre="Coordinador de Importaciones", f_apellido = "ULAB", f_categoria="Administrativo", f_cargo="Coordinador",
						 f_ci=12345674, f_email='ulab-importaciones@usb.ve', f_estatus='Activo',
						 f_usuario=user, f_dependencia=dep)

	# Unidad de Administración
	user = db(db.auth_user.email == 'ulab-administracion@usb.ve').select()[0].id
	dep = db(db.dependencias.nombre == 'Unidad de Administración').select()[0].id

	db.t_Personal.insert(f_nombre="Administrador", f_apellido = "ULAB", f_categoria="Administrativo", f_cargo="Coordinador",
						 f_ci=12345674, f_email='ulab-administracion@usb.ve', f_estatus='Activo',
						 f_usuario=user, f_dependencia=dep)

	# Oficina de Proteccion Radiologica
	user = db(db.auth_user.email == 'ulab-pradiologica@usb.ve').select()[0].id
	dep = db(db.dependencias.nombre == 'Dirección').select()[0].id

	db.t_Personal.insert(f_nombre="Encargado de la Oficina de Proteccion Radiológica", f_apellido = "ULAB", f_categoria="Administrativo", f_cargo="Coordinador",
						 f_ci=12345674, f_email='ulab-pradiologica@usb.ve', f_estatus='Activo',
						 f_usuario=user, f_dependencia=dep)
	
	# Jefes de Laboratorios

	# Laboratorio A
	user = db(db.auth_user.email == 'usb-laba@usb.ve').select()[0].id
	dep = db(db.dependencias.nombre == 'Laboratorio A').select()[0].id

	db.t_Personal.insert(f_nombre="Jefe del Laboratorio A", f_apellido = "ULAB", f_categoria="Administrativo", f_cargo="Jefe de Laboratorio",
						 f_ci=12345674, f_email='usb-laba@usb.ve', f_estatus='Activo',
						 f_usuario=user, f_dependencia=dep)

	# Laboratorio B
	user = db(db.auth_user.email == 'usb-labb@usb.ve').select()[0].id
	dep = db(db.dependencias.nombre == 'Laboratorio B').select()[0].id

	db.t_Personal.insert(f_nombre="Jefe del Laboratorio B", f_apellido = "ULAB", f_categoria="Administrativo", f_cargo="Jefe de Laboratorio",
						 f_ci=12345674, f_email='usb-labb@usb.ve', f_estatus='Activo',
						 f_usuario=user, f_dependencia=dep)

	# Laboratorio C
	user = db(db.auth_user.email == 'usb-labc@usb.ve').select()[0].id
	dep = db(db.dependencias.nombre == 'Laboratorio C').select()[0].id

	db.t_Personal.insert(f_nombre="Jefe del Laboratorio C", f_apellido = "ULAB", f_categoria="Administrativo", f_cargo="Jefe de Laboratorio",
						 f_ci=12345674, f_email='usb-labc@usb.ve', f_estatus='Activo',
						 f_usuario=user, f_dependencia=dep)

	# Laboratorio D
	user = db(db.auth_user.email == 'usb-labd@usb.ve').select()[0].id
	dep = db(db.dependencias.nombre == 'Laboratorio D').select()[0].id

	db.t_Personal.insert(f_nombre="Jefe del Laboratorio D", f_apellido = "ULAB", f_categoria="Administrativo", f_cargo="Jefe de Laboratorio",
						 f_ci=12345674, f_email='usb-labd@usb.ve', f_estatus='Activo',
						 f_usuario=user, f_dependencia=dep)

	# Laboratorio E
	user = db(db.auth_user.email == 'usb-labe@usb.ve').select()[0].id
	dep = db(db.dependencias.nombre == 'Laboratorio E').select()[0].id

	db.t_Personal.insert(f_nombre="Jefe del Laboratorio E", f_apellido = "ULAB", f_categoria="Administrativo", f_cargo="Jefe de Laboratorio",
						 f_ci=12345674, f_email='usb-labe@usb.ve', f_estatus='Activo',
						 f_usuario=user, f_dependencia=dep)

	# Laboratorio F
	user = db(db.auth_user.email == 'usb-labf@usb.ve').select()[0].id
	dep = db(db.dependencias.nombre == 'Laboratorio F').select()[0].id

	db.t_Personal.insert(f_nombre="Jefe del Laboratorio F", f_apellido = "ULAB", f_categoria="Administrativo", f_cargo="Jefe de Laboratorio",
						 f_ci=12345674, f_email='usb-labf@usb.ve', f_estatus='Activo',
						 f_usuario=user, f_dependencia=dep)

	# Laboratorio G
	user = db(db.auth_user.email == 'usb-labg@usb.ve').select()[0].id
	dep = db(db.dependencias.nombre == 'Laboratorio G').select()[0].id

	db.t_Personal.insert(f_nombre="Jefe del Laboratorio G", f_apellido = "ULAB", f_categoria="Administrativo", f_cargo="Jefe de Laboratorio",
						 f_ci=12345674, f_email='usb-labg@usb.ve', f_estatus='Activo',
						 f_usuario=user, f_dependencia=dep)
	
	# Jefes de Seccion

	# Lab A

	# Alta Tension

	user = db(db.auth_user.email == 'sat-laba@usb.ve').select()[0].id
	dep = db(db.dependencias.nombre == 'Alta Tensión').select()[0].id

	db.t_Personal.insert(f_nombre="Jefe de Alta Tensión", f_apellido = "ULAB", f_categoria="Administrativo", f_cargo="Jefe de Sección",
						 f_ci=12345674, f_email='sat-laba@usb.ve', f_estatus='Activo',
						 f_usuario=user, f_dependencia=dep)

	# Conversión de Energía Eléctrica

	user = db(db.auth_user.email == 'scee-laba@usb.ve').select()[0].id
	dep = db(db.dependencias.nombre == 'Conversión de Energía Eléctrica').select()[0].id

	db.t_Personal.insert(f_nombre="Jefe de Conversión de Energía Eléctrica", f_apellido = "ULAB", f_categoria="Administrativo", f_cargo="Jefe de Sección",
						 f_ci=12345674, f_email='scee-laba@usb.ve', f_estatus='Activo',
						 f_usuario=user, f_dependencia=dep)

	# Lab B

	# Alimentos

	user = db(db.auth_user.email == 'labb-alimentos@usb.ve').select()[0].id
	dep = db(db.dependencias.nombre == 'Alimentos').select()[0].id

	db.t_Personal.insert(f_nombre="Jefe de Alimentos", f_apellido = "ULAB", f_categoria="Administrativo", f_cargo="Jefe de Sección",
						 f_ci=12345674, f_email='labb-alimentos@usb.ve', f_estatus='Activo',
						 f_usuario=user, f_dependencia=dep)

	# Bioterio

	user = db(db.auth_user.email == 'labb-bioterio@usb.ve').select()[0].id
	dep = db(db.dependencias.nombre == 'Bioterio').select()[0].id

	db.t_Personal.insert(f_nombre="Jefe de Bioterio", f_apellido = "ULAB", f_categoria="Administrativo", f_cargo="Jefe de Sección",
						 f_ci=12345674, f_email='labb-bioterio@usb.ve', f_estatus='Activo',
						 f_usuario=user, f_dependencia=dep)

	# Lab C

	# Redes, Electrónica Analógica y Digital

	user = db(db.auth_user.email == 'labc-read@usb.ve').select()[0].id
	dep = db(db.dependencias.nombre == 'Redes, Electrónica Analógica y Digital').select()[0].id

	db.t_Personal.insert(f_nombre="Jefe de Redes, Electrónica Analógica y Digital", f_apellido = "ULAB", f_categoria="Administrativo", f_cargo="Jefe de Sección",
						 f_ci=12345674, f_email='labc-read@usb.ve', f_estatus='Activo',
						 f_usuario=user, f_dependencia=dep)

	# Procesamiento de Señales y Sistemas

	user = db(db.auth_user.email == 'labc-pss@usb.ve').select()[0].id
	dep = db(db.dependencias.nombre == 'Procesamiento de Señales y Sistemas').select()[0].id

	db.t_Personal.insert(f_nombre="Jefe de Procesamiento de Señales y Sistemas", f_apellido = "ULAB", f_categoria="Administrativo", f_cargo="Jefe de Sección",
						 f_ci=12345674, f_email='labc-pss@usb.ve', f_estatus='Activo',
						 f_usuario=user, f_dependencia=dep)

	# Lab D

	# Biofísica

	user = db(db.auth_user.email == 'labd-biofisica@usb.ve').select()[0].id
	dep = db(db.dependencias.nombre == 'Biofísica').select()[0].id

	db.t_Personal.insert(f_nombre="Jefe de Biofísica", f_apellido = "ULAB", f_categoria="Administrativo", f_cargo="Jefe de Sección",
						 f_ci=12345674, f_email='labd-biofisica@usb.ve', f_estatus='Activo',
						 f_usuario=user, f_dependencia=dep)

	# Espectroscopía Laser

	user = db(db.auth_user.email == 'labd-espectrocopia@usb.ve').select()[0].id
	dep = db(db.dependencias.nombre == 'Espectroscopía Laser').select()[0].id

	db.t_Personal.insert(f_nombre="Jefe de Espectroscopía Laser", f_apellido = "ULAB", f_categoria="Administrativo", f_cargo="Jefe de Sección",
						 f_ci=12345674, f_email='labd-espectrocopia@usb.ve', f_estatus='Activo',
						 f_usuario=user, f_dependencia=dep)

	# Lab E

	# Coordinación de Actividades Técnicas

	user = db(db.auth_user.email == 'labe-cat@usb.ve').select()[0].id
	dep = db(db.dependencias.nombre == 'Coordinación de Actividades Técnicas').select()[0].id

	db.t_Personal.insert(f_nombre="Jefe de Coordinación de Actividades Técnicas", f_apellido = "ULAB", f_categoria="Administrativo", f_cargo="Jefe de Sección",
						 f_ci=12345674, f_email='labe-cat@usb.ve', f_estatus='Activo',
						 f_usuario=user, f_dependencia=dep)

	# Coordinación de Aseguramiento de la Calidad

	user = db(db.auth_user.email == 'labe-calidad@usb.ve').select()[0].id
	dep = db(db.dependencias.nombre == 'Coordinación de Aseguramiento de la Calidad').select()[0].id

	db.t_Personal.insert(f_nombre="Jefe de Coordinación de Aseguramiento de la Calidad", f_apellido = "ULAB", f_categoria="Administrativo", f_cargo="Jefe de Sección",
						 f_ci=12345674, f_email='labe-calidad@usb.ve', f_estatus='Activo',
						 f_usuario=user, f_dependencia=dep)


	# Lab F

	# Aulas Computarizadas

	user = db(db.auth_user.email == 'labf-ac@usb.ve').select()[0].id
	dep = db(db.dependencias.nombre == 'Aulas Computarizadas').select()[0].id

	db.t_Personal.insert(f_nombre="Jefe de Aulas Computarizadas", f_apellido = "ULAB", f_categoria="Administrativo", f_cargo="Jefe de Sección",
						 f_ci=12345674, f_email='labf-ac@usb.ve', f_estatus='Activo',
						 f_usuario=user, f_dependencia=dep)

	# Computacional de Ciencia Política

	user = db(db.auth_user.email == 'labf-ccp@usb.ve').select()[0].id
	dep = db(db.dependencias.nombre == 'Computacional de Ciencia Política').select()[0].id

	db.t_Personal.insert(f_nombre="Jefe de Computacional de Ciencia Política", f_apellido = "ULAB", f_categoria="Administrativo", f_cargo="Jefe de Sección",
						 f_ci=12345674, f_email='labf-ccp@usb.ve', f_estatus='Activo',
						 f_usuario=user, f_dependencia=dep)

	# Lab G

	# Conversión de Energía Eléctrica

	user = db(db.auth_user.email == 'labg-cee@usb.ve').select()[0].id
	dep = db(db.dependencias.nombre == 'Conversión de Energía Eléctrica' and db.dependencias.id_sede == 2).select()[0].id

	db.t_Personal.insert(f_nombre="Jefe de Conversión de Energía Eléctrica", f_apellido = "ULAB", f_categoria="Administrativo", f_cargo="Jefe de Sección",
						 f_ci=12345674, f_email='labg-cee@usb.ve', f_estatus='Activo',
						 f_usuario=user, f_dependencia=dep)

	# Conversión de Energía Mecánica

	user = db(db.auth_user.email == 'labg-cem@usb.ve').select()[0].id
	dep = db(db.dependencias.nombre == 'Conversión de Energía Mecánica' and db.dependencias.id_sede == 2).select()[0].id

	db.t_Personal.insert(f_nombre="Conversión de Energía Mecánica", f_apellido = "ULAB", f_categoria="Administrativo", f_cargo="Jefe de Sección",
						 f_ci=12345674, f_email='labg-cem@usb.ve', f_estatus='Activo',
						 f_usuario=user, f_dependencia=dep)