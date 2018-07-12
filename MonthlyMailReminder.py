#TODO importar la funcion contar_notificaciones del controlador de personal
import datetime, time

def __enviar_correo(destinatario, asunto, cuerpo):
    mail = auth.settings.mailer
    mail.send(destinatario, asunto, cuerpo)

def contar_notificaciones(correo):
    usuario =db(db.t_Personal.f_email == correo).select(db.t_Personal.ALL)
    
    if(len(usuario)>1): usuario = usuario[1]
    else: usuario = usuario.first()
    es_supervisor = usuario.f_es_supervisor
    dependencia = None
    if es_supervisor:
        if(correo == "sigulabusb@gmail.com") or (correo == "asis-ulab@usb.ve"):
            notif = db(db.t_Personal.f_por_validar == True).count()
        else:
            dependencia = usuario.f_dependencia
            notif = db((db.t_Personal.f_dependencia == dependencia)&(db.t_Personal.f_es_supervisor == False)&(db.t_Personal.f_por_validar == True)).count()
    else:
        notif=0
    return notif

def get_correos_supervisores():
    supervisores = db(db.t_Personal.f_es_supervisor == True).select(db.t_Personal.f_email)
    emails = set()
    for entry in supervisores:
        emails.add(entry.f_email)
    
    return emails
    
    for mail in emails:
        
        pendientes = contar_notificaciones(mail)
        
        print("El usuario "+mail+" tiene "+str(pendientes)+"  fichas por validar")




asunto = '[SIGULAB] Recordatorio de fichas pendientes por validar'
while(1):
    now = datetime.datetime.now()
    if(now.day == 1):
        correos = get_correos_supervisores()
        for mail in correos:
        
            pendientes = contar_notificaciones(mail)
            cuerpo = ' Estimado usuario usted tiene {} fichas por validar bajo el modulo de gestion de personal del SIGULAB, para validarlas puede acceder\
                por el siguiente enlace:\n https://159.90.171.24/personal/listado_estilo '


            if(pendientes > 0 ):
                __enviar_correo(mail,asunto,cuerpo)
    else:
        #Duerme por un dia y chequea de nuevo
        time.sleep(86400)



