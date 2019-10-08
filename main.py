from flask import Flask
import pymysql
pymysql.install_as_MySQLdb()

# 创建app应用
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:mysql@127.0.0.1:3306/test29'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
# 初始化数据库连接对象
db.init_app(app)

# 建立映射模型
class User(db.Model):
   __tablename__ = 'tb_user'
   id = db.Column(db.Integer, primary_key=True)
   name = db.Column(db.String(20), unique=True)
   age = db.Column(db.Integer)


@app.route('/')
def index():
    """增加数据"""
    user1 = User(name='laowang', age=20)
    db.session.add(user1)
    db.session.commit()

    return "index"


@app.route('/demo1')
def demo1():
    # 查询数据
    users = User.query.all()
    print(users)
    return 'demo1'


if __name__ == '__main__':
    # db.drop_all()  # 删除所有继承自db.Model的表
    db.create_all()  # 创建所有继承自db.Model的表
    app.run(debug=True)