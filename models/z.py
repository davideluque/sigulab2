###############################################################################
#
# ESTE ARCHIVO SE ENCARGARA DE POBLAR LA BASE DE DATOS CON DATOS BASICOS.
# EL NOMBRE ES "Z" DEBIDO A QUE ESTE ES EL ULTIMO MODELO QUE DEBE CORRER.
# (ALFABETICAMENTE)
# ToDo Acomodar inserts para las tablas que cambiaron (Dependencias le hace falta jefe principalmente)
###############################################################################

# Usuarios Basicos

if db(db.auth_user).isempty():
  db.auth_user.insert(first_name="Personal", last_name="ULAB", email='personal@usb.ve',
                      password=db.auth_user.password.validate('0000')[0])

  db.auth_user.insert(first_name="Técnico", last_name="ULAB", email='tecnico@usb.ve',
                      password=db.auth_user.password.validate('0000')[0])

  db.auth_user.insert(first_name="Jefe de Sección", last_name="ULAB", email='jefsecc@usb.ve',
                      password=db.auth_user.password.validate('0000')[0])

  db.auth_user.insert(first_name="Jefe de Laboratorio", last_name="ULAB", email='jeflab@usb.ve',
                      password=db.auth_user.password.validate('0000')[0])

  db.auth_user.insert(first_name="Gestor de Sustancias", last_name="ULAB", email='gestor@usb.ve',
                      password=db.auth_user.password.validate('0000')[0])

  db.auth_user.insert(first_name="Coordinador", last_name="ULAB", email='coordinador@usb.ve',
                      password=db.auth_user.password.validate('0000')[0])

  db.auth_user.insert(first_name="Director", last_name="ULAB", email='director@usb.ve',
                      password=db.auth_user.password.validate('0000')[0])

  db.auth_user.insert(first_name="Super", last_name="Usuario", email='webmaster@usb.ve',
                      password=db.auth_user.password.validate('0000')[0])

  db.auth_user.insert(first_name="Cliente", last_name="Interno", email='cinterno@usb.ve',
                      password=db.auth_user.password.validate('0000')[0])

  db.auth_user.insert(first_name="Asistente del Director", last_name="ULAB", email='directassist@usb.ve',
                      password=db.auth_user.password.validate('0000')[0])

# Sedes

if db(db.sedes).isempty():
  db.sedes.insert(nombre="Sartenejas")
  db.sedes.insert(nombre="Litoral")

# Dependencias
# Se asignara un Jefe "Basico" de prueba para cada dependencia, esto permitira probar la funcionalidad de
# las distintas partes del sistema que lo necesiten.

