#!/usr/bin/pyhton
"""
Basic MySQL functionality for database creation.  Required input is a site URL.
@ Lindsey Anderson

"""
import MySQLdb as mysql
import sys, re, os
import string, random
import commands

class MySQLCreationError(Exception):
	pass

def __create_database(database=None, username=None, password=None):
	# Query definitions
	db_exists	= "select count(*) from information_schema.SCHEMATA \
                                where SCHEMA_NAME='{0}';".format(database) 
	db_create	= "create database {0}".format(database)	
	user_exists	= "select count(*) from mysql.user \
                               where user = '{0}' and host = '{1}'".format(database,'%')     
	user_add	= "create user {0} identified by '{1}'".format(username,password)
	user_grant	= "grant all on {0}.* to {1}".format(database,username)
	flush_privs     = "flush privileges"
	

	try:
		# Connect to the local MySQL instance
		connection = mysql.connect()
		cursor     = connection.cursor()
	
		# Check if our username exists on the server
		cursor.execute(user_exists)
		(count_rows,)=cursor.fetchone()
		if count_rows != 0:
			raise MySQLCreationError({"message":"User Creation Error: User " + \
						username + " exists."})
		# Check of our database exists on the server
		cursor.execute(db_exists)
		(count_rows,)=cursor.fetchone()
		if count_rows != 0:
			raise MySQLCreationError({"message": "DB Creation Error: " + \
						database + " exists."})
		# Create database 
		cursor.execute(db_create)
		# Create user
		cursor.execute(user_add)
		# Grant user access to our new db
		cursor.execute(user_grant)
		# Clean it up
		cursor.execute(flush_privs)
	except MySQLCreationError, e:
		msgargs=e.args[0]
		print "\n++ " + msgargs['message']
		return False
	cursor.close()	
	return True


def __create_randompass(length=14, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for x in range (length))

def __derive_database(sitename=None):
	# strip the TLD from domain name
	sitename = sitename[:12] if len(sitename) > 12 else sitename
	# strip periods, make it easier on mysql
	sitename = re.sub('\.', '', sitename)
	sitename = sitename + '_db'
	return sitename 

def __derive_username(sitename=None):
	sitename = sitename[:11] if len(sitename) > 11 else sitename
	sitename = re.sub('\.', '', sitename)
	sitename = sitename + '_user'
	return sitename

# MySQL Running Check
def __is_mysql_running():
	# this seems cheap, find a better way to do this
        psaux = commands.getoutput('ps -A');
        psef  = commands.getoutput('ps -ef');

        if 'mysql' in psaux:
                for each_var in string.split(psef, '\n'):
                        if 'mysql' in each_var:
                                return True
        return False

# MySQL Installation Check
def __is_mysql_installed():
	print "Could not connect to MySQL server"
	print "Attempting to locate binary"
	binary_check = "mysql"
	# attempt to pull the full path from PATH
        try:
		print "Binary found:\n"
                system_which = os.system('which mysql')
                return True
	# this is a last ditch effort.. maybe our path is wrong?
        except:
                for root, directories, files in os.walk('/'):
                	if binary_check in files:
                        	return True
        return False

###
# Simple test
### 
if __is_mysql_running():
	print "MySQL Creation"
	new_username = __derive_username(sitename="example.com")
	new_password = __create_randompass()
	new_database = __derive_database(sitename="example.com")
	if __create_database(database=new_database, username=new_username, password=new_password):
		print "Database and User creation successful!:\n"
		print ">> Username:",new_username
		print ">> Password:",new_password
		print ">> Database:",new_database
elif __is_mysql_installed():
	print "\nMySQL is installed but not started. Please start the service and retry."
else:
	print "Something went horribly, horribly wrong and you should probably just rebuild."
