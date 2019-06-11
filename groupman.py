#!/usr/bin/python3


def parse_file():
    fd = open("build/group","rt")
    groups=dict()

    while(True):
        line = fd.readline()
        if line == '\n':
            break
        record = parse_line(line)
        groups[record['group']] = record
    return groups

def parse_line(line):
    data = line.split(':')
    group=data[0]
    password=data[1]
    gid=data[2]
    users=data[3].split('\n')[0].split(',')

    record = {
         'group': group,
         'gid': gid,
         'password': password,
         'users': users
    }
    return record


def parse_group_file(path):
    fd = open(path,"rt")
    groups=[]

    while(True):
        line = fd.readline()
        if line == '\n':
            break
        group = Group(line)
        groups.append(group)

class Group(object):
    def __init__(self, line):
        data = line.split(':')
        self.name=data[0]
        self.password=data[1]
        self.gid=data[2]
        self.users=data[3].split('\n')[0].split(',')
          

class GroupMan():

    def __init__(self, groups):
        self.groups = groups 


def main():
    print("Hello")
    return 0

if __name__  == '__main__':
  main()


