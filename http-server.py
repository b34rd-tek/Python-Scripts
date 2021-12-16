#!/usr/bin/env python

import sys, BaseHTTPServer, ssl, os, optparse
from OpenSSL import crypto, SSL
from socket import gethostname
from time import gmtime, mktime
from os.path import exists, join
from SimpleHTTPServer import SimpleHTTPRequestHandler as HandlerClass

ServerClass = BaseHTTPServer.HTTPServer
Protocol = "HTTP/1.0"
CERT_FILE = 'python-server.crt'
KEY_FILE = 'python-server.key'
startdir = None
port = None
dir = None

def create_cert(cert_dir):
    if not exists(join(cert_dir, CERT_FILE)) or not exists (join(cert_dir, KEY_FILE)):
        k = crypto.PKey()
        k.generate_key(crypto.TYPE_RSA, 1024)
        cert = crypto.X509()
        cert.get_subject().C = 'US'
        cert.get_subject().ST = 'Maryland'
        cert.get_subject().L = 'City'
        cert.get_subject().O = 'my company'
        cert.get_subject().OU = 'my org'
        cert.get_subject().CN = gethostname()
        cert.set_serial_number(1000)
        cert.gmtime_adj_notBefore(0)
        cert.gmtime_adj_notAfter(10*365*24*60*60)
        cert.set_issuer(cert.get_subject())
        cert.set_pubkey(k)
        cert.sign(k, 'sha1')
        open(join(cert_dir, CERT_FILE), "wt").write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
        open(join(cert_dir, KEY_FILE), "wt").write(crypto.dump_privatekey(crypto.FILETYPE_PEM, k))

def http_server(port):
    print '[-] Attempting to start HTTP server on ' + str(port) + '\n'
    try:
        if (dir != None):
            os.chdir(dir)
        server_address = ('0.0.0.0', port)
        HandlerClass.protocol_version = Protocol
        httpd = ServerClass(server_address, HandlerClass)
        sa = httpd.socket.getsockname()
        print '[+] Serving up some HTTP on', sa[0], 'Port:', sa[1], '...'
        httpd.serve_forever()
    except (KeyboardInterrupt):
        print '\n[!] User exit ... '
    except Exception, e:
        print '[!] ' + str(e)

def https_server(port, cert, key):
    cert = startdir + '/' + cert
    key = startdir + '/' + key
    print '[-] Attempting to start HTTPS server on ' + str(port) + '\n'
    try:
        server_address = ('0.0.0.0', port)
        HandlerClass.protocol_version = Protocol
        httpd = ServerClass(server_address, HandlerClass)
        sa = httpd.socket.getsockname()
        httpd.socket = ssl.wrap_socket(httpd.socket, keyfile=key, certfile=cert, server_side=True, do_handshake_on_connect=True)
        print '[+] Serving up some HTTPS on', sa[0], 'Port:', sa[1], '...'
        if (dir != None):
            os.chdir(dir)
        httpd.serve_forever()
    except (KeyboardInterrupt):
        os.remove(cert)
        os.remove(key)
        print'\n[!] User exit ...'
    except Exception, e:
        os.remove(cert)
        os.remove(key)
        print '[!] ' + str(e)

def main():
    global port
    global dir
    global startdir
    print 'Simple HTTP Server'
    print 'This script will start a simple http server hosted'
    print 'from the directory in which it is started.\n'
    parser = optparse.OptionParser(usage='%prog -p <port number> -s (turn on ssl) -d <directory to serve>\n', version='%prog version 0.5\n\nNow with SSL!\n')
    parser.add_option('-p','--port',dest='port',type='int',help='Specified port to listen.')
    parser.add_option('-s','--ssl', dest='ssl',action='store_true',default=False,help='Turn on SSL')
    parser.add_option('-d','--dir',dest='dir',type='string',help='Directory to start server')
    (options, args) = parser.parse_args()
    port = options.port
    if (port == None):
        print '[+] Using default port of 8000'
        port = 8000
    if (options.dir != None):
        dir = options.dir
    if (options.ssl == False):
        http_server(port)
    elif (options.ssl == True):
        startdir = os.getcwd()
        create_cert(startdir)
        https_server(port, CERT_FILE, KEY_FILE)
    else:
        print parser.usage

if __name__ == '__main__':
    main()
