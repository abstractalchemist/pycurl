#!/usr/bin/env python

from httplib import HTTPConnection
import sys
import os
import os.path
import json
import pprint

if __name__ == '__main__':
   connection = HTTPConnection('localhost',9000)
   headers = { 'unix-name': ( os.environ['PORTAL_USER'] if 'PORTAL_USER' in os.environ else os.environ['USER']), 'application':'test' }
   if 'DATA' in os.environ:
      with open(os.environ['DATA']) as f:
         connection.request(os.environ['METHOD'] if 'METHOD' in os.environ else 'PUT', "/portal/delegate/rest/%s?filename=%s" % ((os.environ['URL'] if 'URL' in os.environ else 'portalfilemanager/files/tmp'), os.path.basename(os.environ['DATA'])), f, headers)
   elif 'BODY' in os.environ:
      headers['content-type'] = 'application/json'
      connection.request(os.environ['METHOD'] if 'METHOD' in os.environ else 'POST', "/portal/delegate/rest/%s" % (os.environ['URL'] if 'URL' in os.environ else ''), os.environ['BODY'], headers)
   else:
      connection.request(os.environ['METHOD'] if 'METHOD' in os.environ else 'GET', "/portal/delegate/rest/%s" % (os.environ['URL'] if 'URL' in os.environ else ''), None, headers)
   response = connection.getresponse()
   if response != None:
      if response.status != 200:
         print("responses was %s on %s reason %s" % (response.status, os.environ['URL'] if 'URL' in os.environ else '', response.reason))
         sys.exit(255)
      if filter((lambda a : a[0] == 'content-type' and a[1] == 'application/json'), response.getheaders()):
         pprint.pprint(json.loads(response.read()))

      elif filter((lambda a : a[0] == 'content-type' and a[1] == 'application/octet-stream' or a[0] == 'content-disposition'), response.getheaders()):
         sys.stdout.write(response.read())
      else:
         print('Content-type undetected')
         print(response.getheaders())
   else:
      sys.exit(255)
   connection.close()
   sys.exit(0)
 
