import SimpleHTTPServer
import SocketServer
import os


class httpserver:

	def __init__(self,directory):
		
		print ("--- HTTP SERVER STARTED ---")
		PORT = int(os.environ.get("PORT", 8000))
		print PORT		
		
		os.chdir(os.path.join(os.path.abspath(os.curdir),directory))

		Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
		Handler.extensions_map.update({'.webapp': 'application/x-web-app-manifest+json',});

		httpd = SocketServer.TCPServer(("", PORT), Handler)

		httpd.serve_forever()
