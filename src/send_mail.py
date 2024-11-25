try:
    from email.mime.text import MIMEText
    import smtplib
    from src import data_base
except Exception as e:
    print(f"Ocurrio un error al importat las librerias en send_mail, {e}")

def send_error_mail(message):
    try:
        server = smtplib.SMTP_SSL('mail.starflowers.com.ec', 465)
        server.login(data_base.get_user_mail(), data_base.get_password_mail())

        subject = "API WebScraping UNOSOF"
        body = f"Mensaje: {message}"

        para = "sistemas@starflowers.com.ec"

        msg = MIMEText(body)
        msg['Subject'] =  subject
        msg['From'] = data_base.get_user_mail()
        msg['To'] = para

        server.sendmail(data_base.get_user_mail(), para, msg.as_string())

        # data_base.log_to_db(1, "INFO", "correo enviado", endpoint='exitoso', status_code=200)
        server.quit()
    except Exception as e:
        message_error = f"Ocurrio un error con la funcion enviar correo, {e}"
        print(message_error)
        data_base.log_to_db(1, "INFO", message_error, endpoint='fallido', status_code=404)