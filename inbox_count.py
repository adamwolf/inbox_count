#!/usr/bin/env python
"""
inbox_count.py
 
inbox_count tells you how many email are in your inbox. 

http://feelslikeburning.com/projects/inbox_count/
"""
# Copyright 2009 Adam Wolf
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import sys, imaplib, getpass, logging, ConfigParser
from optparse import OptionParser

def connect(host, port, username, password, ssl=True):
    """Connect and authenticate to IMAP4 server."""
    if ssl:
        logger.debug("Connecting to %s using SSL", host)
        server = imaplib.IMAP4_SSL(host, port)
    else:
        logger.debug("Connecting to %s without SSL", host)
        server = imaplib.IMAP4(host, port)
    logger.info("Logging in")
    server.login(username, password)
    return server

def parse_commandline_parameters():
    usage = """usage: %prog [options] [-u USERNAME -s HOST]

Logs into IMAP server HOST and displays the number of messages in USERNAME's inbox."""

    parser = OptionParser(usage)
    parser.add_option("-u", "--user", dest="username", help="Username to log into server")
    parser.add_option("--password", dest="password", default=False, help="Password to log into server.  If not included and password file not specified, password will be asked for interactively.")
    parser.add_option("-s", "--server", dest="host", help="Address of server")
    parser.add_option("-p", "--port", dest="port", default="993", help="Port of server, defaults to %default")
    parser.add_option("--password-file", dest="password_file", metavar="file", help="Read password from password file FILE")
    parser.add_option("--no-ssl", dest="ssl", action="store_false", default=True, help="Do not use SSL.")
    parser.add_option("-v", "--verbose", dest="verbose", action="store_true", default=False, help="Be verbose.")
    parser.add_option("--debug", dest="debug", action="store_true", default=False, help="Be really verbose.")

    options, args = parser.parse_args()
    
    if options.debug:
        logger.setLevel(logging.DEBUG)
    elif options.verbose:
        logger.setLevel(logging.INFO)
    
    if not options.host and not options.username:
        parser.error("Server host and username must be specified.")
    if not options.host:
        parser.error("Server host must be specified.")
    if not options.username:
        parser.error("Username must be specified.")
    
    try:
        options.port = int(options.port)
    except ValueError, e:
        parser.error("Port specified as %s. Port must be an integer." % options.port)

    if options.password_file and options.password:
        parser.error("Both password file and password specified.")
    elif options.password_file:
        logger.info("Password file specified: %s", options.password_file)
        options.password = parse_password_file(options.password_file)
    elif not options.password:
        logger.debug("No password specified.")
        options.password = getpass.getpass()

    return options, args

def get_inbox_count(server):
    """Returns the count of the server's INBOX"""
    status, count = server.select('INBOX', readonly=True)
    logger.debug("Server returned status: %s", status)
    logger.debug("Server returned count: %s", count)
    count = int(count[0])
    return count

def parse_password_file(filename):
    f = open(filename, "r")
    password = f.readline().rstrip()
    f.close()
    return password

def get_config():
    logger.debug("Parsing command line parameters")
    options, args = parse_commandline_parameters()

    return options

def main():
    
    options = get_config()

    logging.info("Connecting to %s", options.host)
    imap_server = connect(options.host, 
            options.port, 
            options.username,
            options.password,
            ssl=options.ssl)
    
    logging.info("Getting inbox count")
    inbox_count = get_inbox_count(imap_server)
    
    if options.verbose:
        logger.info("Number of emails in inbox: %d", inbox_count)

    print inbox_count
    return inbox_count

if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING,
            format="%(levelname)-8s %(message)s")
    logger = logging.getLogger()
    
    exit_code = main()
    sys.exit(exit_code)
