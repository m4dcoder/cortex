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

import datetime
import unittest
import uuid

import sqlalchemy
from sqlalchemy.orm import sessionmaker

from cortex.models import base
from cortex.models import executions


DB_USER = 'brainiac'
DB_NAME = 'cortex'
DB_CONN_URL = 'cockroachdb://%s@localhost:26257/%s?sslmode=disable' % (DB_USER, DB_NAME)

"""
DB_CONN_URL_SECURED = (
    'cockroachdb://brainiac@localhost:26257/cortex?'
    'sslcert=%2Fpath%2Fto%2Fcockroachdb%2Fcerts%2Fclient.brainiac.crt&'
    'sslkey=%2Fpath%2Fto%2Fcockroachdb%2Fcerts%2Fclient.brainiac.key&'
    'sslmode=verify-full&'
    'sslrootcert=%2Fpath%2Fto%2Fcockroachdb%2Fcerts%2Fca.crt'
)
"""


class DatabaseSetupTest(unittest.TestCase):
    engine = None

    @classmethod
    def setUpClass(cls):
        super(DatabaseSetupTest, cls).setUpClass()
        cls.engine = sqlalchemy.create_engine(DB_CONN_URL)

    @classmethod
    def tearDownClass(cls):
        cls.engine.dispose()
        super(DatabaseSetupTest, cls).tearDownClass()

    def tearDown(self):
        base.clear_db(self.engine)
        super(DatabaseSetupTest, self).tearDown()

    def test_setup(self):
        base.setup_db(self.engine)

        ex_id = uuid.uuid4().hex
        timestamp = datetime.datetime.utcnow()
        result = {'a': 123}

        entry = executions.ActionExecution(
            id=ex_id,
            created_at=timestamp,
            result=result
        )

        maker = sessionmaker(bind=self.engine)
        session = None

        try:
            session = maker()
            session.add_all([entry])
            session.commit()

            rows = session.query(executions.ActionExecution).count()
            self.assertEqual(int(rows), 1)

            record = session.query(executions.ActionExecution).one()
            self.assertEqual(record.id, ex_id)
            self.assertEqual(record.created_at, timestamp)
            self.assertDictEqual(record.result, result)
        finally:
            if session:
                session.close()
