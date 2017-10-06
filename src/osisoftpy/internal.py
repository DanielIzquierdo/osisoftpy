# -*- coding: utf-8 -*-

#    Copyright 2017 DST Controls
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
"""
osisoftpy.internal
~~~~~~~~~~~~
This module provides utility functions that are consumed internally by 
OSIsoftPy.
"""
from __future__ import (absolute_import, division, unicode_literals)
from future.builtins import *
import logging
import requests
import time
from osisoftpy.structures import APIResponse
from osisoftpy.exceptions import (PIWebAPIError, Unauthorized, HTTPError)

log = logging.getLogger(__name__)


def get(url, session, params=None):
    """Constructs a HTTP request to the provided url.

    Returns an APIResponse namedtuple with two named fields: response and
    session. Both objects are standard Requests objects: Requests.Response,
    and Requests.Session

    :param url: URL to send the HTTP request to.
    :param session: A Requests Session object.
    :param params: Paramaters to be passed to the GET request.
        InsecureRequestWarning will be disabled.

    :return: :class:`APIResponse <APIResponse>` object
    :rtype: osisoftpy.APIResponse
    """
    s = session
    isCrawling = True

    with s:
        try:
            while isCrawling:
                isCrawling = False
                r = APIResponse(s.get(url, params=params), s)
                if r.response.status_code == 401:
                    raise Unauthorized(
                        'Authorization denied - incorrect username or password.')
                if r.response.status_code != 200:
                    raise HTTPError(
                        'Wrong server response: %s %s' %
                        (r.response.status_code, r.response.reason))
                json = r.response.json()
                if 'Errors' in json and json.get('Errors').__len__() > 0:
                    error = json.get('Errors')[0]
                    if(error['ErrorCode'] == 20):
                        print('Database is being crawled. Retrying in 5 sec.')
                        isCrawling = True
                        time.sleep(5)

                        # should we terminate if database is stuck in crawling state?
                        
                    else:
                        msg = 'PI Web API returned an error: {}'
                        raise PIWebAPIError(msg.format(error))
            return r
        except:
            raise

def post(url, session, params=None, json=None):
    """Constructs a HTTP request to the provided url.

    Returns an APIResponse namedtuple with two named fields: response and
    session. Both objects are standard Requests objects: Requests.Response,
    and Requests.Session

    :param url: URL to send the HTTP request to.
    :param session: A Requests Session object.
    :param params: Paramaters to be passed to the GET request.
        InsecureRequestWarning will be disabled.

    :return: :class:`APIResponse <APIResponse>` object
    :rtype: osisoftpy.APIResponse
    """
    s = session

    with s:
        try:
            r = APIResponse(s.post(url, json=json, params=params), s)
            if r.response.status_code == 401:
                raise Unauthorized(
                    'Server rejected request: wrong username or password')
            if r.response.status_code != 202:
                raise HTTPError(
                    'Wrong server response: %s %s' %
                    (r.response.status_code, r.response.reason))
            return r
        except:
            raise

def put(url, session, params=None):

    s = session

    with s:
        try:
            r = APIResponse(s.put(url, params=params), s)
            if r.response.status_code == 401:
                raise Unauthorized(
                    'Server rejected request: wrong username or password')
            if r.response.status_code != 200:
                raise HTTPError(
                    'Wrong server response: %s %s' %
                    (r.response.status, r.response.reason))
            json = r.response.json()
            if 'Errors' in json and json.get('Errors').__len__() > 0:
                msg = 'PI Web API returned an error: {}'
                raise PIWebAPIError(msg.format(json.get('Errors')))
            return r
        except:
            raise


def get_batch(method, webapi, points, action, params=None):
    s = webapi.session

    with s:
        payload = {}

        for p in points:
            url = '{}streams/{}/{}'.format(webapi.url, p.webid, action)
            r = s.prepare_request(requests.Request(method, url, params=params))
            payload[p.name] = dict(Method=r.method, Resource=r.url)

        r = APIResponse(s.post('{}batch/'.format(webapi.url), json=payload), s)
        json = r.response.json()
        if 'Errors' in json and json.get('Errors').__len__() > 0:
            msg = 'PI Web API returned an error: {}'
            raise PIWebAPIError(msg.format(json.get('Errors')))
        else:
            return r


def _stringify(**kwargs):
    """
    Return a concatenated string of the keys and values of the kwargs
    Source: http://stackoverflow.com/a/39623935
    :param kwargs: kwargs to be combined into a single string
    :return: String representation of the kwargs
    """
    return (','.join('{0}={1!r}'.format(k, v)
                     for k, v in kwargs.items()))
