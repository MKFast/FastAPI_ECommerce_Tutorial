from fastapi_mail import ConnectionConfig, MessageSchema, FastMail

config = ConnectionConfig(
    MAIL_USERNAME="mrkarami24251@gmail.com",
    MAIL_PASSWORD="moreka2425",
    MAIL_FROM= "mrkarami24251@gmail.com",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_TLS=True,
    MAIL_SSL=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)

class Mail(object):

    def __init__(self):
        pass

    async def send_notification(self, email:str, order_id:int, first_name:str):

        message= MessageSchema(
            subject='Order nr. {}'.format(order_id),
            recipients=[email],
            body='Dear {}, \n\n You have successfully placed an order.\n\n\
                 Your order id is {}.'.format(first_name,order_id)
        )

        fm= FastMail(config)
        await fm.send_message(message)

