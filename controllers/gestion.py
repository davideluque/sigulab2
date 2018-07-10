#-----------------------------------------------------------------------------
#
# Controladores de las funcionalidades de Gestion
#
# - Erick Flejan <12-1155@usb.ve>
# - Amanda Camacho <12-10644@usb.ve>
# - David Cabeza <13-10191@usb.ve>
# - Fabiola Martínez <13-10838@usb.ve>
# - Lautaro Villalon <12-10427@usb.ve>
# - Yarima Luciani <13-10770@usb.ve>
#-----------------------------------------------------------------------------

@auth.requires_login(otherwise=URL('modulos', 'login'))
def usuarios():
    if(auth.has_membership('ADMINISTRADOR PERSONAL') or auth.has_membership('WEBMASTER')\
       or auth.has_membership('DIRECTOR') or (auth.user.email == "ulab-calidad@usb.ve")):
        table = SQLFORM.smartgrid(db.auth_user,onupdate=auth.archive,links_in_grid=False,csv=False,user_signature=True,paginate=10)
    else:
        table = SQLFORM.smartgrid(db.auth_user,editable=False,deletable=False,csv=False,links_in_grid=False,create=False,paginate=10)
    return locals()

@auth.requires_login(otherwise=URL('modulos', 'login'))
def dependencias():
    if(auth.has_membership('ADMINISTRADOR PERSONAL') or auth.has_membership('WEBMASTER')\
       or auth.has_membership('DIRECTOR') or (auth.user.email == "ulab-calidad@usb.ve")):
        table = SQLFORM.smartgrid(db.dependencias,onupdate=auth.archive,links_in_grid=False,csv=False,user_signature=True,paginate=10)
    else:
        table = SQLFORM.smartgrid(db.dependencias,editable=False,deletable=False,csv=False,links_in_grid=False,create=False,paginate=10)
    
    
    o = table.element(_type='submit', _value='%s' % T('Submit'))
    if o is not None:
        o['_value'] = T("Agregar")
        
    o = table.element(_type='submit', _value='%s' % T('Clear'))
    if o is not None:
        o['_value'] = T("Limpiar")
    
    o = table.element(_title='View')
    if o is not None:
        o['_innerHTML'] = T("Buscar")
    return locals()

@auth.requires_login(otherwise=URL('modulos', 'login'))
def espacios_fisicos():
    if(auth.has_membership('ADMINISTRADOR PERSONAL') or auth.has_membership('WEBMASTER')\
       or auth.has_membership('DIRECTOR') or (auth.user.email == "ulab-calidad@usb.ve")):
        table = SQLFORM.smartgrid(db.espacios_fisicos,onupdate=auth.archive,links_in_grid=False,csv=False,user_signature=True,paginate=10)
    else:
        table = SQLFORM.smartgrid(db.espacios_fisicos,editable=False,deletable=False,csv=False,links_in_grid=False,create=False,paginate=10)
    return locals()


@auth.requires_login(otherwise=URL('modulos', 'login'))

def bitacora_general():
    '''if(auth.has_membership('ADMINISTRADOR PERSONAL') or auth.has_membership('WEBMASTER')\
       or auth.has_membership('DIRECTOR') or (auth.user.email == "ulab-calidad@usb.ve")):
        table = SQLFORM.smartgrid(db.bitacora_general,onupdate=auth.archive, links_in_grid=False,editable=False,create=False,deletable=False,user_signature=True,paginate=10)
    else:
        table = SQLFORM.smartgrid(db.bitacora_general,editable=False,deletable=False,csv=False,links_in_grid=False,create=False,paginate=10)
    #print(db.bitacora_general.fields())
    '''
    entradas_query= db().select(db.bitacora_general.ALL)
    entradas = []

    for elm in entradas_query:
        responsable = db(db.auth_user.id == elm.created_by).select(db.auth_user.ALL).first()

        entradas.append({
            'id': elm.id,
            'accion': elm.f_accion,
            'fecha': elm.created_on,
            'responsable': responsable.first_name + " " + responsable.last_name
        })
        
    return locals()

