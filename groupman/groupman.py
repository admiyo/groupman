#!/usr/bin/python3
import os

def parse_group_file(path):
    fd = open(path, "rt")
    groups = []

    while(True):
        line = fd.readline()
        if line == '\n':
            break
        group = Group(line)
        groups.append(group)
    fd.close()
    return GroupMan(groups)


def write_group_file(groupman, path):
    fd = open(path, "wt")
    fd.write(groupman.to_string())
    fd.close()


class Group(object):
    def __init__(self, line):
        data = line.split(':')
        self.name = data[0]
        self.password = data[1]
        self.gid = data[2]
        self.users = set()
        if len(data) < 4:
            return
        user_line = data[3].split('\n')
        if len(user_line) > 0:
            for user in user_line[0].split(','):
                self.users.add(user)

    def exec_line(self, line):
        if len(line) < 2:
            return
        op = line[0]
        user = line[1:]
        if op == '+':
            self.users.add(user)
        elif op == '-':
            try:
                self.users.remove(user)
            except KeyError:
                pass

    def to_string(self):
        str_val = "%s:%s:%s:" % (self.name, self.password, self.gid)
        separator = ""
        for user in sorted(self.users):
            str_val = str_val + separator + user
            separator = ","
        return str_val


class GroupMan():
    def __init__(self, groups):
        self.group_by_name = dict()
        self.group_by_id = dict()
        for group in groups:
            self.group_by_name[group.name] = group
            self.group_by_id[group.gid] = group
        self.groups = groups

    def to_string(self):
        out = ""
        for key in sorted(self.group_by_id.keys()):
            out = out + self.group_by_id[key].to_string() + "\n"
        return out

    def parse_exec_file(self, execdir, groupname):
        group = self.group_by_name.get(groupname)
        if group is None:
            return
        path = execdir + "/" + groupname
        fd = open(path, "rt")
        for line in fd.readlines():
            group.exec_line(line.strip())
        fd.close()

    def exec_files(self, execdir):
        for r, d, f in os.walk(execdir):
            for file in f:
                self.parse_exec_file(execdir, file)

def execute(groupfile, execdir):
    manager = parse_group_file(groupfile)
    manager.exec_files(execdir)
    write_group_file(manager, groupfile)

    
def main():
    print("Hello")
    return 0

if __name__ == '__main__':
    main()
