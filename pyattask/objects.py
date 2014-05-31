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

"""Common AtTask objects
"""

import pyattask.session
from pyattask.decorators import authenticated
from pyattask.exceptions import (
    GetHTTPError,
    GenericAPIError,
    AtTaskReturnError,
    MethodNotImplemented
)

import logging
log = logging.getLogger(__name__)


class AtTaskObject(object):
    """Generic AtTask objects class"""

    _api_endpoint = None
    _api_objcode = None
    _api_objattrs = {}
    _attrs = {}
    _dirty = False

    _allowed_rest_request_types = ('get', 'post', 'put', 'delete')

    def __init__(self):
        """Initialize the AtTaskSession object"""

    def __repr__(self):
        if "name" in self:
            # If we have a name in our attrs, we might as well display it
            id_ = '"{}"'.format(self['name'])
        elif "id" in self:
            id_ = self['id']
        else:
            id_ = "Uninitialized"
        return "<{}: {}>".format(self.__class__.__name__, id_)

    def __contains__(self, item):
        if item in self._attrs:
            return True
        else:
            return False

    def __getitem__(self, key):
        if key not in self:
            raise KeyError(key)
        elif not isinstance(key, basestring):
            raise TypeError("string")

        return self._attrs[key]

    def __setitem__(self, key, value):
        if not isinstance(key, basestring):
            raise TypeError("string")

        self._attrs[key] = value

        # Make a note that the object is dirty (i.e. we have made changes that
        # have not been flushed to AtTask
        self._dirty = True

    def __len__(self):
        return len(self._attrs)

    def __str__(self):
        if 'id' in self:
            return self['id']
        else:
            return ""

    @classmethod
    def endpoint(cls):
        """Returns the AtTask API endpoint for cls.

        Returns:
          string: ths AtTask API endpoint for cls
        """
        return cls._api_endpoint

    @classmethod
    def objcode(cls):
        """Returns the AtTask objCode for cls.

        Returns:
          string: the AtTask objCode name for cls
        """
        return cls._api_objcode

    @classmethod
    def objattrs(cls):
        """Returns a list of the supported AtTask API field names for cls.

        Returns:
          list: API field names for cls
        """
        return cls._api_objattrs

    @classmethod
    def from_json(cls, json):
        """Return initialized object from json.

        Args:
          json (dict): json serialization of cls

        Returns:
          cls
        """
        if json['objCode'] != cls.objcode():
            log.error("is proper {}".format(cls))

        objattrs = cls.objattrs()
        init_attrs = {}
        for key in json:
            if key in objattrs:
                init_attrs[key.lower()] = json[key]
            else:
                log.warning("attribute {}: {} found in JSON, not in _api_objattrs".format(
                    key, json[key]))

        return cls(attrs=init_attrs)

    @classmethod
    def search(cls, searchfields, params=None):
        """Perform a search on a given class and return matching instances of
        the class.

        Args:
          searchfields (dict): dictionary of search terms
          params (dict, optional): api request parameters

        Returns:
          [ cls,
            cls,
            ...,
            cls ]
        """
        if not params:
            params = {}

        json_resp = cls._search(searchfields, params)
        found_objs = list(cls._convert_from_json(json_resp))

        log.info("returning {}".format(found_objs))
        return found_objs

    @classmethod
    def get(cls, id_, allfields=None, params=None):
        """Fetch the data identified by object + id and return the initialized
        instance the class.

        Args:
          id_ (str): the id of the object
          allfields (bool, optional): return all available fields if True
          params (dict, optional): api request parameters

        Returns:
          object (cls): the object identified by id
        """

        if not params:
            params = {}

        if allfields:
            field_names = ",".join(cls.objattrs())
            params['fields'] = field_names

        json_resp = cls._get(id_, params)
        print params
        obj = cls.from_json(json_resp.get('data', []))

        log.info("returning {}".format(obj))
        return obj

    @classmethod
    def _convert_from_json(cls, json_resp):
        """Take a json object and turn it into an array of searchclass objects.

        Yields:
          cls
        """
        for result in json_resp.get('data', []):
            log.debug(result)
            yield cls.from_json(result)

    @classmethod
    @authenticated
    def _search(cls, searchfields, params):
        """Perform an API search on the given class

        Args:
          searchfields (dict): dictionary of search terms
          params (dict): api request parameters

        Returns:
          json: JSON-encoded response from the API
        """

        # Via HTTP, we don't draw a distinction between the search paramaters
        # and the rest of the api request paramaters. Just "add" the dicts
        # together.
        #
        # TODO(davidr): this is pretty stupid. the behavior exhibited by duped
        #   keys would be "undefined" from the end user's perspective.
        params = dict(searchfields.items() + params.items())

        url = pyattask.session.get_session()._url
        search_url = url + '/' + cls.endpoint() + '/search'
        # TODO(davidr): validate params against class?

        # TODO(davidr): _rest_transaction() throws a lot of errors. you
        #   should maybe check some of those out.
        json_rsp = cls._rest_transaction("get", search_url, params)
        return json_rsp

    @classmethod
    def _rest_transaction(cls, method, url, params):
        """Perform the nuts and bolts of the REST transaction

        Args:
          url (str): the transaction url
          method (str): get, post, put delete
          params (dict, optional) request parameters

        Returns:
          response (json): json response of query

        Raises:
          AtTaskReturnError
          GetHTTPError
          GenericAPIError
          MethodNotImplemented
        """

        if method not in cls._allowed_rest_request_types:
            raise MethodNotImplemented(method)

        session = pyattask.session.get_session()
        search_rsp = session._session.get(url, verify=False, params=params)
        log.info("GET {} returned {}".format(search_rsp.url,
                                             search_rsp.status_code))

        if search_rsp.status_code not in (200, 302):
            # TODO(davidr): must be other response codes?
            # TODO(davidr): any more specific error checking? Raising an
            #   exception might not be what we want here
            raise GetHTTPError("GET {} returned error {}: {}".format(
                search_rsp.url, search_rsp.status_code, search_rsp.reason))

        response = search_rsp.json()
        log.debug("search returned json: {}".format(response))

        if 'error' in response:
            raise AtTaskReturnError(response['error'])
        elif 'data' not in response:
            raise GenericAPIError("data or error not in json resp: {}".format(
                response))

        # TODO(davidr): maybe only return response['data']? what would that
        #   break?
        return response

    @classmethod
    @authenticated
    def _get(cls, id_, params=None):
        """Return a single object corresponding to the ID

        Args:
          id_ (str): the ID of the object to get
          params (dict optional): parameter dict

        Returns:
          response (json): the json data for the object

        TODO(davidr): definitely should raise some sort of notfound error
        """
        if not params:
            params = {}

        print "woot", params
        url = pyattask.session.get_session()._url
        get_url = url + '/' + cls.endpoint() + '/' + id_

        json_rsp = cls._rest_transaction("get", get_url, params=params)
        return json_rsp
