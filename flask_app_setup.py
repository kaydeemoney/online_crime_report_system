from flask import Flask, render_template, request, redirect, url_for, session, flash
from models import db, User, Report, Admin
from config import Config
import uuid

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/report', methods=['GET', 'POST'])
def report():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        anon = request.form.get('anonymous')
        if anon:
            anon_id = str(uuid.uuid4())
            new_user = User(anonymous_id=anon_id)
        else:
            email = request.form['email']
            name = request.form['name']
            ministry = request.form['ministry']
            new_user = User(email=email, name=name, ministry=ministry)
        db.session.add(new_user)
        db.session.commit()
        new_report = Report(title=title, description=description, user_id=new_user.id)
        db.session.add(new_report)
        db.session.commit()
        if anon:
            return redirect(url_for('follow_up_detail', anon_id=anon_id))
        else:
            flash('Report submitted successfully.')
            return redirect(url_for('index'))
    return render_template('report.html')

@app.route('/follow_up', methods=['GET', 'POST'])
def follow_up():
    if request.method == 'POST':
        tracking_id = request.form['tracking_id']
        user = User.query.filter_by(anonymous_id=tracking_id).first()
        if user:
            return redirect(url_for('follow_up_detail', anon_id=tracking_id))
        else:
            flash('Invalid tracking ID')
    return render_template('follow_up.html')

@app.route('/follow_up_detail/<anon_id>')
def follow_up_detail(anon_id):
    user = User.query.filter_by(anonymous_id=anon_id).first()
    reports = user.reports if user else []
    return render_template('follow_up_detail.html', reports=reports)

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        admin = Admin.query.filter_by(email=email).first()
        if admin and admin.password == password:  # Direct comparison without g
            session['admin_id'] = admin.id
            session['admin_level'] = admin.level
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid credentials')
    return render_template('admin_login.html')

@app.route('/admin_dashboard')
def admin_dashboard():
    if 'admin_id' not in session:
        return redirect(url_for('admin_login'))
    level = session['admin_level']
    if level == 1:
        reports = Report.query.filter_by(status='unreviewed').all()
    elif level == 2:
        reports = Report.query.filter_by(status='reviewed by admin 1').all()
    else:
        reports = []
    return render_template('admin_dashboard.html', reports=reports)

@app.route('/report_detail/<report_id>', methods=['GET', 'POST'])
def report_detail(report_id):
    report = Report.query.get(report_id)
    if request.method == 'POST':
        verdict = request.form['verdict']
        level = session['admin_level']
        if level == 1:
            report.status = 'reviewed by admin 1'
        elif level == 2:
            report.status = 'final verdict given'
        db.session.commit()
        return redirect(url_for('admin_dashboard'))
    return render_template('report_detail.html', report=report)

if __name__ == '__main__':
    app.run(debug=True)
