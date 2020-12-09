import os
from twilio.rest import Client
from twilio.twiml.messaging_response import Body, Message, Redirect, MessagingResponse

def whatsapp_message(phone_number):
    account_sid = "AC878d116006cb602ba21786e4f53b7392"
    auth_token = "07a5aaae3bf120fa912633e72d3fa0d7"
    client = Client(account_sid, auth_token)

    from_whatsapp_number = "whatsapp:+14155238886"
    to_whatsapp_number = f"whatsapp:+1{phone_number}"

    response = MessagingResponse()
    message = Message()
    mes = "Hello, someone you have been in contact with may have Covid-19. Please self isolate and if you display any symptoms, message 'test' to this number"


    client.messages.create(body=mes,
                            from_ = from_whatsapp_number,
                            to = to_whatsapp_number)
