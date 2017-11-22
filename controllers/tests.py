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