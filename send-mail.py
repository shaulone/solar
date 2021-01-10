#!/usr/bin/python3

import smtplib, ssl

port = 465  # For SSL
user = "hardufsolar@gmail.com"
password = "harduf1234"
receiver = "shaul.one@gmail.com"
message = """\
Subject: Hi there

This message is sent from Python."""

# Create a secure SSL context
context = ssl.create_default_context()

with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
    server.login(user, password)
    # TODO: Send email here
    # Authentication 
    #server.login("sender_email_id", "sender_email_id_password") 
  
    # sending the mail 
    server.sendmail(user, receiver, message) 
  
    # terminating the session 
    server.quit() 
