#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
import csv
import pexpect

def ssh_copy_id(csv_file):
    with open(csv_file, 'r') as f:
        reader = csv.reader(f, delimiter=',', quotechar='"')
        for row in reader:
            target, user, password = row[0], row[1], row[2]
            prc = pexpect.spawn("/usr/bin/ssh-copy-id {}@{}".format(user, target))
            return_code = prc.expect(['continue connecting \(yes/no\)', '\'s password:', pexpect.EOF], timeout=20)
            if return_code == 0:
                print(type(return_code))
                prc.sendline('yes')
                prc.expect("\'s password:")
                prc.sendline(password)
                prc.expect(pexpect.EOF)
                print(prc.after, prc.before)
            elif return_code == 1:
                prc.sendline(password)
                prc.expect(pexpect.EOF)
                print(prc.after, prc.before)
            elif return_code == 2:
                print('[ FAILED ]')
                print(prc.after, prc.before)
                prc.close()
            # prc.logfile = sys.stdout

ssh_copy_id("hosts.csv")
