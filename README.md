JustNginx - An improperly named installation script
================================
* [Just Curl](http://justcurl.com/) Currently exists and will be accepting this new version once completed.

This is an automated script for both virtual host creation in either Nginx or Apache. Other features will be added as we go to eventually encompass the following:

Features
-------------------------
* Apache Virtual Host creation
* Nginx Virtual Host creation
* MySQL Database creation
* MongoDB Database creation
* Wordpress installation
* Drupal installation

Usage 
-------------------------
	python <( curl 	-H "host: example.com" \
		-H "x-http: apache" \
		-H "x-port: 80" \
		-H "x-docroot: /var/www/vhosts/example.com" \
		-H "x-install: wordpress" justnginx.com)

These headers are likely to change as better ones are thought up.  Check back for current usage. 

Defaults
-------------------------

A host header must always be specified when attempting a virtual host installation.  The following are default values for the remaining headers:

* x-http:    apache 
* x-port:    80
* x-docroot: /var/www/vhosts/%{domain_name}
* x-install: none
