def send_message(iscomplete, subject, body):

    import smtplib
    from email.mime.text import MIMEText

    if iscomplete == True:

        # Set up the message to be sent
        html2 = '''\
            <html>
            <head></head>
            <body>
            <p>**** THIS IS AN AUTOMATED MESSAGE ****<br>
            </p>
            '''

        html3 = '''\
            </body>
            </html>
            '''

        html = html2 + body + '<br>' + html3
        msg = MIMEText(html, 'html')
        msg['Subject'] = subject

        sender = 'sbwilliams@bpu.com'
        recipients = ["TableauDev@bpu.com"]
        msg['From'] = sender
        msg['To'] = ", ".join(recipients)
        #msg['reply-to'] = 'pbrown@bpu.com'
        server = smtplib.SMTP('smtp.corp.bpu.local')
        server.sendmail(sender, recipients, msg.as_string())
        server.close()

        return True

    else:

        # Set up the message to be sent
        html2 = '''\
            <html>
            <head></head>
            <body>
            <p>**** THIS IS AN AUTOMATED MESSAGE ****<br>
            </p>
            '''

        html3 = '''\
            </body>
            </html>
            '''

        html = html2 + body + '<br>' + html3
        msg = MIMEText(html, 'html')
        msg['Subject'] = subject

        sender = 'sbwilliams@bpu.com'
        recipients = ["TableauDev@bpu.com"]
        msg['From'] = sender
        msg['To'] = ", ".join(recipients)
        #msg['reply-to'] = 'pbrown@bpu.com'
        server = smtplib.SMTP('smtp.corp.bpu.local')
        server.sendmail(sender, recipients, msg.as_string())
        server.close()

        return False

