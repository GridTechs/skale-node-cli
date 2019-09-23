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
from configs.node import HOME_DIR

LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

LOG_FILE_SIZE_MB = 300
LOG_FILE_SIZE_BYTES = LOG_FILE_SIZE_MB * 1000000

LOG_BACKUP_COUNT = 1
LOG_DATA_PATH = os.path.join(HOME_DIR, '.skale-cli-log')

LOG_FILENAME = 'node-cli.log'
DEBUG_LOG_FILENAME = 'debug-node-cli.log'
LOG_FILEPATH = os.path.join(LOG_DATA_PATH, LOG_FILENAME)
DEBUG_LOG_FILEPATH = os.path.join(LOG_DATA_PATH, DEBUG_LOG_FILENAME)
