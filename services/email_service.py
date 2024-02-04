from django.core.mail import EmailMessage
from django.conf import settings


class EmailServiceMeta(type):

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class EmailService(metaclass=EmailServiceMeta):

    def __init__(self):
        self.from_email = settings.EMAIL_HOST_USER

    def send(self, subject: str, html_message: str, recipient_list: list):
        email = EmailMessage(subject, html_message,
                             self.from_email, recipient_list)
        email.content_subtype = 'html'
        return email.send()

    def send_activation_email(self, user, token):
        subject = 'Activate your account'
        message = f'''
            <head>
            <style>
            *{{font-family: "Poppins", sans-serif !important;}}
            a.link{{color: #fff; text-decoration: none !important;padding: 10px 20px;background-color: #FCB216;border-radius: 5px;}}
            </style>
            </head>
            <body>
            <h1>{settings.APP_NAME}</h1>
            <h3>Hi!</h3>
            <p>
              We are excited to have you on board. Click the link below to activate your account.
            </p>
            <br>
            <a class='link' href='http://{settings.APP_HOST}/user/activate/{token}/'> Activate Account </a>
            <br><br>
            <p>
            Kind Regards,<br>
            {settings.APP_NAME} Team
            </p>
            </body>'''
        recipient_list = [user.email]
        return self.send(subject, message, recipient_list)
