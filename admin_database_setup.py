from app import create_app, db
from app.models import User

# Create the Flask application
app = create_app()

# Use the application context
with app.app_context():
    # Create admin level 1 user
    admin1 = User(email='admin1@example.com', name='Admin Level 1', department='IT', is_admin=True, admin_level=1)
    admin1.set_password('password1')
    db.session.add(admin1)

    # Create admin level 2 user
    admin2 = User(email='admin2@example.com', name='Admin Level 2', department='IT', is_admin=True, admin_level=2)
    admin2.set_password('password2')
    db.session.add(admin2)

    # Commit the changes
    db.session.commit()

    print("Admin users created successfully")
