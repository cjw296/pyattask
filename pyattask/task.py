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

import pyattask.objects

import logging
log = logging.getLogger(__name__)


class Task(pyattask.objects.AtTaskObject):
    """Generic AtTask objects class"""

    _api_endpoint = "task"
    _api_objcode = "TASK"
    _api_objattrs = ["ID", "name", "objCode", "percentComplete",
                     "plannedCompletionDate", "plannedStartDate", "priority",
                     "progressStatus", "projectedCompletionDate",
                     "projectedStartDate", "status", "taskNumber", "wbs",
                     "workRequired"]

    def __init__(self, **kwargs):
        self._attrs = kwargs['attrs']
