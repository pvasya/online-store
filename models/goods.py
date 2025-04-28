from core.dao_base import DAOBase

class Goods:
    def __init__(self, id, name, image_url, price, is_deleted):
        self.id = id
        self.name = name
        self.image_url = image_url
        self.price = price
        self.is_deleted = is_deleted

class GoodsDAO(DAOBase):
    def get_all(self):
        query = """
            SELECT id, name, url, price, is_deleted
            FROM Goods
            WHERE NOT is_deleted
            ORDER BY id
        """
        self.cur.execute(query)
        return [Goods(*row) for row in self.cur.fetchall()]

    def find_by_id(self, id_):
        query = """
            SELECT id, name, url, price, is_deleted
            FROM Goods
            WHERE id = %s AND NOT is_deleted
        """
        self.cur.execute(query, (id_,))
        row = self.cur.fetchone()
        return Goods(*row) if row else None

    def create(self, Goods):
        query = """
            INSERT INTO Goods (name, url, price, is_deleted)
            VALUES (%s, %s, %s, FALSE)
            RETURNING id
        """
        self.cur.execute(query, (Goods.name, Goods.image_url, Goods.price))
        new_id = self.cur.fetchone()[0]
        self.commit()
        return new_id

    def delete(self, Goods_id):
        query = "UPDATE Goods SET is_deleted = TRUE WHERE id = %s"
        self.cur.execute(query, (Goods_id,))
        self.commit()

    def update(self, Goods):
        query = """
            UPDATE Goods
            SET name = %s, url = %s, price = %s
            WHERE id = %s
        """
        self.cur.execute(query, (Goods.name, Goods.image_url, Goods.price, Goods.id))
        self.commit()
