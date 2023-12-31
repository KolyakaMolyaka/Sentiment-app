from src.app.ext.database import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(128), nullable=False, unique=True)
	password = db.Column(db.Text(), nullable=False)
	is_admin = db.Column(db.Boolean, default=False)

	def __repr__(self):
		return f'<User: username={self.username}>'

	def set_password(self, password):
		self.password = generate_password_hash(password)

	def check_password(self, password):
		""" Проверка, совпадает ли переданный пароль с настоящим """
		return check_password_hash(self.password, password)

	def save(self):
		""" Запись изменений пользователя в БД """
		db.session.add(self)
		db.session.commit()
