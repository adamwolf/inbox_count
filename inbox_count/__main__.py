#!/usr/bin/env python
from __future__ import print_function
import argparse

"""
 inbox_count tells you how many email messages are in your inbox.

https://github.com/adamwolf/inbox_count
"""
# Copyright 2009-2015 Adam Wolf
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

import sys
import imaplib
import getpass
import logging


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


def parse_args(args):
    description = "Logs into IMAP server HOST and displays the number of messages in USERNAME's inbox."
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument("-u", "--user", dest="username",
                        help="Username to log into server")
    parser.add_argument("--password", default=False,
                        help="Password to log into server.  "
                             "If not included and password file not specified, "
                             "password will be asked for interactively.")
    parser.add_argument("-s", "--server", dest="host",
                        help="Address of server")
    parser.add_argument("-p", "--port", dest="port", default="993",
                        help="Port of server, defaults to %default")
    parser.add_argument("--password-file", metavar="file",
                        help="Read password from password file FILE")
    parser.add_argument("--no-ssl", dest="ssl", action="store_false", default=True,
                        help="Do not use SSL.")
    parser.add_argument("-v", "--verbose", dest="verbose", action="store_true", default=False,
                        help="Be verbose.")
    parser.add_argument("--debug", dest="debug", action="store_true", default=False,
                        help="Be really verbose.")

    options = parser.parse_args()

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
    except ValueError:
        parser.error("Port specified as %s. Port must be an integer." % options.port)

    if options.password_file and options.password:
        parser.error("Both password file and password specified.")
    elif options.password_file:
        logger.info("Password file specified: %s", options.password_file)
        options.password = parse_password_file(options.password_file)
    elif not options.password:
        logger.debug("No password specified.")
        options.password = getpass.getpass()

    return options


def get_inbox_count_of_server(server):
    """Returns the count of the server's INBOX"""
    status, count = server.select('INBOX', readonly=True)
    # this count includes DELETED messages!  Guess who didn't know that about IMAP...
    logger.debug("Server returned status: %s", status)
    logger.debug("Server returned count: %s", count)
    status, message_numbers = server.search(None, 'UNDELETED')
    logger.debug("Server returned status: %s", status)
    logger.debug("Server returned UNDELETED message numbers: %s", message_numbers)
    count = len(message_numbers[0].split())
    return count


def parse_password_file(filename):
    with open(filename, 'r') as f:
        password = f.readline().rstrip()
    return password


def get_inbox_count(args):
    options = parse_args(args)
    logger.info("Connecting to %s", options.host)
    imap_server = connect(options.host,
                          options.port,
                          options.username,
                          options.password,
                          ssl=options.ssl)

    logger.info("Getting inbox count")
    inbox_count = get_inbox_count_of_server(imap_server)

    if options.verbose:
        logger.info("Number of emails in inbox: %d", inbox_count)

    return inbox_count


def main(args=None):
    logging.basicConfig(level=logging.WARNING,
                        format="%(levelname)-8s %(message)s")
    logger = logging.getLogger()

    if args is None:
        args = sys.argv[1:]
    count = get_inbox_count(args)
    print(count)


if __name__ == "__main__":
    main()
