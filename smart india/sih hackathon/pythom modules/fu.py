import smtplib
import random

def sendmail(subject,body,sendto):
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login('ayushalas0520@gmail.com','isnpgolplrzoiubg')
    msg = f"Subject:{subject}\n\n{body}"
    server.sendmail(
        'ayushalas0520@gmail.com',
        sendto,
        msg
    )
    print('email sent')
    server.quit()
sendmail('congo','otp, thanks','brijeshsoni371@gmail.com')
def createid():
    n = ''
    x=0
    while x<7:
        y = random.randint(1,9)
        if str(y) not in n:
            n+=str(y)
            x+=1
    return int(n)
    
