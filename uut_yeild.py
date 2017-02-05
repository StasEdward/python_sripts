#!/usr/bin/python2.7
import fdb
import os.path
import time
import mysql.connector
from datetime import datetime, timedelta
import time
import sys

print "*****************************************************************************************"
print "* This script receive YEILD data from all servers and put to local data base for fast access *"
print "*****************************************************************************************"

print 'Number of arguments:', len(sys.argv), 'arguments.'
print 'Argument List:', str(sys.argv)

if len(sys.argv) > 1:
	UUT_TYPE = sys.argv[1]
	if (len(sys.argv) > 2):
		MINIMUM_UUTS = int(sys.argv[2])
	else:
		MINIMUM_UUTS = 500
else:
#	print("Without parameters.Using default UUT as IDU")
	UUT_TYPE = "IDU"
	MINIMUM_UUTS = 500

print("Using UUT as {} and get {} records".format(UUT_TYPE, MINIMUM_UUTS))


now = time.strftime("%c")
## date and time representation
print "Script started at: " + time.strftime("%c")

try:
	cnx = mysql.connector.connect(user='root', password='edstas12', host='localhost', database='atestat')
except mysql.connector.Error as err:
  print("Something went wrong: {}".format(err))


uut_name = ''
uut_fail = 0
uut_pass = 0
uut_totall = 0
uut_yeild = 0
count = 0



from datetime import datetime, timedelta
d = datetime.now()
#d = datetime(2012, 3, 31) # A problem date as an example

# last day of last month
one_month_ago = (d.replace(day=1) - timedelta(days=1))
try:
    # try to go back to same day last month
    one_month_ago = one_month_ago.replace(day=d.day)
except ValueError:
    pass
print("Select all from Today: {0} until one month ago: {0}".format(d, one_month_ago))

stop_date = (d.strftime("%Y-%m-%d"))
start_date = (one_month_ago.strftime("%Y-%m-%d"))
#start_time = (d.strftime("%H:%M"))
#stop_time  = (one_month_ago.strftime("%H:%M"))

#print(start_time)
#print(stop_time)

#start_date = '2017-01-20';
#stop_date  = '2017-01-30';
#start_time = '09:48';
#stop_time  = '19:48';
 
#cur_local_ins = cnx2.cursor()		
cur_local = cnx.cursor(buffered=True)
cur_local_ins = cnx.cursor()

TOTAL_NEW_RECORDS = 0
		
SELECT = "SELECT distinct UUT_NAME FROM UUT_IDU_ODU_LIST WHERE UUT_TYPE='{}'" .format(UUT_TYPE)
#print(SELECT)
cur_local.execute(SELECT)
rows = cur_local.fetchall()
count = cur_local.rowcount
#print(count)

if (rows > 0):
	DELETE = "TRUNCATE atestat.UUT_{}_YELD_MONTH_TMP".format(UUT_TYPE)
	cur_local.execute(DELETE)
	cnx.commit()
	print("Delete old records from table UUT_{}_YELD_MONTH_TMP".format(UUT_TYPE))
#quit()

print("Prepare new data...")

for (UUTNAME) in rows:
	uut_name = UUTNAME[0].encode("latin-1")
	#print(UUTNAME)
	#uut_fail = fails
	SELECT_TOTAL = 'SELECT COUNT(distinct SERIALNUMBER) as totall FROM PHOSTESTGLOBALTEST WHERE UUTNAME ="{}" AND TESTDATE BETWEEN "{}" AND "{}"' .format(uut_name, start_date, stop_date)
#	SELECT_TOTAL = 'SELECT COUNT(distinct SERIALNUMBER) as totall FROM PHOSTESTGLOBALTEST WHERE UUTNAME ="{}" AND TESTDATE BETWEEN "{}" AND "{}" AND TIMESTART BETWEEN "{}" AND "{}"' .format(uut_name, start_date, stop_date, start_time, stop_time)
	#print(SELECT_TOTAL)
	cur_total = cnx.cursor()
	cur_total.execute(SELECT_TOTAL)
	totall_uut = cur_total.fetchone()
	totall_uuts = totall_uut[0]
	#print(totall_uut)
	
	if (totall_uuts > 0):
		SELECT_PASS = 'SELECT COUNT(distinct SERIALNUMBER) as passed FROM PHOSTESTGLOBALTEST WHERE UUTNAME ="{}" AND (GLOBALRESULT="Pass" or GLOBALRESULT="Pass*") AND TESTDATE BETWEEN "{}" AND "{}"' .format(uut_name, start_date, stop_date)
#	SELECT_PASS = 'SELECT COUNT(distinct SERIALNUMBER) as passed FROM PHOSTESTGLOBALTEST WHERE UUTNAME ="{}" AND (GLOBALRESULT="Pass" or GLOBALRESULT="Pass*") AND TESTDATE BETWEEN "{}" AND "{}" AND TIMESTART BETWEEN "{}" AND "{}"' .format(uut_name, start_date, stop_date, start_time, stop_time)
#	print(SELECT_PASS)
		cur_pass = cnx.cursor()
		cur_pass.execute(SELECT_PASS)
		pass_uut = cur_pass.fetchone()
		#print(pass_uut)
		uut_pass = pass_uut[0]
		uut_tested_totall = totall_uuts
		uut_fail = uut_tested_totall - uut_pass
		#YIELD = PASS / (FAIL+PASS) * 100;
		if uut_tested_totall > MINIMUM_UUTS:
			uut_yeild = (float(uut_pass) / float(uut_tested_totall)) *100;
			#print(uut_yeild);
			DB_INSERT = 'INSERT INTO atestat.UUT_{}_YELD_MONTH_TMP (id, UUT_NAME, TOTAL_UUT, TOTAL_PASS, TOTAL_FAIL, YEILD ) VALUES (null, "{}", {}, {}, {}, {})' .format(UUT_TYPE, uut_name, uut_tested_totall, uut_pass, uut_fail, uut_yeild)
			#print(DB_INSERT)
			cur_local_ins.execute(DB_INSERT)
			cnx.commit() 
			TOTAL_NEW_RECORDS = TOTAL_NEW_RECORDS + 1
			print("UUT: {}: YIELD={:.1%}  Total: {}, Pass: {}, Fails:{}" .format(uut_name, uut_yeild/100, uut_tested_totall, uut_pass, uut_fail))
		else:
			print("Records was not added for UUT '{}' because record count {} less than {}".format(uut_name, uut_tested_totall, MINIMUM_UUTS))
	else:
		print("UUT '{}' was skipped because total record count=0".format(uut_name))
	
	#cnx2.commit()
	#print 'Flex2 field updated'



if (TOTAL_NEW_RECORDS > 0):
	print("Clear origin table")
	DELETE = "TRUNCATE atestat.UUT_{}_YELD_MONTH".format(UUT_TYPE)
	cur_local.execute(DELETE)
	cnx.commit()
	print("Copy data from TMP to origin table")
	COPY_TABLE = "INSERT INTO atestat.UUT_{}_YELD_MONTH SELECT * FROM atestat.UUT_{}_YELD_MONTH_TMP".format(UUT_TYPE, UUT_TYPE)
	cur_local.execute(COPY_TABLE)
	cnx.commit()



cur_local.close()
cur_local_ins.close()
cur_total.close()
cur_pass.close()

cnx.close()

now = time.strftime("%c")
## date and time representation

print "Script ended at: " + time.strftime("%c")
print "*****************************************************************************************"
