import http.server
import socketserver
import os

PORT = 8000
TEMPLATES_DIR = "templates"

class MyHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        routes = {
            "/": "index.html",
            "/index.html": "index.html",
            "/categories.html": "categories.html",
            "/orders.html": "orders.html",
            "/contacts.html": "contacts.html",
        }

        filepath = routes.get(self.path)
        if filepath:
            fullpath = os.path.join(TEMPLATES_DIR, filepath)
            if os.path.exists(fullpath):
                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                with open(fullpath, "r", encoding="UTF-8") as file:
                    self.wfile.write(file.read().encode("UTF-8"))
            else:
                self.send_error(404, "file not found")
        if self.path.startswith("/static/"):
            try:
                static_path = os.path.join("static", self.path[8:])
                if os.path.exists(static_path):
                    self.send_response(200)

                    if static_path.endswith(".css"):
                        self.send_header("Content-type", "text/css")

                    elif static_path.endswith(".svg"):
                        self.send_header("Content-type", "image/svg+xml")
                    else:
                        self.send_header("Content-type", "application/octet-stream")

                    self.end_headers()
                    mode = 'rb' if any(static_path.endswith(ext) for ext in ['.svg']) else 'r'
                    with open(static_path, mode) as file:
                        if 'b' in mode:
                            self.wfile.write(file.read())
                        else:
                            self.wfile.write(file.read().encode('utf-8'))
                    return
            except Exception as e:
                self.send_error(500, f"Ошибка сервера: {str(e)}")
                return

with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print(f"Сервер запущен на http://localhost:{PORT}")
    httpd.serve_forever()
