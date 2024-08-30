import sys
from app import db, create_app
from app.models import User

def main(email, name, admin_level, password):
    app = create_app()
    app.app_context().push()

    # Create the admin user with the plain text password
    admin = User(email=email, name=name, department='IT', is_admin=True, admin_level=admin_level)
    admin.set_password(password)  # Assuming the set_password method allows plain text passwords

    # Add the admin to the session and commit to the database
    db.session.add(admin)
    db.session.commit()

    print('Admin user created successfully.')

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python script.py <email> <name> <admin_level> <password>")
        sys.exit(1)

    email = sys.argv[1]
    name = sys.argv[2]
    try:
        admin_level = int(sys.argv[3])
    except ValueError:
        print("Admin level must be an integer.")
        sys.exit(1)
    password = sys.argv[4]

    main(email, name, admin_level, password)
