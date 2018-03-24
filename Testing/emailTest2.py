import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

fromaddr = "DUGreenhouseAlerts@gmail.com"
toaddr = "velacarl@my.dom.edu"
msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = toaddr
msg['Subject'] = "Test Alert"

body = "This is a test alert"
msg.attach(MIMEText(body, 'plain'))

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(fromaddr, "TeamGreen4")
text = msg.as_string()
server.sendmail(fromaddr, toaddr, text)
server.quit()
