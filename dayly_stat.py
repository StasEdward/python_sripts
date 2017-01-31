#!/usr/bin/python2.7

import fdb
import os.path
import time
import mysql.connector

print "*****************************************************************************************"
print "* This scriptp receive data from all servers and put to local data base for fast access *"
print "*****************************************************************************************"

now = time.strftime("%c")
## date and time representation
print "Script started at: " + time.strftime("%c")

try:
	cnx = mysql.connector.connect(user='root', password='edstas12', host='localhost', database='atestat')
except mysql.connector.Error as err:
  print("Something went wrong: {}".format(err))


try:
        con_ceragon = fdb.connect(host='10.10.14.61', database='d:\\home\\administrator\\local_dbs\\ATEGLOBAL', user='SYSDBA', password='masterkey')
        ceragon_connected = True
except fdb.Error, e:
        print "Error in connection to Ceragon DB"
        ceragon_connected = False
try:
        con_flex1 = fdb.connect(host='flex1', database='D:\\pub\\atemaindb\\ATEGLOBAL', user='SYSDBA', password='masterkey')
        flex1_connected = True
except fdb.Error, e:
        print "Error in connection to Flex1 DB"
        flex1_connected = False
try:
        con_flex2 = fdb.connect(host='flex2', database='D:\\pub\\atemaindb\\ATEGLOBAL', user='SYSDBA', password='masterkey')
        flex2_connected = True
except fdb.Error, e:
        print "Error in connection to Flex2 DB"
        flex2_connected = False
try:
        con_vcl = fdb.connect(host='192.168.12.101', database='C:\\PUB\\ATEMAINDB\\ATEGLOBAL.FDB', user='SYSDBA', password='masterkey')
        vcl_connected = True
except fdb.Error, e:
        print "Error in connection to VCL DB"
        vcl_connected = False
try:
        con_ionics1 = fdb.connect(host='192.168.6.7', database='D:\\pub\\atemaindb\\ATEGLOBAL', user='SYSDBA', password='masterkey')
        ionics1_connected = True
except fdb.Error, e:
        print "Error in connection to Ionics1 DB"
        ionics1_connected = False
try:
        con_ionics2 = fdb.connect(host='192.168.6.9', database='D:\\pub\\atemaindb\\ATEGLOBAL', user='SYSDBA', password='masterkey')
        ionics2_connected = True
except fdb.Error, e:
        print "ERROR in connection to Ionics2 DB"
        ionics2_connected = False

try:
        con_jbl1 = fdb.connect(host='192.168.13.101', database='D:\\ate\\firebird_dbs\\ATEGLOBAL', user='SYSDBA', password='masterkey')
        jbl1_connected = True
except fdb.Error, e:
        print "ERROR in connection to JBL12 DB"
        jbl1_connected = False


ceragon_pass = 0
ceragon_fail = 0
flex1_pass = 0
flex1_fail = 0
flex2_pass = 0
flex2_fail = 0
ionics1_pass = 0
ionics1_fail = 0
ionics2_pass = 0
ionics2_fail = 0
vcl_pass = 0
vcl_fail = 0
jbl_pass = 0
jbl_fail = 0


# Retrieving an integer info item is quite simple.
#bytesInUse = con_vcl.database_info(fdb.isc_info_current_memory, 'i')


#print 'The server is currently using %d bytes of memory.' % bytesInUse
#buf = con_vcl.database_info(fdb.isc_info_db_id, 's')
# Parse the filename from the buffer.
#beginningOfFilename = 2
# The second byte in the buffer contains the size of the database filename
# in bytes.
#lengthOfFilename = fdb.ibase.ord2(buf[1])
#filename = buf[beginningOfFilename:beginningOfFilename + lengthOfFilename]

# Parse the host name from the buffer.
#beginningOfHostName = (beginningOfFilename + lengthOfFilename) + 1
# The first byte after the end of the database filename contains the size
# of the host name in bytes.
#lengthOfHostName = fdb.ibase.ord2(buf[beginningOfHostName - 1])
#host = buf[beginningOfHostName:beginningOfHostName + lengthOfHostName]

# get results for local Ceragon
if ceragon_connected:
        cur = con_ceragon.cursor()
        SELECT = "SELECT count(*) as passresult from (select distinct serialnumber FROM phostestglobaltest WHERE testdate >= dateadd (-1 day to current_date) AND GLOBALRESULT like 'Pass%')"
        cur.execute(SELECT)
        for (passresult) in cur:
                ceragon_pass = passresult[0]
        SELECT = "SELECT count(*) as failresult from (select distinct serialnumber FROM phostestglobaltest WHERE testdate >= dateadd (-1 day to current_date) AND GLOBALRESULT='Fail')"
        cur.execute(SELECT)
        for (failresult) in cur:
                ceragon_fail = failresult[0]     
        print 'Ceragon:\t%d Pass, %d Fail' % (ceragon_pass,ceragon_fail)
	con_ceragon.close()
