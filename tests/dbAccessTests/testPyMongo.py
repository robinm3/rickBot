import unittest

from application.dbAccess.pyMongo import setInDB, getInDB, findInDB, deleteFromDB, findAllInDB


class TestPyMongo(unittest.TestCase):
    """
    Tests methods for accessing and modifying database
    """

    def test_setValueInDB(self):
        """
        tests getInDB
        """
        setInDB(0, {"name": "Joe"})
        self.assertEqual("Joe", getInDB(0, "name"), "Should be Joe")

    def test_getNonExistentValue(self):
        """
        tests getInDB to see if it returns false for non existent key
        """
        self.assertFalse(getInDB(0, "nonExistentKey"), "key doesn't exist")

    def test_findInDB(self):
        """
        tests setInDB, findInDB and deleteFromDB
        """
        setInDB(0, {"name": "Joe"})
        self.assertTrue(findInDB(0), "is in db")
        deleteFromDB(1)
        self.assertFalse(findInDB(1), "is not in db anymore")

    def test_deleteFromDB(self):
        """
        tests setInDB, deleteFromDB and getInDB
        """
        setInDB(0, {"name": "Joe"})
        self.assertTrue(getInDB(0, "name"), "is in db")
        deleteFromDB(0)
        self.assertFalse(getInDB(0, "name"), "is not in db anymore")

    def test_givenKeyAndValue_findAllInDB(self):
        """
        tests setInDB, deleteFromDB and getInDB
        """
        setInDB(0, {"potatoe": "Joe"})
        setInDB(1, {"potatoe": "meh"})
        setInDB(2, {"potatoe": None})
        peopleFound = findAllInDB("potatoe", "meh")
        self.assertEqual(1, (peopleFound[0]).get('_id'))
        deleteFromDB(0)
        deleteFromDB(1)
        deleteFromDB(2)


if __name__ == '__main__':
    unittest.main()
