#!/usr/bin/env python
import pika
import smtplib


#gmail creds
gmail_user = 'yourgmail@gmail.com'  
gmail_password = 'change_your_password'
SUBJECT = "Jenkins Job STATUS"

#read mq
credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters('172.21.0.1', 5672, '/', credentials))
channel = connection.channel()
channel.queue_declare(queue='jenkins')
def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    TEXT = body
    message = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(gmail_user, gmail_password)
    server.sendmail(
    "yourgmail@gmail.com", 
    "grigorj@connectto.com", 
    message)
    server.quit()
      
channel.basic_consume(callback,
                      queue='jenkins',
                      no_ack=True)



print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
