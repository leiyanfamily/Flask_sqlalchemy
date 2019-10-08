# Flask_sqlalchemy
基于Flask-sqlalchemy的MySQL读写分离
    sqlalchemy 没有实现读写分离,需要自定义实现
    读写分离的核心在于重写session的get_bind()方法
        自定义一个Session类,继承默认的Session
        重写get_bind()方法
        自定义SQLAlchemy类,继承SQLAlchemy类
        重写create_session()方法