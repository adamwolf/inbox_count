inbox count
===============
`
    gilgamesh:~/projects/inbox_count $ ./inbox_count.py -h
    Usage: inbox_count.py [options] [-u USERNAME -s HOST]
    
    Logs into IMAP server HOST and displays the number of messages in USERNAME's inbox.
    
    Options:
      -h, --help            show this help message and exit
      -u USERNAME, --user=USERNAME
                            Username to log into server
      --password=PASSWORD   Password to log into server.  If not included and
                            password file not specified, password will be asked
                            for interactively.
      -s HOST, --server=HOST
                            Address of server
      -p PORT, --port=PORT  Port of server, defaults to 993
      --password-file=file  Read password from password file FILE
      --no-ssl              Do not use SSL.
      -v, --verbose         Be verbose.
      --debug               Be really verbose.
`

Example
-------
    gilgamesh:~/projects/inbox_count$ ./inbox_count.py -u example_user -s email.example.org --password-file password
    25

If you don't specify a password file or a password on the command line, inbox_count will ask you interactively.

    gilgamesh:~/projects/inbox_count$ ./inbox_count.py -u example_user -s email.example.org
    25


Motivation
----------
I was inspired by a blog post at http://thomas.apestaart.org/log/?p=785. In it, Thomas uses a script to graph the number of emails in his Evolution email inbox, helping him turn "Inbox Zero" into a game.  I don't use Evolution.

In that vein, this script returns a return code equal to the number of emails in your inbox.  Unix tradition is that a return code of zero is success.

It's not my intention, however, that you use this script to compulsively check your email status.  That would likely be counterproductive--instead, it's meant for crontastically recording your inbox counts so you can make pretty graphs and track yourself.

Security
--------
Because command line arguments are usually available to other users on a system, inbox_count.py lets you specify the password in a password file.  You can use filesystem permissions to lock down that password.

Licensing
---------
This software is copyright 2009 Adam Wolf, and is distributed under the terms of the GNU General Public License.

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

Troubleshooting, Questions, or Comments:
----------------------------------------
inbox_count is located at http://feelslikeburning.com/projects/inbox_count

The code is currently maintained at http://github.com/adamwolf/inbox_count

Feel free to contact me at http://feelslikeburning.com/contact

