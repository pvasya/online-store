from core.view import render_template
from core.session import load_session

class BaseController:
    def __init__(self, request_handler):
        self.req = request_handler
        self.user = load_session(request_handler)

    def render(self, template_name, context=None, status=200):
        render_template(self.req, template_name, context or {}, status)

    def redirect(self, location):
        self.req.send_response(302)
        self.req.send_header('Location', location)
        self.req.end_headers()

    def parse_form(self):
        length = int(self.req.headers.get('Content-Length', 0))
        data = self.req.rfile.read(length).decode('utf-8')
        return dict(pair.split('=') for pair in data.split('&') if '=' in pair)

    def require_login(self):
        if not self.user:
            self.redirect('/login')
            return False
        return True