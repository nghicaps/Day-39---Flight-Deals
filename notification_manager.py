from twilio.rest import Client

ACCOUNT_SID = "<ACCOUNT SID>"
AUTH_TOKEN = "<AUTH_TOKEN>"


class NotificationManager:
    def __init__(self):
        self.client = Client(ACCOUNT_SID, AUTH_TOKEN)

    def send_text(self, notif_message):
        message = self.client.messages.create(
            body=notif_message,
            from_="<number1>",
            to="<number2>",
        )
