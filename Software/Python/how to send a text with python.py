#!/usr/bin/python
from twilio.rest import Client

account_sid="account sid" #you get this from your twilio account
auth_tokken="auth tokken"#you also get this

client = Client(account_sid, auth_tokken)

text = input("")

message = client.api.account.messages.create(
        to="+1773",
        from_="+17738325163",
        body=text)
