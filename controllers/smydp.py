#-----------------------------------------------------------------------------
# Controladores provisionales utilizados solo para probar las vistas del modulo de SMyDP
#
# - Samuel Arleo <saar1312@gmail.com>
#-----------------------------------------------------------------------------


@auth.requires_login(otherwise=URL('modulos', 'login'))
def index():
	return locals()


@auth.requires_login(otherwise=URL('modulos', 'login'))
def sustancias():
	return locals()


@auth.requires_login(otherwise=URL('modulos', 'login'))
def listado():
	return locals()


@auth.requires_login(otherwise=URL('modulos', 'login'))
def inventarios():
	return locals()


@auth.requires_login(otherwise=URL('modulos', 'login'))
def desechos():
	return locals()