if db(db.dependencias).isempty():
  # Direccion
  user = db(db.auth_user.email == 'director@usb.ve').select()[0].id
  db.dependencias.insert(nombre='Dirección', id_sede=1, id_jefe_dependencia=user)

  direccionid = db(db.dependencias.nombre == 'Dirección').select()[0].id

  # Laboratorios
  user = db(db.auth_user.email == 'jeflab@usb.ve').select()[0].id

  db.dependencias.insert(nombre='Laboratorio A', id_sede=1, unidad_de_adscripcion=direccionid, id_jefe_dependencia=user)
  db.dependencias.insert(nombre='Laboratorio B', id_sede=1, unidad_de_adscripcion=direccionid, id_jefe_dependencia=user)
  db.dependencias.insert(nombre='Laboratorio C', id_sede=1, unidad_de_adscripcion=direccionid, id_jefe_dependencia=user)
  db.dependencias.insert(nombre='Laboratorio D', id_sede=1, unidad_de_adscripcion=direccionid, id_jefe_dependencia=user)
  db.dependencias.insert(nombre='Laboratorio E', id_sede=1, unidad_de_adscripcion=direccionid, id_jefe_dependencia=user)
  db.dependencias.insert(nombre='Laboratorio F', id_sede=1, unidad_de_adscripcion=direccionid, id_jefe_dependencia=user)
  db.dependencias.insert(nombre='Laboratorio G', id_sede=2, unidad_de_adscripcion=direccionid, id_jefe_dependencia=user)

  # Coordinaciones
  user = db(db.auth_user.email == 'coordinador@usb.ve').select()[0].id

  db.dependencias.insert(nombre='Unidad de Administración', id_sede=1, unidad_de_adscripcion=direccionid, id_jefe_dependencia=user)
  db.dependencias.insert(nombre='Coordinación de Adquisiciones', id_sede=1, unidad_de_adscripcion=direccionid, id_jefe_dependencia=user)
  db.dependencias.insert(nombre='Coordinación de Importaciones', id_sede=1, unidad_de_adscripcion=direccionid, id_jefe_dependencia=user)
  db.dependencias.insert(nombre='Coordinación de la Calidad', id_sede=1, unidad_de_adscripcion=direccionid, id_jefe_dependencia=user)
  db.dependencias.insert(nombre='Oficina de Protección Radiológica', id_sede=1, unidad_de_adscripcion=direccionid, id_jefe_dependencia=user)

  # Secciones
  user = db(db.auth_user.email == 'jefsecc@usb.ve').select()[0].id

  # Laboratorio A
  laboratorioid = db(db.dependencias.nombre == 'Laboratorio A').select()[0].id

  db.dependencias.insert(nombre='Alta Tensión', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user)
  db.dependencias.insert(nombre='Conversión de Energía Eléctrica', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user)
  db.dependencias.insert(nombre='Conversión de Energía Mecánica', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user)
  db.dependencias.insert(nombre='Desarrollo de Modelos y Prototipos', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user)
  db.dependencias.insert(nombre='Dinámica de Máquinas', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user)
  db.dependencias.insert(nombre='Fenómenos de Transporte', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user)
  db.dependencias.insert(nombre='Mecánica Computacional', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user)
  db.dependencias.insert(nombre='Mecánica de Fluidos', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user)
  db.dependencias.insert(nombre='Operaciones Unitarias', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user)
  db.dependencias.insert(nombre='Sistemas de Potencia', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user)
  

  # Laboratorio B
  laboratorioid = db(db.dependencias.nombre == 'Laboratorio B').select()[0].id

  db.dependencias.insert(nombre='Alimentos', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user)
  db.dependencias.insert(nombre='Bioterio', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user)
  db.dependencias.insert(nombre='Biología Celular', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user)
  db.dependencias.insert(nombre='Biología de Organismos', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user)
  db.dependencias.insert(nombre='Biología Marina', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user)
  db.dependencias.insert(nombre='Ecología', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user)
  db.dependencias.insert(nombre='Físico Química', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user)
  db.dependencias.insert(nombre='Nutrición', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user)
  db.dependencias.insert(nombre='Polímeros', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user)
  db.dependencias.insert(nombre='Procesos Químicos', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user)
  db.dependencias.insert(nombre='Química Analítica', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user)
  db.dependencias.insert(nombre='Química General', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user)
  db.dependencias.insert(nombre='Química Inorgánica', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user)
  db.dependencias.insert(nombre='Química Orgánica', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user)


  # Laboratorio C
  laboratorioid = db(db.dependencias.nombre == 'Laboratorio C').select()[0].id

  db.dependencias.insert(nombre='Redes, Electrónica Analógica y Digital', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user)
  db.dependencias.insert(nombre='Procesamiento de Señales y Sistemas', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user)
  db.dependencias.insert(nombre='Comunicaciones', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user)
  db.dependencias.insert(nombre='Instrumentación y Control de Procesos y Sistemas', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user)
  db.dependencias.insert(nombre='Centro de Automatización Industrial', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user)
  db.dependencias.insert(nombre='Electrónica de Potencia', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user)
  db.dependencias.insert(nombre='Sistemas Digitales', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user)
  db.dependencias.insert(nombre='Telecomunicaciones', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user)
  db.dependencias.insert(nombre='Mecatrónica', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user)
  db.dependencias.insert(nombre='Control Automático', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user)
  db.dependencias.insert(nombre='Acústica y Comunicaciones', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user)
  db.dependencias.insert(nombre='Estado Sólido', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user)
  db.dependencias.insert(nombre='Biomecánica', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user)
  db.dependencias.insert(nombre='Sistemas Biomédicos', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user)
  db.dependencias.insert(nombre='Procesamiento de Señales y Sistemas', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user)
  db.dependencias.insert(nombre='Grupo de Redes Electrónicas y Telemática Aplicada (GRETA)', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user)
  db.dependencias.insert(nombre='Grupo de Procesamiento de Señales (GPS)', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user)
  db.dependencias.insert(nombre='Grupo de Telecomunicaciones (GTEL)', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user)
  db.dependencias.insert(nombre='Grupo de Centro y Automatización Industrial (CAI)', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user)
  db.dependencias.insert(nombre='Grupo de Sistemas Industriales de Electrónica de Potencia (SIEP)', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user)
  db.dependencias.insert(nombre='Grupo de Laboratorio de Investigación en Sistemas de Información (LISI)', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user)
  db.dependencias.insert(nombre='Grupo de Mecatrónica', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user)
  db.dependencias.insert(nombre='Grupo de Biomecánica', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user)
  db.dependencias.insert(nombre='Laboratorio de Control Automático (LCA).', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user)
  db.dependencias.insert(nombre='Grupo de Energía Alternativa (GEA)', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user)
  db.dependencias.insert(nombre='Grupo de Laboratorio de Electrónica de Estados Sólidos (LEES)', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user)
  db.dependencias.insert(nombre='Grupo de Biomecánica, Rehabilitación y Procesamiento de Señales (GBRPS)', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user)


  # Laboratorio D
  laboratorioid = db(db.dependencias.nombre == 'Laboratorio D').select()[0].id

  db.dependencias.insert(nombre='Biofísica', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user)
  db.dependencias.insert(nombre='Espectroscopía Laser', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user)
  db.dependencias.insert(nombre='Física de Estado Sólido', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user)
  db.dependencias.insert(nombre='Física Nuclear', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user)
  db.dependencias.insert(nombre='Geofísica', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user)
  db.dependencias.insert(nombre='Laboratorio de Demostraciones', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user)
  db.dependencias.insert(nombre='Simulaciones de la Materia Condensada', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user)
  db.dependencias.insert(nombre='Óptica', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user)
  db.dependencias.insert(nombre='Óptica e Interferometría', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user)
  db.dependencias.insert(nombre='Óptica Moderna y Aplicada', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user)
  db.dependencias.insert(nombre='Plasma Contínua y Pulsada', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user)
  db.dependencias.insert(nombre='Psicofisiología y Conducta Humana', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user)
  db.dependencias.insert(nombre='Fabricación y Caracterización de Nanomateriales', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user)


  # Laboratorio E
  laboratorioid = db(db.dependencias.nombre == 'Laboratorio E').select()[0].id

  db.dependencias.insert(nombre='Cerámica y Suelos', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user)
  db.dependencias.insert(nombre='Corrosión', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user)
  db.dependencias.insert(nombre='Materiales', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user)
  db.dependencias.insert(nombre='Metalurgia Química', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user)
  db.dependencias.insert(nombre='Metrología Dimensional', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user)
  db.dependencias.insert(nombre='Microscopía Electrónica', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user)
  db.dependencias.insert(nombre='Polímeros', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user)
  db.dependencias.insert(nombre='Procesos Metalmecánicos', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user)
  db.dependencias.insert(nombre='Procesos Metalúrgicos', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user)


  # Laboratorio F
  laboratorioid = db(db.dependencias.nombre == 'Laboratorio F').select()[0].id

  db.dependencias.insert(nombre='Aulas Computarizadas', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user)
  db.dependencias.insert(nombre='Computacional de Ciencia Política', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user)
  db.dependencias.insert(nombre='Informática Educativa', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user)
  db.dependencias.insert(nombre='Lengua - José Santos Urriola', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user)
  db.dependencias.insert(nombre='Computación', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user)
  db.dependencias.insert(nombre='Redes y Bases de Datos', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user)
  db.dependencias.insert(nombre='Diseño Asistido por Computadora', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user)
  db.dependencias.insert(nombre='Matemáticas y Estadísticas Computacionales', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user)
  db.dependencias.insert(nombre='Centro de Estadística y Software Matemático', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user)
  db.dependencias.insert(nombre='Bases de Datos', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user)
  db.dependencias.insert(nombre='Computación Gráfica y Multimedia', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user)
  db.dependencias.insert(nombre='Geomática Urbana', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user)
  db.dependencias.insert(nombre='Inteligencia Artificial', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user)
  db.dependencias.insert(nombre='Investigación en Sistemas de Información', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user)
  db.dependencias.insert(nombre='Lenguajes y Algoritmos', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user)
  db.dependencias.insert(nombre='Digital de Música', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user)
  db.dependencias.insert(nombre='Sistemas Paralelos y Distribuidos', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user)
  db.dependencias.insert(nombre='Computación de Alto Rendimiento', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user)
  db.dependencias.insert(nombre='Estudios Tecnológicos', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user)
  db.dependencias.insert(nombre='Idiomas Asistido por Computadoras', id_sede=1, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user)


  # Laboratorio G
  laboratorioid = db(db.dependencias.nombre == 'Laboratorio G').select()[0].id

  db.dependencias.insert(nombre='Conversión de Energía Eléctrica', id_sede=2, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user)
  db.dependencias.insert(nombre='Conversión de Energía Mecánica', id_sede=2, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user)
  db.dependencias.insert(nombre='Aeronaves', id_sede=2, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user)
  db.dependencias.insert(nombre='Procesos Mecánicos de Fabricación y Materiales', id_sede=2, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user)
  db.dependencias.insert(nombre='Física', id_sede=2, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user)
  db.dependencias.insert(nombre='Fundamentos de Circuitos Eléctricos', id_sede=2, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user)
  db.dependencias.insert(nombre='Digitales', id_sede=2, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user)
  db.dependencias.insert(nombre='Intrumentación y Control', id_sede=2, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user)
  db.dependencias.insert(nombre='Biomédica', id_sede=2, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user)
  db.dependencias.insert(nombre='Tecnologías de la Información', id_sede=2, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user)
  db.dependencias.insert(nombre='Telemática', id_sede=2, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user)
  db.dependencias.insert(nombre='Comunicaciones', id_sede=2, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user)
  db.dependencias.insert(nombre='Idiomas', id_sede=2, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user)
  db.dependencias.insert(nombre='Alimentos y Bebidas', id_sede=2, unidad_de_adscripcion=laboratorioid, id_jefe_dependencia=user)

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
  role = db(db.auth_group.role == 'Cliente Interno').select()[0].id

  db.auth_membership.insert(user_id=user, group_id=role)

  user = db(db.auth_user.email == 'gestor@usb.ve').select()[0].id
  dep = db(db.dependencias.nombre == 'Dirección').select()[0].id
  role = db(db.auth_group.role == 'Gestor de SMyDP').select()[0].id

  db.auth_membership.insert(user_id=user, group_id=role, dependencia_asociada=dep)

  user = db(db.auth_user.email == 'personal@usb.ve').select()[0].id
  dep = db(db.dependencias.nombre == 'Dirección').select()[0].id
  role = db(db.auth_group.role == 'Personal de Coordinación').select()[0].id

  db.auth_membership.insert(user_id=user, group_id=role, dependencia_asociada=dep)

  user = db(db.auth_user.email == 'tecnico@usb.ve').select()[0].id
  dep = db(db.dependencias.nombre == 'Alta Tensión').select()[0].id
  role = db(db.auth_group.role == 'Técnico').select()[0].id

  db.auth_membership.insert(user_id=user, group_id=role, dependencia_asociada=dep)

  user = db(db.auth_user.email == 'jefsecc@usb.ve').select()[0].id
  dep = db(db.dependencias.nombre == 'Alta Tensión').select()[0].id
  role = db(db.auth_group.role == 'Jefe de Sección').select()[0].id

  db.auth_membership.insert(user_id=user, group_id=role, dependencia_asociada=dep)

  user = db(db.auth_user.email == 'jeflab@usb.ve').select()[0].id
  dep = db(db.dependencias.nombre == 'Laboratorio A').select()[0].id
  role = db(db.auth_group.role == 'Jefe de Laboratorio').select()[0].id

  db.auth_membership.insert(user_id=user, group_id=role, dependencia_asociada=dep)

  user = db(db.auth_user.email == 'coordinador@usb.ve').select()[0].id
  dep = db(db.dependencias.nombre == 'Unidad de Administración').select()[0].id
  role = db(db.auth_group.role == 'Coordinador').select()[0].id

  db.auth_membership.insert(user_id=user, group_id=role, dependencia_asociada=dep)

  user = db(db.auth_user.email == 'directassist@usb.ve').select()[0].id
  dep = db(db.dependencias.nombre == 'Dirección').select()[0].id
  role = db(db.auth_group.role == 'Asistente del Director').select()[0].id

  db.auth_membership.insert(user_id=user, group_id=role, dependencia_asociada=dep)

  user = db(db.auth_user.email == 'director@usb.ve').select()[0].id
  dep = db(db.dependencias.nombre == 'Dirección').select()[0].id
  role = db(db.auth_group.role == 'Director').select()[0].id

  db.auth_membership.insert(user_id=user, group_id=role, dependencia_asociada=dep)

  user = db(db.auth_user.email == 'webmaster@usb.ve').select()[0].id
  role = db(db.auth_group.role == 'WebMaster').select()[0].id

  db.auth_membership.insert(user_id=user, group_id=role)

