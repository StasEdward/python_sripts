#!/usr/bin/python2.7

import fdb
import os.path
import time
import sys
import smtplib
import email.utils
import mysql.connector
from datetime import datetime, timedelta
from email.mime.text import MIMEText


try:
	cnx = mysql.connector.connect(user='root', password='edstas12', host='localhost', database='atestat')
except mysql.connector.Error as err:
  print("Something went wrong: {}".format(err))


time_now = datetime.now()
ten_min_ago = (datetime.now() - timedelta(minutes = 10))

print("Time now is: {} and 10 min ago is: {}".format(time_now, ten_min_ago))

stop_date = (time_now.strftime("%Y-%m-%d"))
start_date = (ten_min_ago.strftime("%Y-%m-%d"))

cur_local = cnx.cursor(buffered=True)
cur_local_update = cnx.cursor()

SELECT = "SELECT FACILITY, HOST, LAST_UPDATE, WAS_INFORMED FROM db_updater_status"
#print(SELECT)
cur_local.execute(SELECT)
for (facility, host, last_update, was_informed) in cur_local:
	uut_facility = facility
	uut_host = host
	uut_updated = last_update;
	email_was_sended = was_informed;
	#uut_last = datetime.strptime(uut_updated, "%Y-%m-%d %H:%M:%S.%f")
	update_delta = round((time_now - uut_updated).total_seconds()/60)
	print("Facility: {}  Host:{} Now:{:%H:%M} Last Update: {:%H:%M} Delta: {} mins".format(uut_facility, uut_host, time_now, uut_updated, update_delta))
	if (update_delta > 10):
		if (email_was_sended < 1):
			print("Sending emai about host '{}'...".format(uut_host))
			# Create the message
			text = "Hi,\nThis is the warning message from DB sync server.\n"
			text = text + "Time on server is {:%H:%M}, but host '{}' was updated last time at {:%H:%M} and this is {} min. and more than 10 min. ago".format(time_now, uut_host, uut_updated, update_delta)
			msg = MIMEText(text, 'plain')
			msg['To'] = email.utils.formataddr(('Recipient', 'edwards@ceragon.com'))
			msg['From'] = email.utils.formataddr(('DB server admin', 'admin@atestat.ceragon.com'))
			msg['Subject'] = 'DB sync warning message'

			server = smtplib.SMTP('10.10.10.184')
			server.set_debuglevel(False) # show communication with the server
			try:
				server.sendmail('edwards@ceragon.com', ['edwards@ceragon.com'], msg.as_string())
			finally:
				server.quit()
			UPDATE_TABLE = "UPDATE db_updater_status SET WAS_INFORMED=1 where HOST='{}'".format(uut_host)
			print("Update host '{}' status to 1".format(uut_host))
	else:
		UPDATE_TABLE = "UPDATE db_updater_status SET WAS_INFORMED=0 where HOST='{}'".format(uut_host)
		print("Update host '{}' status to 0".format(uut_host))


	print("Update host status")
	cur_local_update.execute(UPDATE_TABLE)
	cnx.commit()


		
cur_local.close()
cnx.close()