import hashlib

import time
from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.ext.declarative import declared_attr, as_declarative
from sqlalchemy.orm import relationship, sessionmaker


@as_declarative()
class Base(object):
    id = Column(Integer, primary_key=True, autoincrement=True)

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    @classmethod
    def new(cls, **kwargs):
        session.add(cls(**kwargs))
        session.commit()
        return cls.find_one(**kwargs)

    @classmethod
    def all(cls):
        return session.query(cls).all()

    @classmethod
    def _find_by(cls, **kwargs):
        return session.query(cls).filter_by(**kwargs)

    @classmethod
    def find_by(cls, **kwargs):
        return cls._find_by(**kwargs).all()

    @classmethod
    def find_one(cls, **kwargs):
        return cls._find_by(**kwargs).first()

    @classmethod
    def delete_one(cls, **kwargs):
        cls._find_by(**kwargs).delete()
        session.commit()

    @classmethod
    def update_one(cls, **kwargs):
        id = int(kwargs.get('id'))
        b = cls._find_by(id=id)
        b.update(values=kwargs)
        session.commit()
        return b.one()

    def __repr__(self):
        classname = self.__class__.__name__
        properties = ['{}: ({})'.format(k, v) for k, v in self.__dict__.items() if k != '_sa_instance_state']
        s = '|'.join(properties)
        return '< {}- {} >'.format(classname, s)

    def json(self):
        d = self.__dict__
        if '_sa_instance_state' in d:
            d.pop('_sa_instance_state')
        return d

    @classmethod
    def find_to_json(cls, **kwargs):
        bs = cls.find_by(**kwargs)
        jsons = [b.json() for b in bs]
        return jsons

    @classmethod
    def all_json(cls):
        bs = cls.all()
        jsons = [b.json() for b in bs]
        return jsons


class Session(Base):
    sid = Column(String(120))
    user_id = Column(Integer, ForeignKey('user.id'))


class Todo(Base):
    task = Column(String(20), nullable=False)
    status = Column(String(20), default='未完成')
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User', back_populates='todos')
    created_time = Column(Integer, default=0)

    @classmethod
    def new(cls, **kwargs):
        kwargs['created_time'] = int(time.time())
        session.add(cls(**kwargs))
        session.commit()
        return cls.find_one(**kwargs)


class User(Base):
    username = Column(String(20), unique=True, nullable=False)
    password = Column(String(120), default='123456')

    @classmethod
    def validate_register(cls, form):
        username = form.get('username')
        password = form.get('password')
        u = cls.find_by(username=username)
        print('register u', u)
        if not u and len(username) > 2 and len(password) > 2:
            form['password'] = cls.salted_password(password)
            cls.new(**form)
            return True
        else:
            return False

    @classmethod
    def validate_login(cls, form):
        print('login form', form)
        username = form.get('username')
        password = form.get('password')
        print('all user', cls.all())
        u = cls.find_one(username=username)
        print('login u', u)
        if u is not None and u.password == cls.salted_password(password):
            print('登录成功')
            return u
        else:
            print('登录失败')
            return None

    @staticmethod
    def salted_password(password, salt='$d<?-[u*&^'):
        salted = password + salt
        hash = hashlib.sha256(salted.encode('ascii'))
        return hash.hexdigest()


User.todos = relationship('Todo', order_by=Todo.id, back_populates='user', cascade="all, delete, delete-orphan")

engine = create_engine('mysql+mysqlconnector://root:password@localhost:3306/test')

# 初始化数据库连接:
# Base.metadata.drop_all(bind=engine)
# Base.metadata.create_all(bind=engine)

# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)
# 创建session对象:
session = DBSession()
