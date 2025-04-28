from core.dao_base import DAOBase

class Order:
    def __init__(self, id, user_id, goods, total_price, is_active):
        self.id = id
        self.user_id = user_id
        self.goods = goods
        self.total_price = total_price
        self.is_active = is_active

class OrderDAO(DAOBase):
    def get_all(self):
        query = """
            SELECT id, user_id, goods, total_price, is_active
            FROM orders
            ORDER BY id DESC
        """
        self.cur.execute(query)
        return [Order(*row) for row in self.cur.fetchall()]

    def get_by_user(self, user_id):
        query = """
            SELECT id, user_id, goods, total_price, is_active
            FROM orders
            WHERE user_id = %s
            ORDER BY id DESC
        """
        self.cur.execute(query, (user_id,))
        return [Order(*row) for row in self.cur.fetchall()]

    def create(self, order):
        query = """
            INSERT INTO orders (user_id, goods, total_price, is_active)
            VALUES (%s, %s, %s, TRUE)
            RETURNING id
        """
        self.cur.execute(query, (order.user_id, order.goods, order.total_price))
        new_id = self.cur.fetchone()[0]
        self.commit()
        return new_id

    def complete(self, order_id):
        query = "UPDATE orders SET is_active = FALSE WHERE id = %s"
        self.cur.execute(query, (order_id,))
        self.commit()
