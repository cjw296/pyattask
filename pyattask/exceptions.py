# -*- coding: utf-8 -*-
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

"""Exceptions"""


class AtTaskException(Exception):
    """Catchall base class for exceptions"""
    pass


class NoSession(AtTaskException):
    """A session has been referenced that does not exist"""
    pass


class GetHTTPError(AtTaskException):
    """A generic error HTTP error in an API transaction"""
    pass


class GenericAPIError(AtTaskException):
    """A request to the API has returned no data, only errors"""
    pass


class AtTaskReturnError(AtTaskException):
    pass


class AuthenticationError(AtTaskException):
    pass


class MethodNotImplemented(AtTaskException):
    pass
