from app import db

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	nickname = db.Column(db.String(64), index=True, unique=True)
	password = db.Column(db.String(64))
	posts = db.relationship('Post', backref='author', lazy='dynamic', cascade='all, delete-orphan')
	comments = db.relationship('Comment', backref='author', lazy='dynamic', cascade='all, delete-orphan')

	def __repr__(self):
		return 'nickname: ' + self.nickname

	@property
	def is_authenticated(self):
		return True

	@property
	def is_active(self):
		return True

	@property
	def is_anonymous(self):
		return False

	def get_id(self):
		try:
			return unicode(self.id)
		except NameError:
			return str(self.id)  # python 3

class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(64))
	timestamp = db.Column(db.DateTime)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	comments = db.relationship('Comment', backref='post', lazy='dynamic', cascade='all, delete-orphan') 

	def __repr__(self):
		return 'title: ' + self.title + ', id: ' + str(self.id)

class Comment(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
	content = db.Column(db.String(64))

	def __repr__(self):
		return 'id: ' + str(self.id) + ', title: ' + self.content