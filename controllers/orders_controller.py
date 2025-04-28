from core.controller import BaseController
from models.order import Order, OrderDAO
from models.basket import BasketDAO
from models.goods import GoodsDAO
from models.user import UserDAO
from core.logger import logger

def view_orders(req):
    ctrl = BaseController(req)
    if not ctrl.require_login():
        return

    display = []
    if ctrl.user.is_admin:
        raw = OrderDAO().get_all()
        for o in raw:
            u = UserDAO().get_by_id(o.user_id)
            display.append({'order': o, 'username': u.username})
    else:
        raw = OrderDAO().get_by_user(ctrl.user.id)
        for o in raw:
            display.append({'order': o})

    ctrl.render('orders.html', {'user': ctrl.user, 'orders': display})

def create_order(req):
    ctrl = BaseController(req)
    if not ctrl.require_login() or ctrl.user.is_admin:
        ctrl.redirect('/')
        return

    items = BasketDAO().get_active_by_user(ctrl.user.id)
    counts = {}
    for it in items:
        counts[it.goods_id] = counts.get(it.goods_id, 0) + 1

    parts = []
    total = 0
    for gid, qty in counts.items():
        goods = GoodsDAO().find_by_id(gid)
        if goods:
            parts.append(f"{qty} - {goods.name}")
            total += goods.price * qty
    goods_str = ', '.join(parts)

    new_order = Order(None, ctrl.user.id, goods_str, total, True)
    OrderDAO().create(new_order)

    BasketDAO().clear(ctrl.user.id)
    logger.info(f"User {ctrl.user.username} created an order: {goods_str}")
    ctrl.redirect('/orders')

def complete_order(req):
    ctrl = BaseController(req)
    if not ctrl.require_login() or not ctrl.user.is_admin:
        ctrl.redirect('/')
        return
    data = ctrl.parse_form()
    oid = data.get('id')
    if oid:
        OrderDAO().complete(int(oid))
    ctrl.redirect('/orders')