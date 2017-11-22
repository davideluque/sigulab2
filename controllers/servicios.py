
#------------------------------------------------------------------------------
#
# Controladores de las funcionalidades del modulo de Servicios
#
#------------------------------------------------------------------------------

# Pagina principal del modulo
@auth.requires_login(otherwise=URL('modulos', 'login'))
def index():
	return dict()

def usuario():
    return dict(form=auth.profile(), form2=auth.change_password())