#!/usr/bin/env python
# title           :ftpserver-cli.py
# description     :CLI ftp server.
# author          :Stefano Palazzo, Valerio Riggi
# usage           :./ftpserver-cli.py --d=/path/to/dir
# python_version  :2.7.9
# ==============================================================================

import sys
import os
# sys.path.append("/path/to/pyftpdlib-svn") # enter your proper path here
import argparse

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer


def processCmdLineOptions():
    global optparser
    optparser = argparse.ArgumentParser(description="ftpserver-cli",
                                        formatter_class=argparse.RawDescriptionHelpFormatter)
    optparser.add_argument('-v', '--verbose', dest='verbose', action='store_true')
    optparser.set_defaults(verbose=False)
    optparser.add_argument('-u', '--username', action='store', type=str,
                           default="user", help="username")
    optparser.add_argument('-p', '--password', action='store', type=str,
                           default="12345", help="password")
    optparser.add_argument('-t', '--port', action='store', type=int,
                           default="21", help="port")
    optparser.add_argument('-d', '--directory', action='store', type=str,
                           default=False, help="port")
    optargs = optparser.parse_args(sys.argv[1:])  # (sys.argv)
    return optargs


optargs = processCmdLineOptions()

if not optargs.directory:
    sys.exit("You must specify a directory with -d")
if not os.path.isdir(optargs.directory):
    sys.exit("Directory %s not found. Please specify a different directory with -d" % optargs.directory)

if optargs.verbose:
    print(
        "Using: user: %s pass: %s port: %d dir: %s" % (
        optargs.username, optargs.password, optargs.port, optargs.directory))

authorizer = DummyAuthorizer()
authorizer.add_user(optargs.username, optargs.password, optargs.directory, perm="elradfmw")
# authorizer.add_anonymous("/home/nobody")

handler = FTPHandler
handler.authorizer = authorizer

server = FTPServer(("127.0.0.1", optargs.port), handler)
server.serve_forever()
