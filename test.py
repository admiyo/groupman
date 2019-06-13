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


    def test_parse_groups(self):
        manager = groupman.parse_group_file("build/group")
        self.assertEqual(5, len(manager.groups))
        self.assertEqual('admins', manager.group_by_name['admins'].name )
        self.assertEqual('test', manager.group_by_id['5000'].name )
        self.assertEqual(2, len(manager.group_by_name['admins'].users))


if __name__  == '__main__':
  unittest.main()


