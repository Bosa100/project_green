#program can work if the gmail security option for "less secure apps" is turned on
#the cronjob would look something like this:
# 0 0-21/3 * * * /usr/bin/python eAlerts.py
# 30 1-23/3 * * * /usr/bin/python eAlerts.py

import smtplib

content = 'testing'

mail = smtplib.SMTP('smtp.gmail.com', 587)

mail.ehlo()

mail.starttls()

mail.login('brian.rico94@gmail.com','rome2004')

mail.sendmail('brian.rico94@gmail.com', 'brian.rico94@gmail.com', content)

mail.close()
