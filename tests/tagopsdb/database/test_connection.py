import unittest2


class TestConnections(unittest2.TestCase):

    def setUp(self):
        self.protocol = 'mysql+oursql'
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
