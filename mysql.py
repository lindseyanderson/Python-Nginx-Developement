#!/usr/bin/python

import commands
import MySQLdb
import string
import os, sys

# MySQL installer
def install_mysql():
	print "Please install MySQL and re-run this script ( feature not available )."	

# MySQL Running Check
def is_mysql_running():	
	psaux = commands.getoutput('ps -A');
	psef  = commands.getoutput('ps -ef');
	
	if 'mysql' in psaux:
		for each_var in string.split(psef, '\n'):
			if 'mysql' in each_var:
				return True
	return False

# MySQL Installation Check
def is_mysql_installed():
	checkMySQLrunning = is_mysql_running()
	if checkMySQLrunning:
		return True
	else:
		binary_check = "mysql"
		try:
			system_which = os.system('which mysql')
			return True
		except:
			for root, directories, files in os.walk('/'):
				if binary_check in files:
					return True
	return False
	
# MySQL connect test
def is_mysql_connectable():
	global username
	global password
	global db
	username = raw_input("Username: ")
	password = raw_input("Password: ")
	if password:
		try: 
			db = MySQLdb.connect(user=username, passwd=password, db="temp")
			return "password, connected, db"
		except MySQLdb.OperationalError:
			print "OE"
			return False
		else:
			db = MySQLdb.connect(user=username, password=password)
			return "password, connected, no db"
	else:
		try:
			db = MySQLdb.connect(user=username, db="temp")
			return "Blank password, connected, db"
		except MySQLdb.OperationalError:
			print "OE"
			return False
		else:
			db = MySQLdb.connect(user=username)
			return "Blank password, connected, no db" 	
	return False

if is_mysql_installed():
	print is_mysql_connectable()
#		print "Connection to MySQL instance successful."
#	else:
#		if is_mysql_installed():
#			print "MySQL is Installed - credentials must be bad."
#			cursor = db.cursor()
#			cursor.execute("""SHOW TABLES""")
#			print cursor.fetchone()
#		else:
#			install_mysql()
#else:
#	print "Something went horribly, horribly wrong."
#
#	cursor.close()
#	db.close()