else:
        print 'Ceragon DB skipped'

# get results for Ionics 1
if ionics1_connected:
        cur = con_ionics1.cursor()
        SELECT = "SELECT count(*) as passresult from (select distinct serialnumber FROM phostestglobaltest WHERE testdate >= dateadd (-1 day to \
current_date) AND GLOBALRESULT like 'Pass%')"
        cur.execute(SELECT)
        for (passresult) in cur:
                ionics1_pass = passresult[0]
        SELECT = "SELECT count(*) as failresult from (select distinct serialnumber FROM phostestglobaltest WHERE testdate >= dateadd (-1 day to \
current_date) AND GLOBALRESULT='Fail')"
        cur.execute(SELECT)
        for (failresult) in cur:
                ionics1_fail = failresult[0]
        print 'Ionics1:\t%d Pass, %d Fail' % (ionics1_pass,ionics1_fail)
        con_ionics1.close()
else:
        print 'Ionics1 DB skipped'

if ionics2_connected:
# get results for Ionics 2
        cur = con_ionics2.cursor()
        SELECT = "SELECT count(*) as passresult from (select distinct serialnumber FROM phostestglobaltest WHERE testdate >= dateadd (-1 day to \
current_date) AND GLOBALRESULT like 'Pass%')"
        cur.execute(SELECT)
        for (passresult) in cur:
                ionics2_pass = passresult[0]
        SELECT = "SELECT count(*) as failresult from (select distinct serialnumber FROM phostestglobaltest WHERE testdate >= dateadd (-1 day to \
current_date) AND GLOBALRESULT='Fail')"
        cur.execute(SELECT)
        for (failresult) in cur:
                ionics2_fail = failresult[0]
        print 'Ionics2:\t%d Pass, %d Fail' % (ionics2_pass,ionics2_fail)
        con_ionics2.close()
else:
        print 'Ionics2 DB skipped'

        
# get results for Flex 1
if ionics2_connected:
        cur = con_flex1.cursor()
        SELECT = "SELECT count(*) as passresult from (select distinct serialnumber FROM phostestglobaltest WHERE testdate >= dateadd (-1 day to \
current_date) AND GLOBALRESULT like 'Pass%')"
        cur.execute(SELECT)
        for (passresult) in cur:
                flex1_pass = passresult[0]
        SELECT = "SELECT count(*) as failresult from (select distinct serialnumber FROM phostestglobaltest WHERE testdate >= dateadd (-1 day to \
current_date) AND GLOBALRESULT='Fail')"
        cur.execute(SELECT)
        for (failresult) in cur:
                flex1_fail = failresult[0]
        print 'Flex1:\t%d Pass, %d Fail' % (flex1_pass,flex1_fail)
        con_flex1.close()
else:
        print 'Flex1 DB skipped'
        
# get results for Flex 2
if flex2_connected:
        cur = con_flex2.cursor()
        SELECT = "SELECT count(*) as passresult from (select distinct serialnumber FROM phostestglobaltest WHERE testdate >= dateadd (-1 day to \
current_date) AND GLOBALRESULT like 'Pass%')"
        cur.execute(SELECT)
        for (passresult) in cur:
                flex2_pass = passresult[0]
        SELECT = "SELECT count(*) as failresult from (select distinct serialnumber FROM phostestglobaltest WHERE testdate >= dateadd (-1 day to \
current_date) AND GLOBALRESULT='Fail')"
        cur.execute(SELECT)
        for (failresult) in cur:
                flex2_fail = failresult[0]
        print 'Flex2:\t%d Pass, %d Fail' % (flex2_pass,flex2_fail)
        con_flex2.close()
else:
        print 'Flex2 DB skipped'
        
# get results for VCL
if vcl_connected:
        cur = con_vcl.cursor()
        SELECT = "SELECT count(*) as passresult from (select distinct serialnumber FROM phostestglobaltest WHERE testdate >= dateadd (-1 day to \
        current_date) AND GLOBALRESULT like 'Pass%')"
        cur.execute(SELECT)
        for (passresult) in cur:
                vcl_pass = passresult[0]

        SELECT = "SELECT count(*) as failresult from (select distinct serialnumber FROM phostestglobaltest WHERE testdate >= dateadd (-1 day to \
        current_date) AND GLOBALRESULT='Fail')"
        cur.execute(SELECT)
        for (failresult) in cur:
                vcl_fail = failresult[0]
        print 'VCL:\t%d Pass, %d Fail' % (vcl_pass,vcl_fail)
        con_vcl.close()
