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

    def test_end_to_end(self):
        manager = groupman.parse_group_file("build/group")
        before =  manager.group_by_name["admins"].to_string()
        self.assertEqual("admins:x:1000:anne,prithi", before)
        manager.exec_files("data/group.d")
        after =  manager.group_by_name["admins"].to_string()
        self.assertEqual("admins:x:1000:adam,anne", after)

    def test_execute(self):
        group_file = "build/group"

        fd = open(group_file, "rt")
        before =  fd.readlines()
        fd.close()
        
        manager = groupman.execute(group_file, "data/group.d")

        fd = open(group_file, "rt")
        after =  fd.readlines()
        fd.close()
        num_lines = len(before)
        self.assertEqual(num_lines, len(after))
        for i in range(num_lines):
            before_line = before[i]
            after_line = after[i]
            if before_line.startswith("admins"):
                assertEqual('admins:x:1000:anne,prithi\n', before_line)
                assertEqual('admins:x:1000:adam,anne\n', after_line)
            else:
                assertEqual(before_line, after_line)
        

if __name__ == '__main__':
    unittest.main()
