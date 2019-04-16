#!/usr/bin/python3
# -*- coding: utf-8 -*-
import csv
import pexpect
import termcolor

def ssh_copy_id(csv_file):
    failed = termcolor.colored('[ FAILED ]', 'red')
    ok = termcolor.colored('[ OK ]', 'green')
    changed = termcolor.colored('[ CHANGED ]', 'yellow')
    with open(csv_file, 'r') as f:
        reader = csv.reader(f, delimiter=',', quotechar='"')
        for row in reader:
            target, user, password = row[0], row[1], row[2]
            pattern_list = [
                'continue connecting \(yes/no\)',
                "\'s password:",
                'WARNING: All keys were skipped because they already exist on the remote system.',
                'ERROR: ssh: Could not resolve hostname target: Temporary failure in name resolution',
                pexpect.exceptions.EOF,
                pexpect.exceptions.TIMEOUT,
            ]
            prc = pexpect.spawn("/usr/bin/ssh-copy-id {}@{}".format(user, target))
            index = prc.expect(pattern_list, timeout=10)
            if index == 0:
                prc.sendline('yes')
                prc.expect("\'s password:")
                prc.sendline(password)
                index = prc.expect([pexpect.exceptions.TIMEOUT], timeout=10)
                if index == 0:
                    print(failed, target)
                    print(prc.after)
                    continue
                prc.expect(pexpect.EOF)
                print(changed, target)
                print(prc.before)
            elif index == 1:
                prc.sendline(password)
                index = prc.expect([pexpect.exceptions.TIMEOUT], timeout=10)
                if index == 0:
                    print(failed, target)
                    print(prc.after)
                    continue
                prc.expect(pexpect.EOF)
                print(changed, target)
                print(prc.before)
            elif index == 2:
                print(ok, target)
                prc.expect(pexpect.EOF)
                print(prc.after)
            elif index == 3 or index == 4 or index == 5:
                print(failed, target)
                print(prc.after)
                prc.close()

if __name__ == '__main__':
    ssh_copy_id("hosts.csv")
