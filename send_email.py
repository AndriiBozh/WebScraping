import smtplib


def send_mail(message):
    mail = "andriibozhenko@gmail.com"
    send_to = 'deux_jours_avant@hotmail.com'
    passw = 'gsqp nfnr siwx jczv'
    # create SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)
    # start TLS for security
    s.starttls()
    try:
        # authentication
        s.login(mail, passw)
        s.sendmail(mail, send_to, message)
        s.quit()
        print('Email was sent.')
    except Exception as e:
        print('Error occurred! ', e)
