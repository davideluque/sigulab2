# Manual de Instalación de SIGULAB

1. Descargar el contenido del [repositorio](https://github.com/davideluque/sigulab2) y colocar todo el contenido en una carpeta llamada `sigulab2`. También se puede clonar el contenido del repositorio mediante el uso de `git` y se obtendrá el mismo resultado. 


2. Descargar la última versión estable de `web2py` de la [página oficial](http://web2py.com/init/default/download). Descargar especificamente la opción llamada `Source Code` de la categoría `For Normal Users`. 


3. Una vez que se descargue el archivo comprimido con los archivos necesarios para ejecutar web2py, descomprimir su contenido. Obtendremos una nueva carpeta llamada `web2py`, que de ahora en adelante nos referiremos a ella como *el directorio raíz* o *~*. Esta carpeta puede ser renombrada si se desea.


4. Abrir el directorio raíz, y observaremos una carpeta llamada `applications`. Colocar la carpeta `sigulab2` que se obtuvo en el paso 2 dentro de esta carpeta `applications`.


5. Colocar el archivo `appconfig.ini` proporcionado por el encargado del repositorio en la siguiente ruta: `~/applications/sigulab2/private/`.


6. Instalar el paquete `python-psycopg2` que permite conectar a Python con el manejador de base de datos PostgreSQL, ejecutando el siguiente comando: 

`sudo apt-get install python-psycopg2`


7. Crear el rol `sigulab` en PostgreSQL utilizando el siguiente comando:

`sudo -u postgres createuser -PE -s sigulab`

**Nota**: al crear el rol, asignar como clave `sigulab`. Al crear el rol se pide la contraseña del rol 2 veces, y posterior a esto, se pide nuevamente una contraseña. Esta última contraseña requerida es la del usuario `postgres` en el sistema. Por defecto esta contraseña es `postgres`, a menos de que el usuario la haya modificado.


8. Crear la base de datos 'sigulab' en PostgreSQL utilizando el siguiente comando:

`sudo -u postgres createdb -O sigulab -E UTF8 sigulab2`

9. Una vez hecho todo esto, ir al directorio raíz y ejecutar web2py de la siguiente manera: 

`python web2py.py`

**Nota**: asegurarse de que se está ejecutando con Python 2.7. Al iniciar web2py, se le pedirá al usuario que ingrese una contraseña: colocar alguna contraseña sencilla. Esta contraseña le permitirá acceder a la interfaz administrativa posteriormente.


10. Para asegurarse de que todo está corriendo bien, ir a la siguiente ruta en el navegador:

`http://localhost:8000/sigulab2`

Si todo ha salido bien, verá la pantalla de login de SIGULAB.

___
