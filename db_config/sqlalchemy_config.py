import random
from flask_sqlalchemy import SQLAlchemy, SignallingSession, get_state
from sqlalchemy import orm


class Config:
    SQLALCHEMY_BINDS = {
        "m1": 'mysql://root:mysql@127.0.0.1:3306/test29',
        "m2": 'mysql://root:mysql@127.0.0.1:3306/test29',
        "s1": 'mysql://root:mysql@127.0.0.1:8306/test29',
        "s2": 'mysql://root:mysql@127.0.0.1:8306/test29',
    }
    SQLALCHEMY_CLUSTER = {
        "masters": ["m1", "m2"],
        "slaves": ['s1', 's2'],
        "default": 'm1'
    }
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False


class MySession(SignallingSession):
    def __init__(self, db, autocommit=False, autoflush=True, **options):
        SignallingSession.__init__(self, db, autocommit=autocommit, autoflush=autoflush, **options)
        self.default_key = db.default_key
        self.master_keys = db.master_keys if len(db.master_keys) else self.default_key
        self.slave_keys = db.slave_keys if len(db.slave_keys) else self.default_key
        self.bind_key = None


    def get_bind(self, mapper=None, clause=None):
        """获取会话使用的数据库连接engine"""
        state = get_state(self.app)

        if self.bind_key:
            # 指定
            print('Using DB bind: _name={}'.format(self.bind_key))
            return state.db.get_engine(self.app, bind=self.bind_key)
        else:
            # 默认数据库
            print('Using default DB bind: _name={}'.format(self.default_key))
            return state.db.get_engine(self.app, bind=self.default_key)

    def set_to_write(self):
        """使用写数据库"""
        self.bind_key = random.choice(self.master_keys)

    def set_to_read(self):
        """使用读数据库"""
        self.bind_key = random.choice(self.slave_keys)


class MySQLAlchemy(SQLAlchemy):
    def init_app(self, app):
        config_binds = app.config.get("SQLALCHEMY_BINDS")
        if not config_binds:
            raise RuntimeError('Missing SQLALCHEMY_BINDS config')

        cluster = app.config.get("SQLALCHEMY_CLUSTER")
        if not cluster:
            raise RuntimeError('Missing SQLALCHEMY_CLUSTER config')

        default_key = cluster.get('default')
        if not default_key:
            raise KeyError("deafult is not in SQLALCHEMY_CLUSTER")

        # 生成并保存数据库引擎
        self.master_keys = cluster.get("masters") or []
        self.slave_keys = cluster.get("slaves") or []
        self.default_key = default_key

        super(MySQLAlchemy, self).init_app(app)


    def create_session(self, options):
        return orm.sessionmaker(class_=MySession, db=self, **options)

