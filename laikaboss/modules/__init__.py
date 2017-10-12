# Copyright 2015 Lockheed Martin Corporation
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# 
import os
import syslog
import traceback
import sys
import logging
from laikaboss.objectmodel import QuitScanException, \
                                GlobalScanTimeoutError, GlobalModuleTimeoutError

# This block of code looks for all py files in the current directory
# and imports the class with the same name (except uppercase) as the file.
# This ensures that the dispatcher can access every _module in this folder without
# any further configuration needed.


def log_debug(message):
    syslog.syslog(syslog.LOG_DEBUG, "DEBUG %s" % message)

for _module in os.listdir(os.path.dirname(__file__)):
    try:
        if _module == '__init__.py' or _module[-3:] != '.py':
            continue
        _temp = __import__(_module[:-3], locals(), globals(), [_module[:-3].upper()], -1)
        globals()[_module[:-3].upper()] = getattr(_temp, _module[:-3].upper())
    except (QuitScanException, GlobalScanTimeoutError, GlobalModuleTimeoutError):
        raise
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        logging.exception("Import Exception for %s _module: %s" % (_module, repr(traceback.format_exception(exc_type, exc_value, exc_traceback))))
        log_debug("Import Exception for %s _module: %s" % (_module, repr(traceback.format_exception(exc_type, exc_value, exc_traceback))))
        continue
del _module
del _temp
