import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from threading import Thread


MAIL_TEMPLATE = {
    'register': {
        'from': 'Mr.Lean <{sender}>',
        'subject': 'Mr.Lean says a hello to you!',
        'html': '<p>Welcome to Lean\'s blog!</p>'
    }
}

class Mail(object):
    def __init__(self, app=None):
        self.host = None
        self.port = None
        self.user = None
        self.password = None
        self.sender = None
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        self.host=app.config['MAIL_HOSTNAME']
        self.port=app.config['MAIL_PORT']
        self.user=app.config['MAIL_USERNAME']
        self.password=app.config['MAIL_PASSWORD']
        self.sender = app.config['MAIL_SENDER']

    def __get_connection(self):
        smtp = smtplib.SMTP(
            host=self.host,
            port=self.port
        )
        smtp.set_debuglevel(1)
        smtp.login(
            user=self.user,
            password=self.password
        )
        return smtp

    def send_mail(self, recipient, type_='register'):
        template = MAIL_TEMPLATE[type_]
        msg = MIMEMultipart('alternative')
        msg['From'] = self.sender
        msg['To'] = recipient
        msg['Subject'] = template['subject']
        msg.attach(
            MIMEText(
                _text=template['html'], 
                _subtype='html',
                _charset='utf-8'
            ))
        t = Thread(target=self.__send_async_email, args=(msg, ))
        t.start()
        return True
    
    def __send_async_email(self, msg):
        smtp = self.__get_connection()
        smtp.send_message(msg)
        smtp.quit()
