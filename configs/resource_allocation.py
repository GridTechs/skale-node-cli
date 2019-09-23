#   -*- coding: utf-8 -*-
#
#   This file is part of skale-node-cli
#
#   Copyright (C) 2019 SKALE Labs
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os
from configs.node import NODE_DATA_PATH
from core.config import THIRDPARTY_FOLDER_PATH, DATAFILES_FOLDER

MEDIUM_DIVIDER = 1
SMALL_DIVIDER = 8
TINY_DIVIDER = 128

TIMES = 1
TIMEOUT = 1
MEMORY_FACTOR = 0.9
DISK_FACTOR = 0.8

RESOURCE_ALLOCATION_FILENAME = 'resource_allocation.json'
RESOURCE_ALLOCATION_FILEPATH = os.path.join(NODE_DATA_PATH, RESOURCE_ALLOCATION_FILENAME)

DISK_MOUNTPOINT_FILENAME = 'disk_mountpoint.txt'
DISK_MOUNTPOINT_FILEPATH = os.path.join(NODE_DATA_PATH, DISK_MOUNTPOINT_FILENAME)

CONVOY_HELPER_SCRIPT_FILENAME = 'dm_dev_partition.sh'
CONVOY_HELPER_SCRIPT_FILEPATH = os.path.join(THIRDPARTY_FOLDER_PATH, CONVOY_HELPER_SCRIPT_FILENAME)

CONVOY_SERVICE_TEMPLATE_FILENAME = 'convoy.service.j2'
CONVOY_SERVICE_TEMPLATE_PATH = os.path.join(DATAFILES_FOLDER, CONVOY_SERVICE_TEMPLATE_FILENAME)
CONVOY_SERVICE_PATH = '/etc/systemd/system/convoy.service'
