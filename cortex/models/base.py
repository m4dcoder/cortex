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

from sqlalchemy.ext import declarative


BaseModel = declarative.declarative_base()


def setup_db(engine):
    # Automatically create the tables based on the models.
    BaseModel.metadata.create_all(engine)


def clear_db(engine):
    # Automatically drop all the tables based on the models. Ensure database
    # sessions are closed otherwise the operation will be blocked.
    BaseModel.metadata.drop_all(engine)
