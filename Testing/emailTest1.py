import smtplib

content = "This is a test email."

mail = smtplib.SMTP('smtp.gmail.com', 587)

mail.ehlo()

mail.starttls()

mail.login('DUGreenhouseAlerts@gmail.com', 'TeamGreen4')

mail.sendmail('DUGreenhouseAlerts@gmail.com', 'velacarl@my.dom.edu', content)

mail.close()
