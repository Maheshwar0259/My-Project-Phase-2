from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

def send_alert(message):
    # Your Account SID and Auth Token from Twilio Console
    account_sid = 'AC6273763727e71a482db9a74493746173'
    auth_token = '73b9320939c7e3542724a6465dbf5424'

    client = Client(account_sid, auth_token)

    try:
        # Sending the SMS
        alert_message = client.messages.create(
            body=message,
            from_='+15394495759',  # Replace with your Twilio phone number
            to='+917702163563'     # Replace with your verified phone number
        )
        print(f"Alert sent successfully: {alert_message.sid}")
    except TwilioRestException as e:
        # Handle error in sending message
        print(f"Failed to send alert: {e}")