else:
        print "VCL DB skipped"

# get results for JBL
if vcl_connected:
        cur = con_jbl1.cursor()
        SELECT = "SELECT count(*) as passresult from (select distinct serialnumber FROM phostestglobaltest WHERE testdate >= dateadd (-1 day to \
        current_date) AND GLOBALRESULT like 'Pass%')"
        cur.execute(SELECT)
        for (passresult) in cur:
                jbl_pass = passresult[0]

        SELECT = "SELECT count(*) as failresult from (select distinct serialnumber FROM phostestglobaltest WHERE testdate >= dateadd (-1 day to \
        current_date) AND GLOBALRESULT='Fail')"
        cur.execute(SELECT)
        for (failresult) in cur:
                jbl_fail = failresult[0]
        print 'JBL:\t%d Pass, %d Fail' % (jbl_pass,jbl_fail)
        con_jbl1.close()
else:
        print "JBL DB skipped"


DB_UPDATE = 'INSERT INTO atestat.PASSFAIL_DAYLY (DATE, SERVER, PASS, FAIL ) VALUES (current_timestamp, "Ceragon", %d, %d)' % (ceragon_pass, ceragon_fail)
#print(DB_UPDATE)
cur_local = cnx.cursor()
cur_local.execute(DB_UPDATE)
cnx.commit()
#print 'Ceragon field updated'


flex1_pass = flex1_pass + flex2_pass 
flex1_fail = flex1_fail + flex2_fail

DB_UPDATE = 'INSERT INTO atestat.PASSFAIL_DAYLY (DATE, SERVER, PASS, FAIL ) VALUES (current_timestamp, "Flex", %d, %d)' % (flex1_pass, flex1_fail)
#print(DB_UPDATE)
cur_local = cnx.cursor()
cur_local.execute(DB_UPDATE)
cnx.commit()
#print 'Flex1 field updated'

#DB_UPDATE = 'INSERT INTO atestat.PASSFAIL_DAYLY (DATE, SERVER, PASS, FAIL ) VALUES (current_timestamp, "Flex2", %d, %d)' % (flex2_pass, flex2_fail)
#print(DB_UPDATE)
#cur_local = cnx.cursor()
#cur_local.execute(DB_UPDATE)
#cnx.commit()
#print 'Flex2 field updated'


ionics1_pass = ionics1_pass + ionics2_pass
ionics1_fail = ionics1_fail + ionics2_fail

DB_UPDATE = 'INSERT INTO atestat.PASSFAIL_DAYLY (DATE, SERVER, PASS, FAIL ) VALUES (current_timestamp, "Ionics", %d, %d)' % (ionics1_pass, ionics1_fail)
#print(DB_UPDATE)
cur_local = cnx.cursor()
cur_local.execute(DB_UPDATE)
cnx.commit()
#print 'Ionics1 field updated'

#DB_UPDATE = 'INSERT INTO atestat.PASSFAIL_DAYLY (DATE, SERVER, PASS, FAIL ) VALUES (current_timestamp, "Ionics2", %d, %d)' % (ionics2_pass, ionics2_fail)
#print(DB_UPDATE)
#cur_local = cnx.cursor()
#cur_local.execute(DB_UPDATE)
#cnx.commit()
#print 'Ionics2 field updated'

DB_UPDATE = 'INSERT INTO atestat.PASSFAIL_DAYLY (DATE, SERVER, PASS, FAIL ) VALUES (current_timestamp, "VCL", %d, %d)' % (vcl_pass, vcl_fail)
#print(DB_UPDATE)
cur_local = cnx.cursor()
cur_local.execute(DB_UPDATE)
cnx.commit()
#print 'VCL field updated'

DB_UPDATE = 'INSERT INTO atestat.PASSFAIL_DAYLY (DATE, SERVER, PASS, FAIL ) VALUES (current_timestamp, "JBL", %d, %d)' % (jbl_pass, jbl_fail)
#print(DB_UPDATE)
cur_local = cnx.cursor()
cur_local.execute(DB_UPDATE)
cnx.commit()
#print 'VCL field updated'


cnx.close()

now = time.strftime("%c")
## date and time representation

print "Script ended at: " + time.strftime("%c")
print "*****************************************************************************************"
