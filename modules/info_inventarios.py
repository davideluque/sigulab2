# encoding: utf-8
'''
Librería auxiliar con constantes largas para facilitar su manejo y reducir
el código repetido.
'''

CATEGORIAS_VEHICULOS = {
    '15010-0000 - Vehículos automotores terrestres': [
        '15010-0001 - Ambulancias',
        '15010-0002 - Autobuses',
        '15010-0003 - Automóviles',
        '15010-0004 - Camiones cisterna para asfalto',
        '15010-0005 - Camiones cisterna para agua',
        '15010-0006 - Camiones cisterna para gasolina',
        '15010-0007 - Camiones cisterna para gas',
        '15010-0008 - Camiones chasis',
        '15010-0009 - Camiones de estacas',
        '15010-0010 - Camiones volteos',
        '15010-0011 - Camiones ganaderos',
        '15010-0012 - Camiones grúas',
        '15010-0013 - Camiones para basura',
        '15010-0014 - Camionetas de carga cubiertas',
        '15010-0015 - Camionetas de carga pick-up',
        '15010-0016 - Camionetas de pasajeros',
        '15010-0017 - Camionetas (ómnibus rurales)',
        '15010-0019 - Carros bombas para incendios',
        '15010-0020 - Carros de bomberos',
        '15010-0021 - Chutos',
        '15010-0022 - Escaleras automóviles para bomberos',
        '15010-0023 - Furgones',
        '15010-0024 - Gandolas',
        '15010-0025 - Microbúses',
        '15010-0026 - Motocicletas',
        '15010-0027 - Motocicletas de reparto',
        '15010-0028 - Motonetas',
        '15010-0029 - Motonetas de reparto',
        '15010-0030 - Radiopatrullas',
        '15010-0031 - Transportadores de vehículos',
    ],
    '15020-0000 - Equipos ferroviarios y carros aéreos': [
        '15020-0001 - Autovías',
        '15020-0002 - Grúas ferroviarias automotores',
        '15020-0003 - Locomotoras a vapor',
        '15020-0004 - Locomotoras diésel',
        '15020-0005 - Locomotoras eléctricas',
        '15020-0006 - Tranvías',
        '15020-0007 - Trolle (trolley)',
        '15020-0008 - Vagones de mercancías cubiertos',
        '15020-0009 - Vagones de carga para cables aéreos',
        '15020-0010 - Vagones de mercancías bordes altos',
        '15020-0011 - Vagones de mercancías bordes bajos',
        '15020-0012 - Vagones de pasajeros',
        '15020-0013 - Vagones de pasajeros de cables aéreos',
        '15020-0014 - Vagones de tracción propia',
        '15020-0015 - Vagones grúa',
        '15020-0016 - Vagones plataforma',
        '15020-0017 - Vagones refrigerantes',
        '15020-0018 - Vagones tanque',
        '15020-0019 - Vagones tolva',
        '15020-0020 - Vagones volquete',
        '15020-0021 - Vagonetas',
    ],
    '15030-0000 - Equipos marítimos de transporte': [
        '15030-0001 - Balandras',
        '15030-0002 - Barcos cargueros',
        '15030-0003 - Barcos de guerra (reservado ministerio de la defensa)',
        '15030-0004 - Barcos de río',
        '15030-0005 - Barcos de salvamento y de rescate',
        '15030-0006 - Barcos extintores de incendio',
        '15030-0007 - Barcos furgoneros',
        '15030-0008 - Barcos mixtos de carga y de pasajeros',
        '15030-0009 - Barcos pesqueros',
        '15030-0010 - Barcos refrigerantes',
        '15030-0011 - Barcos taller',
        '15030-0012 - Barcos tanqueros',
        '15030-0013 - Botes',
        '15030-0014 - Buques-faro',
        '15030-0015 - Gabarras',
        '15030-0016 - Lanchas',
        '15030-0017 - Remolcadores',
        '15030-0018 - Veleros',
        '15030-0019 - Yates',
    ],
    '15040-0000 - Equipos aéreos de transporte': [
        '15040-0001 - Aviones de carga',
        '15040-0002 - Aviones de pasajeros',
        '15040-0003 - Avionetas',
        '15040-0004 - Dirigibles',
        '15040-0005 - Helicópteros',
        '15040-0006 - Planeadores'
    ],
    '15050-0000 - Vehículos de tracción no motorizados': [
        '15050-0001 - Bicicletas',
        '15050-0002 - Coches de tracción animal',
        '15050-0003 - Triciclos',
        '15050-0004 - Remolques',
        '15050-0005 - Zorras'
    ],
    '15060-0000 - Equipos auxiliares de transporte': [
        '15060-0001 - Boyas',
        '15060-0002 - Camiones especiales para aeropuertos',
        '15060-0003 - Encerados para camión',
        '15060-0004 - Escafandras',
        '15060-0005 - Escalerillas para aviones',
        '15060-0006 - Gabarras',
        '15060-0007 - Grúas flotantes',
        '15060-0008 - Grúas móviles',
        '15060-0009 - Montacargas automotores',
        '15060-0010 - Motores fuera de borda',
        '15060-0011 - Motores marinos',
        '15060-0012 - Remolcadores (chocones)',
        '15060-0013 - Remolques',
        '15060-0014 - Remolques especiales para aeropuertos',
        '15060-0015 - Señales de tránsito',
        '15060-0016 - Transportadores de vehículos',
        '15060-0017 - Vagonetas',
        '15060-0018 - Zorras'
    ],
    '15990-0000 - Otros equipos de transporte, traccion y elevacion': [
        '15990-0001 - Otros equipos de transporte, traccion y elevacion'
    ]
}

CLASIFICACIONES_VEHICULOS = {
    'Motocicleta': [
        'Comercial',
        'Oficial',
        'Deportiva',
        'Policial',
        'Paseo'
    ],
    'Automóvil': [
        'De pasajeros sin fines de lucro',
        'De pasajeros con fines de lucro de alquiler',
        'De pasajeros con fines de lucro por puesto'
    ],
    'Minibús': [
        'Sin fines de lucro',
        'Con fines de lucro'
    ],
    'Autobús': [
        'Uso público',
        'Uso privado'
    ],
    'Vehículos de carga': [
        'General, a granel, perecedera y frágil',
        'De alto riesgo'
    ],
    'Vehículos especiales': [
        'Enseñanza',
        'Emergencia',
        'Escolares',
        'Diplomático'
    ]
}