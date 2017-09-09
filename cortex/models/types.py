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

import json
import sqlalchemy as sa
import sys


class JsonEncoded(sa.TypeDecorator):
    impl = sa.UnicodeText

    def process_bind_param(self, value, dialect):
        value = json.dumps(value) if value else None

        # In python 3, str is unicode by default.
        # For python 2.x, convert the string to unicode.
        if sys.version_info[0] < 3:
            value = value.decode('utf-8')

        return value

    def process_result_value(self, value, dialect):
        return json.loads(value) if value else None
