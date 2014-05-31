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

from functools import wraps
import pyattask.session
from pyattask.exceptions import (
    AuthenticationError
)

def authenticated(function):
    """Decorator to check for an authenticated session

    For functions requiring authenticated sessions, prepend the definition
    with the @authenticated decorator.

    TODO(davidr): perhaps memoize this somehow to avoid calls on every function?
      maybe every 60s?
    """
    @wraps(function)
    def check_authenticated(*args, **kwargs):
        if not pyattask.session.get_session().is_authenticated():
            raise AuthenticationError(function.__name__, *args, **kwargs)

        return function(*args, **kwargs)
    return check_authenticated
