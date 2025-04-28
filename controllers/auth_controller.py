from core.controller import BaseController
from core.session import set_session, clear_session
from models.user import UserDAO
from core.logger import logger
import bcrypt

def show_login(req):
    ctrl = BaseController(req)
    if ctrl.user:
        ctrl.redirect('/')
        return
    ctrl.render('login.html')

def login(req):
    ctrl = BaseController(req)
    data = ctrl.parse_form()
    username = data.get('username', '')
    password = data.get('password', '')

    user = UserDAO().find_by_username(username)
    if user and not user.is_blocked:
        pw_bytes = password.encode('utf-8')
        stored_hash = user.password_hash.encode('utf-8')
        if bcrypt.checkpw(pw_bytes, stored_hash):
            handler = ctrl.req
            handler.send_response(302)
            set_session(handler, user)
            handler.send_header('Location', '/')
            handler.end_headers()
            logger.info(f"User {user.username} login successfully.")
            return

    logger.warning(f"Anonymous login attempt with username: {username}")
    ctrl.render('login.html', {'error': 'Wrong username or password'}, 401)
    
def logout(req):
    ctrl = BaseController(req)
    handler = ctrl.req
    handler.send_response(302)
    clear_session(handler)
    handler.send_header('Location', '/')
    handler.end_headers()
    logger.info(f"User {ctrl.user.username} logout successfully.")
