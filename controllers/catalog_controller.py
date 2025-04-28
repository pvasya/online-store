from core.controller import BaseController
from models.goods import Goods, GoodsDAO
from models.basket import BasketDAO
from urllib.parse import unquote

def index(req):
    ctrl = BaseController(req)
    goods = GoodsDAO().get_all()
    basket_counts = {}
    if ctrl.user and not ctrl.user.is_admin:
        items = BasketDAO().get_active_by_user(ctrl.user.id)
        for it in items:
            basket_counts[it.goods_id] = basket_counts.get(it.goods_id, 0) + 1

    ctrl.render('catalog.html', {
        'user': ctrl.user,
        'goods': goods,
        'basket_counts': basket_counts
    })

def add_goods(req):
    ctrl = BaseController(req)
    data = ctrl.parse_form()
    name = data.get('name')
    url = data.get('url')
    image_url = unquote(url).lstrip('/')
    price = data.get('price')
    if name and url and price:
        goods = goods(None, name, image_url, int(price), False)
        GoodsDAO().create(goods)
    ctrl.redirect('/')

def delete_goods(req):
    ctrl = BaseController(req)
    data = ctrl.parse_form()
    id_ = data.get('id')
    if id_:
        GoodsDAO().delete(int(id_))
    ctrl.redirect('/')

def update_goods(req):
    ctrl = BaseController(req)
    data = ctrl.parse_form()
    id_ = data.get('id')
    name = data.get('name')
    url = data.get('url')
    image_url = unquote(url).lstrip('/')
    price = data.get('price')
    if id_ and name and url and price:
        goods = Goods(int(id_), name, image_url, int(price), False)
        GoodsDAO().update(goods)
    ctrl.redirect('/')
