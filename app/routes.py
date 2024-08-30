from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app import db
from app.models import ReportReview, User, Report
import uuid

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')


@main.route('/about')
def about():
    return render_template('about.html')



@main.route('/faq')
def faq():
    return render_template('faq.html')


@main.route('/contact')
def contact():
    return render_template('contact.html')



@main.route('/services')
def services():
    return render_template('services.html')


@main.route('/index_report')
def index_report():
    return render_template('index_report.html')


@main.route('/police_details')
def police_details():
    return render_template('police_details.html')

@main.route('/about_us')
def about_us():
    return render_template('about_us.html')


@main.route('/y_report')
def y_report():
    return render_template('y_report.html')

@main.route('/rt')
def rt():
    return render_template('rt.html')





@main.route('/report', methods=['GET', 'POST'])
def report():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        is_anonymous = 'is_anonymous' in request.form

        if is_anonymous:
            user = User(is_anonymous=True)
        else:
            email = request.form.get('email')
            name = request.form.get('name')
            department = request.form.get('department')
            user = User(email=email, name=name, department=department, is_anonymous=False)

        db.session.add(user)
        db.session.commit()

        tracking_id = str(uuid.uuid4())
        report = Report(title=title, description=description, user_id=user.id, tracking_id=tracking_id)
        db.session.add(report)
        db.session.commit()

        flash(f'Your report has been submitted. Your tracking ID is {tracking_id}. Please save this ID to follow up on your report.', 'success')
        return redirect(url_for('main.index_report'))

    return render_template('report.html')

@main.route('/follow_up', methods=['GET', 'POST'])
def follow_up():
    if request.method == 'POST':
        tracking_id = request.form['tracking_id']
        report = Report.query.filter_by(tracking_id=tracking_id).first()

        if report:
            review = ReportReview.query.filter_by(tracking_id=tracking_id).first()
            admin1_verdict = review.admin1_verdict if review else None
            admin2_verdict = review.admin2_verdict if review else None
            return render_template('follow_up_results.html', report=report, admin1_verdict=admin1_verdict, admin2_verdict=admin2_verdict)
        else:
            flash('Invalid tracking ID.', 'danger')
            return redirect(url_for('main.follow_up'))

    return render_template('follow_up.html')




@main.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email, is_admin=1).first()

        if user and user.verify_password(password):
            session['admin_id'] = user.id
            session['admin_level'] = user.admin_level
            return redirect(url_for('main.admin_dashboard'))

        return render_template('admin_login.html', error='Invalid credentials')

    return render_template('admin_login.html')


@main.route('/admin_dashboard')
def admin_dashboard():
    if 'admin_id' not in session:
        return redirect(url_for('main.admin_login'))

    admin_level = session.get('admin_level', 0)
    reports = Report.query.all()
    return render_template('admin_dashboard.html', admin_level=admin_level, reports=reports)

@main.route('/review/<int:report_id>', methods=['GET', 'POST'])
def review_report(report_id):
    if 'admin_id' not in session:
        return redirect(url_for('main.admin_login'))

    report = Report.query.get_or_404(report_id)
    admin_level = session.get('admin_level', 0)

    if request.method == 'POST':
        review_text = request.form['review']
        tracking_id = report.tracking_id

        # Check if a review record already exists
        review_record = ReportReview.query.filter_by(tracking_id=tracking_id).first()

        if not review_record:
            review_record = ReportReview(tracking_id=tracking_id)

        if admin_level == 1:
            review_record.admin1_verdict = review_text
            report.status = "reviewed by admin 1"
        elif admin_level == 2:
            review_record.admin2_verdict = review_text
            report.status = "reviewed by admin 2"

        db.session.add(review_record)
        db.session.commit()

        return redirect(url_for('main.admin_dashboard'))

    return render_template('review_report.html', report=report, admin_level=admin_level)
