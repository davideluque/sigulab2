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

@auth.requires_login(otherwise=URL('modulos', 'login'))
def catalogo():
    columnas = [db.t_Sustancia.f_nombre, 
                db.t_Sustancia.f_cas, 
                db.t_Sustancia.f_pureza, 
                db.t_Sustancia.f_estado, 
                db.t_Sustancia.f_control, 
                db.t_Sustancia.f_peligrosidad, 
                db.t_Sustancia.f_hds ]
    if(auth.has_membership('Gestor de SMyDP') or  auth.has_membership('WEBMASTER')):
        table = SQLFORM.smartgrid(  
                                    db.t_Sustancia,   
                                    fields=columnas,
                                    onupdate=auth.archive,
                                    links_in_grid=False,
                                    csv=False,
                                    user_signature=True,
                                    paginate=10)
    else:
        table = SQLFORM.smartgrid(
                                    db.t_Sustancia, 
                                    fields=columnas,
                                    editable=False,
                                    deletable=False,
                                    csv=False,
                                    links_in_grid=False,
                                    create=False,
                                    paginate=10,
                                    showid=False)
    return locals()

