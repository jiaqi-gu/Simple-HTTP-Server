#!/usr/bin/python

"""
This program is a simple threaded HTTP server, and it allows users to download files through HTTP connection.
To run the server: Python HttpServer [port]. Python 3 is required. This program is tested on Python 3.4.
For testing locally, enter http://localhost:[port]/, and you will all all files available for download.
Or enter http://localhost:[port]/[filename] to download the file.
The default folder is ./files/

Author: Jiaqi Gu
"""

# Import
import http.server
import socketserver
import json
import mimetypes
import os
import sys
import urllib.request, urllib.parse, urllib.error

# Global variables
FilePath = "files/"
Host = ""

class HTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    """
    The request handler class for HTTP server. It is instantiated for each connection to the server.
    """
    
    # Response to a HTTP GET request
    def do_GET(self):
        # Parse the input, and the full path and name
        query = urllib.parse.splitquery(self.path)
        path = urllib.parse.unquote_plus(query[0])
        fn = urllib.parse.unquote_plus(FilePath + path).replace("/",os.sep)

        # Send header to the client
        self.send_response(200)
        self.send_header("content-type","text/html")
        content = ""
        
        # Determine if the client requests a folder or a file
        if os.path.isdir(fn):
            # Form the content of files and folders in HTML
            contentFolders = "<table>"
            contentFileNames = "<table>"
            # Iterate all files and folders, and form HTML elements
            for filename in os.listdir(fn):
                if filename[0] != ".":
                    filepath = "%s%s%s" % (fn, os.sep, filename)
                    if os.path.isdir(filepath):
                        filename += os.sep
                        contentFolders += """\n <tr><td valign="top"> <img src="http://www.apache.org/icons/dir.png" alt="[FOLDER]"> <a href="%s%s%s">%s</a> </td></tr>""" % (Host, path, filename, filename)
                    else:
                        contentFileNames += """\n <tr><td valign="top"> <img src="http://www.apache.org/icons/generic.png" alt="[FILE]"> <a href="%s%s%s">%s</a> </td></tr> """ % (Host, path, filename, filename)
            # Encode the output stream
            content = bytes("<h1>File System<h1>"+contentFolders+"</table>"+contentFileNames+"</table>", "utf-8")
            self.send_header("content-type","text/html")
        elif os.path.isfile(fn):
            # If the client request a file, send the 
            f = open(fn, "rb")
            content = f.read()
            f.close()
            contenttype,_ = mimetypes.guess_type(fn)
            if contenttype:
                self.send_header("content-type",contenttype)
        else:
            # If the file or folder does not exist
            print((FilePath, path, fn))
            # Encode the output stream
            content = bytes("<h1>404 Not Found<h1>", "utf-8")
            self.send_header("content-type","text/html")

        # End of the header, and send the output stream back to the client
        http.server.BaseHTTPRequestHandler.end_headers(self)
        self.wfile.write(content)
        

class ThreadedHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    """
    This mix-in class is for creating the custom HTTP server binding ThreadingMixIn to HTTPServer
    """
    pass

# This is the main of the program
if __name__=="__main__":
    # Check the number of arguments. Only one optional argument is allowed.
    if len(sys.argv)>2:
        print("Usage: Python HttpServer.py [port]")

    # Default port. Port can be changed via argument.
    port = 8080
    if len(sys.argv)==2:
        port = int(sys.argv[1])
    Host = "http://localhost:%s/" % (port)
    
    # Set up server
    server_address = ("localhost", port)
    server = ThreadedHTTPServer(("localhost", port), HTTPRequestHandler)
    print("Server listens at port:", port)
    
    # Run the server
    while(True):
        # Handle only one request
    	server.handle_request()
    	# Uncomment request_queue_size to specify the size of the request queue 
    	#server.request_queue_size(10)
