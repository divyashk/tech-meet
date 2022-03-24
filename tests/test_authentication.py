import unittest

import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, '../webapp')

import app

class TestUser(unittest.TestCase):
    ''' Test authentication functions written '''

    def test_is_user_id_valid(self):
        valid = app.is_user_id_valid("hello")
        assert(valid == True)

    def test_role_string(self):
        role = app.role_string(0)
        assert(role == "patient")

        role = app.role_string(1)
        assert(role == "doctor")

        role = app.role_string(2)
        assert(role == "hospital")
        
        role = app.role_string(2)
        assert(role != "")


    def test_user_points_update(self):
        pass

    def test_user_level_change(self):
        pass

if __name__ == '__main__':
    unittest.main()
