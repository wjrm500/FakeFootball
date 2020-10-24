import smtplib
from email.message import EmailMessage

def script_finish(script_name, time_taken):
    sender = 'wjrm500@gmail.com'
    receiver = 'wjrm500@gmail.com'
    password = 'fatscumbags123'
    message = EmailMessage()
    minutes, seconds = divmod(time_taken, 60)
    message.set_content('Your Python script \'{}\' completed in {} minutes and {} seconds!'.format(script_name, minutes, seconds))
    message['Subject'] = 'Python script completed'
    message['From'] = sender
    message['To'] = receiver

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender, password)
    server.send_message(message)
