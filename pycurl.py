#!/usr/bin/python2

from httplib import HTTPConnection
import sys
import os
import os.path
import json
import pprint

# Configuration Variables
# API_PORT      - the port that the api is listening on
# API_HOST      - the host that the api is listening on
# METHOD        - the httpd method to use
# DATA          - a path to a file to use as the body for the http request
# BODY          - a string to send as the body for the http request
# URL           - the portal rest url to place the request.  It should be the path after /portal/delegate/rest/$URL
# PORTAL_USER   - the portal user to send the request as.  By default, it uses the running user



if __name__ == '__main__':
   host = os.environ['API_HOST'] if 'API_HOST' in os.environ else 'localhost'
   port = int(os.environ['API_PORT']) if 'API_PORT' in os.environ else 9000
   connection = HTTPConnection(host, port)
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
#         print("response headers %s" % response.getheaders())
         chunk=1048576
         read_chunk=response.read(chunk)
         while read_chunk != None and len(read_chunk) > 0:
            sys.stdout.write(read_chunk)
            read_chunk=response.read(chunk)
      else:
         print('Content-type undetected')
         print(response.getheaders())
   else:
      sys.exit(255)
   connection.close()
   sys.exit(0)
 
