#!/usr/bin/python
#
# Nginx functions script
#
# @author: Lindsey Anderson
# @date: 21/04/2013

import os, sys
import commands
import fnmatch

def is_nginx_installed():
	# First release we'll assume php-fpm is installed
	# We'll revisit the check after the status is updated


	# Check nginx installation status
        print "Attempting to locate binary"
        binary_check = "nginx"
        # attempt to pull the full path from PATH
	# Should probably try to use dpkg/rpm to determine status
	# unfortunately doesn't account for source installs
        try:
                print "Binary found:\n"
                system_which = os.system('which nginx')
                return True
        # this is a last ditch effort.. maybe our path is wrong?
        except:
                for root, directories, files in os.walk('/'):
                        if binary_check in files:
                                return True
        return False

def is_nginx_running():
	# Check nginx running status
        psaux = commands.getoutput('ps -A');
        psef  = commands.getoutput('ps -ef');

        if 'nginx' in psaux:
                for each_var in string.split(psef, '\n'):
                        if 'nginx' in each_var:
                                return True
        return False


def does_virtualhost_exist(site_url=None):
	# Check virtual host exists
	base_path = '/etc/nginx'

	# Get a list of all files within the base path that end in .conf
	files = [ os.path.join(subdir, filename)
			for (subdir, directories, files) in os.walk(base_path)
			for filename in fnmatch.filter(files, '*.conf') ]

	# Pull all server_name directives that are active within those files
	server_blocks = [ line for file in files
			for line in open(file,'r')
			if 'server_name' in line
			if not line.startswith('#') ]

	# We need to find only the actual data, strip the fat away
	# multiple server_names will result in sublists
	stripped_blocks = [ found_urls.strip(' server_name \;\n') for found_urls in server_blocks ]

	# flatten the lists
	nested_blocks = [ block.split(' ') for block in stripped_blocks ]

	server_names = [ value for sublist in nested_blocks for value in sublist ]

	# See if our site_url is in the list
	for server_name in server_names:
		if server_name == site_url:
			print "Site URL exists as an active server_name"
			return True
	return False


def check_directories_exist():
	available_directory = '/etc/nginx/sites-available'
	enabled_directory   = '/etc/nginx/sites-enabled'

	if not os.path.exists(available_directory):
		try:
			os.makedirs(available_directory)
			return True
		except:
			print "Something bad happened!"
			sys.exit(0)
	elif not os.path.exists(enabled_directory):
		try:
			os.makedirs(enabled_directory)
			return True
		except:
			print "Something bad happened!"
			sys.exit(0)
	else:
		return True
	return False


def check_nginxconf_includes():
	# Testing purposes
	input_file = 'nginx.conf'
	output_file = 'nginx_new.conf'
	append_line = '    include /etc/nginx/sites-enabled/*;\n'

	# Check for our include line in the nginx configuration
	with open(input_file, 'r') as file_data:
		content = file_data.readlines()
		if append_line in content:
			return True

	# Find the line we can safely insert our include into
	line_number = [ i+1 for i, line in enumerate(open(input_file, 'r'))
                if 'http {' in line ]

	# Get data from old nginx.conf, this will be our backup
	old_file = open(input_file, "r")
	new_file_array = []
	for line_num, line in enumerate(old_file):
		try:
	        	if line_num == line_number[0]:
	        	        new_file_array.append(append_line)
			new_file_array.append(line)
		except:
			new_file_array.append(line)

	# Create new nginx.conf
	new_file = open(output_file, "w")
	for item in new_file_array:
	        new_file.write("%s" % item)

	# Move our old nginx configuration to a backup
	temp_file_path = input_file
	os.rename(input_file, input_file + '-OLD')
	os.rename(output_file, temp_file_path)

	# Our include now exists
	return True


print check_nginxconf_includes()
