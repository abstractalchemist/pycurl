#!/usr/bin/env python

from httplib import HTTPConnection
import sys
import os
import json
import pprint

if __name__ == '__main__':
   connection = HTTPConnection('localhost',9000)
   headers = { 'unix-name': ( os.environ['PORTAL_USER'] if 'PORTAL_USER' in os.environ else os.environ['USER']), 'application':'test' }
   if 'DATA' in os.environ:
      with open(os.environ['DATA']) as f:
         connection.request(os.environ['METHOD'] if 'METHOD' in os.environ else 'PUT', "/portal/delegate/rest/%s?filename=%s" % ((os.environ['URL'] if 'URL' in os.environ else 'portalfilemanager/files/tmp'), os.environ['DATA']), f, headers)
   else:
      connection.request(os.environ['METHOD'] if 'METHOD' in os.environ else 'GET', "/portal/delegate/rest/%s" % (os.environ['URL'] if 'URL' in os.environ else ''), None, headers)
   response = connection.getresponse()
   if response != None:
      if response.status != 200:
         print("responses was %s" % response.status)
         sys.exit(255)
      if filter((lambda a : a[0] == 'content-type' and a[1] == 'application/json'), response.getheaders()):
         pprint.pprint(json.loads(response.read()))
         sys.exit(0)
      else:
         print('Content-type undetected')
         print(response.getheaders())
         print(response.read())
   else:
      sys.exit(255)
 
