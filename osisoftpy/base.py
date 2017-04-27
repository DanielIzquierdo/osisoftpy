# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import unicode_literals

import logging

log = logging.getLogger(__name__)


class Base(object):
    """
    
    """

    def __init__(self):

        """

        """
        msg = 'Classes which inherit osisoftpy.Base must implement __init__'
        log.error(msg, exc_info=True)
        raise NotImplementedError()

    #
    # def __getattr__(self, key):
    #     """
    #
    #     :param key:
    #     :return:
    #     """
    #     try:
    #         return self.__dict__[key]
    #     except KeyError:
    #         msg = '"{}" object has no attribute "{}"'
    #         raise AttributeError(msg.format(type(self).__name__, key))
    #
    # def __setattr__(self, key, value):
    #     """
    #
    #     :param key:
    #     :param value:
    #     """
    #     try:
    #         self.__dict__[key] = value
    #     except KeyError:
    #         msg = '"{}" object has no attribute "{}"'
    #         raise AttributeError(msg.format(type(self).__name__, key))
    #     except ValueError:
    #         msg = 'Invalid value "{}" for "{}" object attribute "{}"'
    #         raise AttributeError(msg.format(value, type(self).__name__, key))
