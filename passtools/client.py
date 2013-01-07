#!/usr/bin/env python
##########################################
# pt_client.py
# 
# Interface to PassTools REST API
#
# Copyright 2012, Tello, Inc.
##########################################
"""
HTTP interface to PassTools REST API, used indirectly, via other PassTools classes.

"""

try:
    import simplejson as json
except ImportError:
    import json

import copy
import logging
import urllib
import urllib2

import exceptions


BASE_URL = 'https://api.passtools.com/v1'

#########################
# CLASS PassToolsClient
# 
#
#########################
class PassToolsClient(object):

    def __init__(self, api_key=None):
        self.api_key = api_key

    def get_json(self, path, **kwargs):
        """
        Make an HTTP GET request of specified URL

        @type path: str
        @param path: target URL (base_url will be prepended)
        @type kwargs: kwargs
        @param kwargs: any desired URL parameters
        @return: HTTP request status code and response data as json.
        """

        # Append any request data
        kwargs['api_key'] = self.api_key

        # Assemble request url
        request_url = "%s%s?%s" % (BASE_URL, path, urllib.urlencode(kwargs))

        # create request
        req = urllib2.Request(request_url)
        logging.debug("PassToolsClient request_url: %s" % request_url)

        # and make the request
        response_code, response_data = self.__run_request(req)
        if response_code == 200:
            logging.debug("PassToolsClient response:\n%s" % (response_data))

        return response_code, response_data

    def get(self, request_url, **kwargs):
        """
        Make an HTTP GET request of specified URL

        @type request_url: str
        @param request_url: target URL (base_url will be prepended)
        @type kwargs: kwargs
        @param kwargs: any desired URL parameters
        @return: HTTP request status code and response data as python dict.
        """
        response_code, response_data = self.get_json(request_url, **kwargs)
        if response_code == 200:
            response_data = json.loads(response_data, encoding="ISO-8859-1")
        return response_code, response_data

    def post(self, path, kwargs):
        """
        Make an HTTP POST request of specified URL

        @type path: str
        @param path: target URL (base_url will be prepended)
        @type kwargs: kwargs
        @param kwargs: any desired URL parameters
        @return: HTTP request status code and response data as json.
        """
        # Assemble request url
        request_url = "%s%s" % (BASE_URL, path)

        kwargs = copy.deepcopy(kwargs)
        # Append api_key to request
        self.__api_key_check()
        kwargs["api_key"] = self.api_key

        # Format the input data
        encoded_kwargs = urllib.urlencode(kwargs)
        logging.debug("encoded kwargs: %s" % encoded_kwargs)

        # Prepare headers
        headers = {}
        headers['Content-Type'] = 'application/x-www-form-urlencoded'
        headers['Accept'] = '*/*'

        # create a request
        req = urllib2.Request(request_url, encoded_kwargs, headers=headers)
        logging.debug("pt_post request_url: %s" % request_url)

        # and make the request
        response_code, response_data = self.__run_request(req)
        if response_code == 200:
            logging.debug("pt_post response:\n%s" % (response_data))

        return response_code, response_data

    def post_dict(self, request_url, kwargs):
        """
        Make an HTTP POST request of specified URL

        @type request_url: str
        @param request_url: target URL (base_url will be prepended)
        @type kwargs: kwargs
        @param kwargs: any desired URL parameters
        @return: HTTP request status code and response data as python dict.
        """
        response_code, response_data = self.post_json(request_url, kwargs)
        if response_code == 200:
            response_data = json.loads(response_data, encoding="ISO-8859-1")
        return response_code, response_data

    def put(self, path, kwargs = {}):
        """
        Make an HTTP PUT request of specified URL

        @type path: str
        @param path: target URL (base_url will be prepended)
        @type kwargs: kwargs
        @param kwargs: any desired URL parameters
        @return: HTTP request status code and response data as json.
        """
        # Assemble request url
        request_url = "%s%s" % (BASE_URL, path)


        kwargs = copy.deepcopy(kwargs)
        # Append api_key to request
        self.__api_key_check()
        kwargs["api_key"] = self.api_key

        # Format the input data
        encoded_kwargs = urllib.urlencode(kwargs)
        logging.debug("encoded kwargs: %s" % encoded_kwargs)

        # Prepare headers
        headers = {}
        headers['Content-Type'] = 'application/x-www-form-urlencoded'
        headers['Accept'] = '*/*'

        # create a request
        req = urllib2.Request(request_url, encoded_kwargs, headers=headers)
        req.get_method = lambda: 'PUT'
        logging.debug("pt_put request_url: %s" % request_url)

        # and make the request
        response_code, response_data = self.__run_request(req)

        return response_code, response_data

    def put_json(self, request_url, kwargs = {}):
        """
        Make an HTTP PUT request of specified URL

        @type request_url: str
        @param request_url: target URL (base_url will be prepended)
        @type kwargs: kwargs
        @param kwargs: any desired URL parameters
        @return: HTTP request status code and response data as python dict.
        """
        response_code, response_data = self.put(request_url, kwargs)
        if response_code == 200:
            response_data_json = json.loads(response_data, encoding="ISO-8859-1")
            logging.debug("pt_put response:\n%s" %
                             json.dumps(response_data, sort_keys = True, indent = 2))
        return response_code, response_data_json

    def delete(self, path, kwargs):
        """
        Make an HTTP DELETE request of specified URL

        @type path: str
        @param path: target URL (base_url will be prepended)
        @type kwargs: kwargs
        @param kwargs: any desired URL parameters
        @return: HTTP request status code and response data as json.
        """
        # Assemble request url
        request_url = "%s%s?api_key=%s" % (BASE_URL, path, self.api_key)

        # Append any request data
        for keyName in kwargs:
            request_url += "&" + keyName + "=" + str(kwargs[keyName])

        # Prepare headers
        headers = {}
        headers['Content-Type'] = 'application/x-www-form-urlencoded'
        headers['Accept'] = '*/*'

        # create a request
        req = urllib2.Request(request_url)
        req.get_method = lambda: 'DELETE'
        logging.debug("pt_put request_url: %s" % request_url)

        # and make the request
        response_code, response_data = self.__run_request(req)

        return response_code, response_data

    def delete_json(self, request_url, kwargs):
        """
        Make an HTTP DELETE request of specified URL

        @type request_url: str
        @param request_url: target URL (base_url will be prepended)
        @type kwargs: kwargs
        @param kwargs: any desired URL parameters
        @return: HTTP request status code and response data as python dict.
        """
        response_code, response_data = self.delete(request_url, kwargs)
        if response_code == 200:
            response_data_json = json.loads(response_data, encoding="ISO-8859-1")
            logging.debug("pt_delete response:\n%s" %
                             json.dumps(response_data, sort_keys = True, indent = 2))
        return response_code, response_data_json


    def __api_key_check(self):
        if not self.api_key:
            raise exceptions.AuthenticationException("No API secret key provided. Did you create a service instance?")

    def __dispatch_exception(self, response_code, fail_msg, request):
        request_url = request._Request__original
        get_params = request_url.split("?")
        post_params = request.headers
        if len(get_params) > 1:
            params = get_params[1:]
        elif post_params != {}:
            params = post_params
        else:
            params = ""
        if response_code < 400:
            raise exceptions.PassToolsException(message = fail_msg, http_status = response_code)
        elif response_code == 400:
            raise exceptions.InvalidRequestException(message = fail_msg, param=params, http_status = response_code)
        elif response_code == 401:
            raise exceptions.AuthenticationException(message = fail_msg, http_status = response_code)
        elif response_code == 406:
            raise exceptions.InvalidRequestException(message = fail_msg, param=params, http_status = response_code)
        elif response_code == 429:
            raise exceptions.TooManyRequestsException(message = fail_msg, http_status = response_code)
        elif response_code >= 500:
            raise exceptions.InternalServerException(message = fail_msg, http_status = response_code)
        else:
            raise exceptions.APIException()

    def __run_request(self, request):
        response_code = None
        response_data = {}
        try:
            # Open the request on the url
            http_verbosity = 0     # For debugging purposes...turn it up to 10
            opener = urllib2.build_opener(urllib2.HTTPHandler(http_verbosity))
            request_handle = opener.open(request)

            # Get the data from the response
            response_code = request_handle.code
            response_data = request_handle.read()
            request_handle.close()
            logging.debug("Response code: %d" % response_code)
        except urllib2.URLError, e:
            fail_msg = "Error"
            # If exception includes no status code but a reason, it's a URLError
            if hasattr(e, 'reason') and hasattr(e.reason, 'errno'):
                response_code = e.reason.errno
                fail_msg = "Communication with host '%s' failed: %s (errno %s)" % (request.host, e.reason.strerror, response_code)
             # else if exception includes an HTTP status code, it's an HTTPError
            elif hasattr(e, 'code'):
                fail_msg = self.__req_error(e)

            logging.error(fail_msg)

            if response_code != 200:
                self.__dispatch_exception(response_code, fail_msg, request)

        return response_code, response_data



    def __req_error(self, e):
        response_code = e.code
        fail_msg = "HTTPError (%s)" % response_code
        if response_code < 500:
        # If not a server error, read error details from the returned page
            try:
                err_page = json.load(e)
                if 'description' in err_page:
                    fail_msg += (" %s" % err_page['description'])
                if 'details' in err_page:
                    if err_page['details'] == "field errors" and "fieldErrors" in err_page:
                        fail_msg += " Details:\n"
                        for err_item in err_page['fieldErrors']:
                            fail_msg += err_item["message"] + "\n"
                    else:
                        fail_msg += (" Details: '%s'" % err_page['details'])
            except: 
                raise
        else: # For a server error, don't count on an error page
             if hasattr(e, 'msg'):
                fail_msg += (": %s" % e.msg)                
        return fail_msg

