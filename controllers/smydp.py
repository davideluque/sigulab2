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
def inventarios():
	return locals()


@auth.requires_login(otherwise=URL('modulos', 'login'))
def desechos():
	return locals()


#-------------------------------------- Catalogo ---------------------------------------
"""
@auth.requires_login(otherwise=URL('modulos', 'login'))
def catalogo():

    if not 'view' in request.args:
        db.t_sustancias.f_peligrosidad.represent = lambda v,r: v[0] if v else "Ninguna"

    if 'edit' in request.args or 'new' in request.args:
        mark_not_empty(db.t_sustancias)

    if(auth.has_membership('Gestor de SMyDP') or \
    auth.has_membership('WebMaster')):
        table = SQLFORM.smartgrid(db.t_sustancias,onupdate=auth.archive,links_in_grid=False,csv=False,user_signature=True,paginate=10)
    else:
        table = SQLFORM.smartgrid(db.t_sustancias,editable=False,deletable=False,csv=False,links_in_grid=False,create=False,paginate=10)
    return locals()
"""