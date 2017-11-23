#!/usr/bin/ python
# encoding=utf8  
#import sys  
  
#sys.setdefaultencoding('utf8')

#-------------------------------------
#
# Controladores integrados/en conjunto
#
#-------------------------------------

# Pagina, botones de eleccion entre nuestros modulos
# o SMDP

@auth.requires_login(otherwise=URL('modulos', 'login'))
def index():
    return dict()

@auth.requires_login(otherwise=URL('modulos', 'login'))
def sigulab2():
    return dict()

#-------------------------------------
# Autenticacion y manejo de cuenta
#-------------------------------------

# Inicio de Sesion
def login():
    if auth.user:
        return redirect(URL('index'))
    form=auth.login()
    return dict(form=form)

# Perfil de Usuario
@auth.requires_login(otherwise=URL('modulos', 'login'))
def editprofile():
    return dict(form=auth.profile(), form2=auth.change_password())

# Registro de usuarios-
def register():
    if auth.user:
        return redirect(URL('index'))
    form=auth.register()
    return dict(form=form)

# Recuperacion de Contraseña (pedido) 
def resetpassword():
    site_url = URL(request.application, 'modulos', 'recoverpassword', host=True)
    # pagina indicada en el email
    auth.messages.reset_password = 'Por favor clickee el siguiente link ' + site_url + '/?key=' + '%(key)s para resetear su contraseña'
    form = auth.request_reset_password()
    return dict(form=form)

# Recuperacion de Contraseña (reinicio) 
def recoverpassword():
    return dict(form=auth.reset_password())

def logout():
    auth.logout()
    return redirect(URL('login'))
