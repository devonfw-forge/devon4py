from settings import Session

session = Session()


# Se crea la clase BaseModelMixin con métodos de utilidad para los modelos.
class BaseModelMixin:
    def create(self):
        session.add(self)
        session.commit()
    def delete(self):
        session.delete(self)
        session.commit()
    @classmethod
    def update(cls, dc, *args):
        session.query(cls).filter(*args).update(dc)
        session.commit()
    @classmethod
    def get_all(cls):
        return session.query(cls).all()
    @classmethod
    def get_by_id(cls, id):
        return session.query(cls).get(id)
    @classmethod
    def get_by(cls, param):
        return session.query(cls).get(param)
    # @classmethod
    # def simple_filter(cls, **kwargs):
    #     return cls.query.filter_by(**kwargs).all()
    @classmethod
    def filter(cls, *args):
        return session.query(cls).filter(*args)
    @classmethod
    def filter_all(cls, *args):
        return session.query(cls).filter(*args).all()
    @classmethod
    def filter_first(cls, *args):
        return session.query(cls).filter(*args).first()
    @classmethod
    def commit(cls):
        session.commit()