from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
import threading

class SimpleRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)

        # Parse the POST data
        parsed_data = parse_qs(post_data.decode('utf-8'))

        # Print the received data
        print(f"Received POST data on {self.server.server_port}: {parsed_data}")

        # Send a response to the client
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'OK')

def run_server(port):
    server_address = ('', port)
    httpd = HTTPServer(server_address, SimpleRequestHandler)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    # Run two instances on different ports
    port_1 = 8080
    port_2 = 8081

    # Use threading to run both servers concurrently
    thread_1 = threading.Thread(target=run_server, args=(port_1,))
    thread_2 = threading.Thread(target=run_server, args=(port_2,))

    thread_1.start()
    thread_2.start()

    thread_1.join()
    thread_2.join()
