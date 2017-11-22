from servicios_libreria import *

# ----------------------------------------------------------------------------------------
# Controlador que no sera implementado en la aplicacion final, pueden hacerse pruebas aca
# ----------------------------------------------------------------------------------------

# Prueba en mini tabla de personas
def display_form():
   form = SQLFORM(db.person)
   if form.process().accepted:
       response.flash = 'form accepted'
   elif form.errors:
       response.flash = 'form has errors'
   else:
       response.flash = 'please fill out the form'
   return dict(form=form)


def prueba_lista_servicios():
	lista = ListaServicios(db)
	print
	lista.invertir_ordenamiento()
	lista.cambiar_columna('sede')
	lista.orden_y_filtrado()
	for i in lista.servicios_a_mostrar:
		print i.sede

	return dict()
