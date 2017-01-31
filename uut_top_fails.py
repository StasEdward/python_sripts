#!/usr/bin/python2.7
import fdb
import os.path
import time
import mysql.connector

print "******************************************************************************************************"
print "* This scriptp receive TOP UUT FAIL data from all servers and put to local data base for fast access *"
print "******************************************************************************************************"

now = time.strftime("%c")
## date and time representation
print "Script started at: " + time.strftime("%c")

try:
	cnx = mysql.connector.connect(user='root', password='edstas12', host='localhost', database='atestat')
except mysql.connector.Error as err:
  print("Something went wrong: {}".format(err))

  print("Something went wrong: {}".format(err))

uut_name = ''
uut_fail = 0
uut_facility = ''
count = 0
#cur_local_ins = cnx2.cursor()		
cur_local = cnx.cursor(buffered=True)
SELECT = "SELECT UUTNAME as name, COUNT(GLOBALRESULT) as fails, FACILITY AS facility FROM (SELECT * from PHOSTESTGLOBALTEST where GLOBALRESULT='Fail' AND TESTDATE >= NOW() - INTERVAL 1 DAY AND GLOBALRESULT='Fail' order by UUTNAME ASC, SERIALNUMBER ASC) as table_result GROUP BY UUTNAME ORDER by fails DESC"
#print(SELECT)
cur_local.execute(SELECT)

rows = cur_local.fetchall()
count = cur_local.rowcount
print(count)

if (rows > 0):
	DELETE = "TRUNCATE atestat.UUT_TOP_FAILS"
	cur_local.execute(DELETE)
	cnx.commit()
	print("Delete old records")

for (name, fails, facility) in rows:
	uut_name = name
	uut_fail = fails
	uut_facility = facility
	DB_INSERT = 'INSERT INTO atestat.UUT_TOP_FAILS (id, UUT_NAME, UUT_FAILS, FACILITY ) VALUES (null, "%s", %d, "%s")' % (uut_name, uut_fail, uut_facility)
	print(DB_INSERT)
	cur_local_ins = cnx.cursor()
	cur_local_ins.execute(DB_INSERT)
	#cnx2.commit()
#	print 'Flex2 field updated'



cur_local.close()
cur_local_ins.close()

cnx.close()

now = time.strftime("%c")
## date and time representation

print "Script ended at: " + time.strftime("%c")
print "*****************************************************************************************"
