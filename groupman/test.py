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
        copyfile("data/group", "build/group")

    def test_parse_groups(self):
        manager = groupman.parse_group_file("build/group")
        self.assertEqual(5, len(manager.groups))
        self.assertEqual('admins', manager.group_by_name['admins'].name)
        self.assertEqual('test', manager.group_by_id['5000'].name)
        self.assertEqual(2, len(manager.group_by_name['admins'].users))

    def test_add(self):
        group = groupman.Group("groupname:x:1:init")
        self.assertEqual(1, len(group.users))
        group.exec_line("+newval")
        self.assertEqual(2, len(group.users))

    def test_remove(self):
        group = groupman.Group("groupname:x:1:init")
        self.assertEqual(1, len(group.users))
        group.exec_line("-init")
        self.assertEqual(0, len(group.users))

    def test_group_to_string(self):
        group = groupman.Group("groupname:x:1:init")
        str_val = group.to_string()
        self.assertEqual("groupname:x:1:init", str_val)

    def test_group_add_to_string(self):
        group = groupman.Group("groupname:x:1:init")
        group.exec_line("+newval")
        str_val = group.to_string()
        self.assertEqual("groupname:x:1:init,newval", str_val)

    def test_group_remove_to_string(self):
        group = groupman.Group("groupname:x:1:init,newval")
        group.exec_line("-newval")
        str_val = group.to_string()
        self.assertEqual("groupname:x:1:init", str_val)

    def test_group_add_duplicate_to_string(self):
        group = groupman.Group("groupname:x:1:init,newval")
        group.exec_line("+newval")
        str_val = group.to_string()
        self.assertEqual("groupname:x:1:init,newval", str_val)

    def test_manager_to_string(self):
        group = groupman.Group("groupname:x:1:init")
        manager = groupman.GroupMan([group])
        self.assertEqual(1, len(manager.groups))
        str_val = manager.to_string()
        self.assertEqual("groupname:x:1:init\n", str_val)


if __name__ == '__main__':
    unittest.main()
