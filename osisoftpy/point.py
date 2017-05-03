# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import unicode_literals


from .base import Base


class Point(Base):
    """The Point class provides methods for the available PI points"""

    def __init__(self, name=None, description=None, uniqueid=None, webid=None,
                 datatype=None):
        # type: (str, str, str, str, str) -> object

        """

        :rtype: Point object
        :param name: 
        :param description: 
        :param uniqueid: 
        :param webid: 
        :param datatype: 
        """

        self.name = name
        self.description = description
        self.uniqueid = uniqueid
        self.webid = webid
        self.datatype = datatype
        self.current_value = None
        self.interpolated_values = None
        self.recorded_values = None
        self.plot_values = None
        self.summary_values = None
        self.end_value = None
