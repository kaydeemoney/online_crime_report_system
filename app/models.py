from app import db

class ReportReview(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tracking_id = db.Column(db.String(36), db.ForeignKey('report.tracking_id'), nullable=False)
    admin1_verdict = db.Column(db.Text, nullable=True)
    admin2_verdict = db.Column(db.Text, nullable=True)
    report = db.relationship('Report', backref=db.backref('reviews', lazy=True))

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    name = db.Column(db.String(120), nullable=True)
    department = db.Column(db.String(120), nullable=True)
    is_anonymous = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)
    admin_level = db.Column(db.Integer, default=0)

    def set_password(self, password):
        self.password = password

    def verify_password(self, password):
        return self.password == password

class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    tracking_id = db.Column(db.String(36), unique=True, nullable=False)
    status = db.Column(db.String(50), default='unreviewed')


