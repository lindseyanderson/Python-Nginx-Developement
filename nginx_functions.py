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
	
	# Transverse the nginx install path, pulling in only
	# files that will be loaded by nginx
	for path, subdirectories, files in os.walk(base_path):
		for name in fnmatch.filter(files, '*.conf'):
			current_file = os.path.join(path,name)
			with open(current_file) as file_data:
				for line in file_data:
					if not line.startswith('#'):
						if 'server_name' in line:
							found_alias =  line.split()[1]
							found_alias = found_alias[:-1]
							if found_alias == site_url:
								return True
	return False

print does_virtualhost_exist(site_url="${site_url}")

