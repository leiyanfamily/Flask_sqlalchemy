from flask import Flask
import pymysql
from db_config import db
from db_config.decorator import set_write_db, set_read_db
from db_config.sqlalchemy_config import Config

pymysql.install_as_MySQLdb()

# 创建app应用
app = Flask(__name__)
app.config.from_object(Config)

# 初始化数据库连接对象
db.init_app(app)

# 建立映射模型
class User(db.Model):
   __tablename__ = 'tb_user'
   id = db.Column(db.Integer, primary_key=True)
   name = db.Column(db.String(20), unique=True)
   age = db.Column(db.Integer)


@app.route('/')
@set_write_db
def index():
    """增加数据"""
    user1 = User(name='xiao', age=20)
    db.session.add(user1)
    db.session.commit()

    return "index"


@app.route('/demo1')
@set_read_db
def demo1():
    try:
        # 查询数据
        users = User.query.all()
        print(users)
    except Exception as e:
        return "查询错误:{}".format(e)
    return 'demo1'


if __name__ == '__main__':
    # db.drop_all()  # 删除所有继承自db.Model的表
    # db.create_all()  # 创建所有继承自db.Model的表
    app.run(debug=True)