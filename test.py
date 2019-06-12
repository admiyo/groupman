#!/usr/bin/python3

from os import unlink
from os import mkdir
from shutil import copyfile
import unittest

import groupman


class TestGroupManager(unittest.TestCase):
    def setUp(self):
        try:
            mkdir("build", 0o755)  
        except FileExistsError:
            pass
        try:
            unlink("build/group")
        except FileNotFoundError:
            pass
        copyfile("data/group","build/group")

    def test_parse(self):
        records = groupman.parse_file()
        self.assertEqual(5, len(records))
        self.assertEqual('admins', records['admins']['group'] )
        self.assertEqual(2, len(records['admins']['users']))

    def test_parse_groups(self):
        manager = groupman.parse_group_file("build/group")


if __name__  == '__main__':
  unittest.main()


