#!/usr/bin/python3

from os import unlink
from os import mkdir
from shutil import copyfile

import groupman

def assertTrue(value):
    if not value:
        raise value



def setUp():
    try:
        mkdir("build", 0o755)  
    except FileExistsError:
        pass
    try:
        unlink("build/group")
    except FileNotFoundError:
        pass
    copyfile("data/group","build/group")


def test():
    test_parse()
    test_parse_groups()
    print('ok')

def test_parse():
     records = groupman.parse_file()

     assert(len(records) == 5 )
     assert(records['admins']['group'] == 'admins')
     assert(len(records['admins']['users']) == 2)

def test_parse_groups():
     manager = groupman.parse_group_file("build/group")


def tearDown():
    pass

def main():
    setUp()
    test()
    tearDown()
    return 0

if __name__  == '__main__':
  main()


