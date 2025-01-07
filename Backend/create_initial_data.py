from flask import current_app as app  # Access the current app context

def create_initial_data():
    """
    Create initial roles and users for the application.
    """
    # Ensure the app context is pushed before interacting with the database
    with app.app_context():
        from Backend.models import db, Role, User  # Import database models

        # Create all tables in the database
        db.create_all()

        # Check and create roles if they don't already exist
        if not Role.query.filter_by(name='admin').first():
            admin_role = Role(name='admin', description='superadmin')
            db.session.add(admin_role)
        else:
            admin_role = Role.query.filter_by(name='admin').first()

        if not Role.query.filter_by(name='Customer').first():
            customer_role = Role(name='Customer', description='normal user')
            db.session.add(customer_role)
        else:
            customer_role = Role.query.filter_by(name='Customer').first()

        if not Role.query.filter_by(name='ServiceProfessional').first():
            professional_role = Role(name='ServiceProfessional', description='service professional')
            db.session.add(professional_role)
        else:
            professional_role = Role.query.filter_by(name='ServiceProfessional').first()

        # Check and create users if they don't already exist
        if not User.query.filter_by(email='parveen@gmail.com').first():
            admin_user = User(
                email='parveen@gmail.com',
                password='saroha123',  # Hashing should be handled during model definition or elsewhere
                username="Parveen",
                roles=[admin_role]  # Assign the admin role
            )
            db.session.add(admin_user)

        if not User.query.filter_by(email='customer@gmail.com').first():
            customer_user = User(
                email='customer@gmail.com',
                password='customer123',  # Hashing should be handled during model definition or elsewhere
                username="Customer",
                roles=[customer_role]  # Assign the customer role
            )
            db.session.add(customer_user)

        if not User.query.filter_by(email='service@gmail.com').first():
            service_user = User(
                email='service@gmail.com',
                password='service123',  # Hashing should be handled during model definition or elsewhere
                username="Service Professional",
                roles=[professional_role]  # Assign the service professional role
            )
            db.session.add(service_user)

        # Commit changes to the database to persist the data
        db.session.commit()
        print("Initial data creation successful.")
