#!/usr/bin/env python

import os, sys, optparse
from threading import *
from subprocess import call
from passlib.hash import atlassian_pbkdf2_sha1

Found = False
maxThreads = 25
lock = BoundedSemaphore(value=maxThreads)

def testHash(p,h):
    global Found
    try:
        test = atlassian_pbkdf2_sha1.verify(p, h)
        if (test == True):
            print '[+] Password Found: ' + p
            Found = True
            exit(0)
        elif (test == False):
            lock.release()
    except (KeyboardInterrupt):
        print '[!] Exception / User cancelled!'

def main():
    global maxThreads
    call('clear')
    print 'Atlassian Password Finder ... '
    print 'This script is written to check passwords'
    print 'in a list against a compromised hash.'
    print ' '
    print 'Written by James Luther, TS13, Pentester\n'
    parser = optparse.OptionParser(usage = '%prog -l <password list> -p <password hash> -t <max threads>\n\n' +\
                                    'Hash must be in quotes "HASH"\n\n',
                                    version = '%prog Version 3.0\n\n' +\
                                    'We now have MULTITHREADING!\n')
    parser.add_option('-l','--list',dest='list',type='string',help='Path' +\
                        ' to Password List')
    parser.add_option('-p','--hash',dest='hash',type='string',help='Atla' +\
                        'ssian Password Hash')
    parser.add_option('-t','--threads',dest='threads',type='int',help='Ma' +\
                        'x Number of Threads')
    (options, args) = parser.parse_args()
    list = options.list
    hash = options.hash
    threads = options.threads
    if (list == None) | (hash == None):
        print parser.usage
        exit(0)
    if (threads != None):
        maxThreads = threads
    fn = open(list, 'r')
    for line in fn.readlines():
        if Found:
            print '[*] Exiting: Password Found!'
            exit(0)
        lock.acquire()
        password = line.strip('\r').strip('\n')
        os.write(1,'\r[-] Testing: ' + str(password) + '                  ')
        t = Thread(target=testHash, args=(password, hash))
        child = t.start()

if __name__ == "__main__":
    main()
