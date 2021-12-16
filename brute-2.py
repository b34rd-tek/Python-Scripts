#!/usr/bin/env python

import sys, optparse, os
import multiprocessing
from subprocess import *
from itertools import product

Found = False

def bruteCryptKey(password, drive):
    global Found
    try:
        result = call("echo " + "'" + password + "'" + " | " + "/sbin/cryptsetup luksOpen "
                      + drive + " encrypted" + " 2>/dev/null", shell=True)
        if result is 0:
            print '[!] Password Found: {0}'.format(password)
            Found = True
            sys.exit(0)
        elif result is not 0:
            pass
    except (KeyboardInterrupt):
        print '[*] User cancelled!'
    except Exception as e:
        print '[*] Unknown error has occured... {0}'.format(str(e))

def main():
    global maxThreads
    print '\nCryptSetup Brute Forcer'
    print 'This script will attempt to brute force luks passwords.'
    print 'It will take a LONG time to complete.\n'
    print 'Written by James Luther\n'
    parser = optparse.OptionParser(usage = '%prog -p <password length> -t ' +\
                                   '<max threads> -d <drive>\n\n', version = '%prog Vers' +\
                                   'ion 0.1\n\n')
    parser.add_option('-p', '--length', dest='length', type='int', help='' +\
                      'Integer for number of characters in password')
    parser.add_option('-t', '--threads', dest='threads', type='int', help='' +\
                      'Max number of threads.')
    parser.add_option('-d', '--drive', dest='drive', type='string', help='' +\
                      'Drive to run brute force against.')
    (options, args) = parser.parse_args()
    length = options.length
    threads = options.threads
    drive = options.drive
    if length is None and drive is None:
        print parser.usage
        sys.exit(0)
    if threads is not None:
        maxThreads = threads
    permutation = product('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*()',
                          repeat=length)
    p = ""
    jobs = []
    for p in permutation:
        if Found:
            print '[!] Exiting: Password Found!'
            sys.exit(0)
        p = "".join(p)
        p = p.strip('\r')
        os.write(1,'\r[-] Testing: ' + str(p))
        job = multiprocessing.Process(target=bruteCryptKey, args=(p, drive))
        jobs.append(job)
        job.start()

if __name__ == '__main__':
    main()
