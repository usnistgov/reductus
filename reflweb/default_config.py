#############################################################
# rename or copy this file to config.py if you make changes #
#############################################################

# change this to your fully-qualified domain name to run a 
# remote server.  The default value of localhost will
# only allow connections from the same computer.
#
# for remote (cloud) deployments, it is advised to remove 
# the "local" data_sources item below, and to serve static
# files using a standard webserver
#
# if use_redis is False, server will use in-memory cache.

jsonrpc_servername = "localhost"
jsonrpc_port = 8001
serve_staticfiles = True
use_redis = True
data_sources = {
    "ncnr": "http://ncnr.nist.gov/pub/",
    "local": "file:///"
}
file_helper = "http://ncnr.nist.gov/ipeek/listftpfiles.php"
