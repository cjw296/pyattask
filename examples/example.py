#!/usr/bin/env python

#  Copyright (C) 2014 Jump Operations, LLC
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to:
#    Free Software Foundation, Inc.
#    51 Franklin Street, Fifth Floor
#    Boston, MA  02110-1301, USA.

import pyattask.session
import pyattask.task
import pyattask.user
import pyattask.project
import ConfigParser

import logging

log = logging.getLogger("pyattask")
log.setLevel(logging.DEBUG)
format_string =  "%(asctime)s level=%(levelname)s name=%(name)s "
format_string += "lineno=%(lineno)s %(message)s"
ch = logging.StreamHandler()
formatter = logging.Formatter(format_string)
ch.setFormatter(formatter)
log.addHandler(ch)


def main():

    config = ConfigParser.ConfigParser()
    config.read("pyattask.ini")

    url = config.get("Production", "url")
    username = config.get("Production", "username")
    password = config.get("Production", "password")
    domain = config.get("Production", "domain")
    pyattask.session.create_session(url, forcetlsone=True)
    if pyattask.session.get_session().is_authenticated():
        print "Authenticated"
    else:
        print pyattask.session.get_session().login(username, password, domain=domain)
        if pyattask.session.get_session().is_authenticated():
            print "Authenticated (after login)"

    pyattask.task.Task.search({'status': "INP", 'wbs': 2})
    myuser = pyattask.user.User.current_user()
    print myuser.__repr__()


if __name__ == "__main__":
    main()
