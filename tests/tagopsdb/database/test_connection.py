import unittest2

from tagopsdb.database import create_dbconn_string, init_session
from tagopsdb.database.meta import Session


class TestConnections(unittest2.TestCase):

    def setUp(self):
        self.protocol = 'mysql+oursql'
        self.db_user = 'testuser'
        self.db_password = 'testpw'
        self.hostname = 'opsdb.tagged.com'
        self.db_name = 'TagOpsDB'

    def test_create_dbconn_string(self):
        params = dict(hostname=self.hostname, db_name=self.db_name)
        dbconn_string = create_dbconn_string(self.db_user, self.db_password,
                                             **params)
        expect_str = self.protocol + '://' + self.db_user + ':' + \
                     self.db_password + '@' + self.hostname + '/' + \
                     self.db_name
        self.assertEquals(dbconn_string, expect_str)

    def test_get_connection(self):
        params = {}
        db_user = 'tagopsdb_reader'
        db_password = 'kitties'
        expect_str = 'Engine(' + self.protocol + '://' + db_user + ':' + \
                     db_password + '@' + self.hostname + '/' + \
                     self.db_name + ')'
        self.assertIsNone(init_session(db_user, db_password, **params))
        self.assertEquals(str(Session.get_bind()), expect_str)
