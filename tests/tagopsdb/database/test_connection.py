# Copyright 2016 Ifwe Inc.
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

import unittest2


class TestConnections(unittest2.TestCase):

    def setUp(self):
        self.protocol = 'mysql+pymysql'
        self.db_user = 'testuser'
        self.db_password = 'testpw'
        self.hostname = 'opsdb.tagged.com'
        self.db_name = 'TagOpsDB'

    @unittest2.skip('not currently valid')
    def test_create_dbconn_string(self):
        from tagopsdb.database import create_dbconn_string

        params = dict(hostname=self.hostname, db_name=self.db_name)
        dbconn_string = create_dbconn_string(self.db_user, self.db_password,
                                             **params)
        expect_str = (
            self.protocol + '://' + self.db_user + ':' +
            self.db_password + '@' + self.hostname + '/' +
            self.db_name
        )
        self.assertEquals(dbconn_string, expect_str)
