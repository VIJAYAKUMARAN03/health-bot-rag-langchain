from twilio.rest import Client

# Your Twilio Account SID, Authentication Token, and Twilio Phone Number
account_sid = '' #Your Twilio Account SID
auth_token = ''  #Your Twilio Authentication Token
twilio_phone_number = '' #Your Twilio Phone Number

# Recipient's phone number
to_phone_number = ''  # Include the number with country code (ex: +919999999999)


# Initialize Twilio client
client = Client(account_sid, auth_token)

# Send the message

def sendSMS(data):
    message = client.messages.create(
        body=data,
        from_=twilio_phone_number,
        to=to_phone_number
    )
    print("Message sent successfully!")
    print("Message SID:", message.sid)


