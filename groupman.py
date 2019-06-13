#!/usr/bin/python3


def parse_group_file(path):    
    fd = open(path,"rt")
    groups=[]

    while(True):
        line = fd.readline()
        if line == '\n':
            break
        group = Group(line)
        groups.append(group)
    fd.close()
    return GroupMan(groups)

class Group(object):
    def __init__(self, line):
        data = line.split(':')
        self.name=data[0]
        self.password=data[1]
        self.gid=data[2]
        self.users=data[3].split('\n')[0].split(',')
          

class GroupMan():
    def __init__(self, groups):
        self.group_by_name = dict()
        self.group_by_id = dict()
        for group in groups:
            self.group_by_name[group.name] = group
            self.group_by_id[group.gid] = group
        self.groups = groups 


def main():
    print("Hello")
    return 0

if __name__  == '__main__':
  main()


