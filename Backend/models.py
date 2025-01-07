from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Existing User, Role, UserRoles Models
# UserRoles Table
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    # username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String, nullable=False)
    active = db.Column(db.Boolean, default=True)
    roles = db.relationship('Role', secondary='user_roles', backref='users', lazy='subquery')
    customer = db.relationship('Customer', backref='user', uselist=False)
    service_professional = db.relationship('ServiceProfessional', backref='user', uselist=False)

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=False)

class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    
# Model for Customer Table
class Customer(db.Model):
    # Specify the name of the table in the database
    __tablename__ = 'customers'
    
    # Define columns in the Customer table
    id = db.Column(db.Integer, primary_key=True)  # Primary key for the customer
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    username = db.Column(db.String(100), nullable=False)  # Customer's username
    email = db.Column(db.String(100), unique=True, nullable=False)  # Unique email for the customer
    password = db.Column(db.String(100), nullable=False)  # Password for the customer (hashed)
    address = db.Column(db.String(100), nullable=False)  # Address of the customer
    pincode = db.Column(db.Integer, nullable=False)  # Pincode of the customer's area
    mobile = db.Column(db.String(15), nullable=False)  # Mobile number of the customer
    status = db.Column(db.String(20), nullable=False, default='pending')  # Account status (pending, accepted, rejected)


    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'address': self.address,
            'pincode': self.pincode,
            'mobile': self.mobile,
            'status': self.status
        }

    # Predefined status options for easy reference
    STATUS_PENDING = "pending"
    STATUS_ACCEPTED = "accepted"
    STATUS_REJECTED = "rejected"
    
     # Establish relationship with ServiceRequest and enable cascade delete
    service_requests = db.relationship('ServiceRequest', backref='customer', lazy=True, cascade="all, delete-orphan")

    # String representation of the Customer object
    def __repr__(self):  
        return f"<Customer {self.id} - {self.username}>"

# Model for Service Professional Table
class ServiceProfessional(db.Model):
    __tablename__ = 'service_professionals'
    
    # Define columns for the service professional table
    id = db.Column(db.Integer, primary_key=True)  # Primary key for the service professional
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    username = db.Column(db.String(100), nullable=False)  # Username of the professional
    email = db.Column(db.String(120), unique=True, nullable=False)  # Email (must be unique)
    password = db.Column(db.String(128), nullable=False)  # Hashed password
    service_type = db.Column(db.String(100), nullable=False)  # Type of service they provide (e.g., plumber, electrician)
    experience = db.Column(db.Integer, nullable=False)  # Years of experience in the service industry
    pincode = db.Column(db.String(10), nullable=False)  # Pincode for the professional's service area
    address = db.Column(db.String(255), nullable=False)  # Full address of the professional
    resume_file_path = db.Column(db.String(255), nullable=True)  # Path to the professional's resume (optional)
    status = db.Column(db.String(20), nullable=False, default='pending')  # Status (pending, accepted, rejected)
    mobile_no = db.Column(db.String(15), nullable=False)  # Contact number of the professional
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'service_type': self.service_type,
            'experience': self.experience,
            'pincode': self.pincode,
            'address': self.address,
            'resume_file_path': self.resume_file_path if self.resume_file_path else None,
            'status': self.status,
            'mobile_no': self.mobile_no,
            'service_id': self.service_id
        }

    # Predefined status options for easy reference
    STATUS_PENDING = "pending"
    STATUS_ACCEPTED = "accepted"
    STATUS_REJECTED = "rejected"
    STATUS_CLOSED = "closed"  # Status for closed service requests
    
    # Establish a one-to-many relationship with the ServiceRequest model
    service_requests = db.relationship('ServiceRequest', backref='service_professional', lazy=True)

    def __repr__(self):  
        return f"<ServiceProfessional {self.username}>"

# Model for Service Table
class Service(db.Model):
    __tablename__ = 'services'  # Define table name in database
    
    # Define columns for the service table
    id = db.Column(db.Integer, primary_key=True)  # Primary key for the service
    name = db.Column(db.String(100), nullable=False)  # Name of the service (e.g., plumbing, cleaning)
    description = db.Column(db.Text, nullable=False)  # Description of the service
    base_price = db.Column(db.Float, nullable=False)  # Base price for the service

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.base_price
        }

    # One-to-many relationship with the ServiceRequest model (a service can have many requests)
    service_requests = db.relationship('ServiceRequest', backref='service', lazy=True, cascade="all, delete-orphan")


# Model for Service Request Table
class ServiceRequest(db.Model):
    __tablename__ = 'service_requests'  # Define the table name in database
    
    # Define columns for the service request table
    id = db.Column(db.Integer, primary_key=True)  # Primary key for the request
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=False)  # Foreign key linking to the Service table
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.user_id'), nullable=False)  # Foreign key linking to the Customer table
    professional_id = db.Column(db.Integer, db.ForeignKey('service_professionals.user_id'), nullable=True)  # Optional foreign key for the professional assigned to the request
    request_date = db.Column(db.DateTime, nullable=False)  # The date and time when the request was made
    status = db.Column(db.String(50), default="Pending")  # Status of the request (e.g., Pending, Accepted, Completed)
    rating = db.Column(db.Integer, nullable=True)  # Rating for the service (optional, may be null initially)
    remarks = db.Column(db.String(500), nullable=True)  # Remarks provided by the customer 

    def to_dict(self):
        return {
            'id': self.id,
            'service_id': self.service_id,
            'customer_id': self.customer_id,
            'professional_id': self.professional_id if self.professional_id else None,
            'request_date': self.request_date.strftime('%Y-%m-%d %H:%M:%S') if self.request_date else None,
            'status': self.status,
            'rating': self.rating if self.rating else None,
            'remarks': self.remarks if self.remarks else None
        }

      # Methods to change the status of the request (e.g., Accept, Reject, Close , remarks)
    def accept_request(self):
        self.status = "Accepted"
        db.session.commit()

    def reject_request(self):
        self.status = "Rejected"
        db.session.commit()

    def close_request(self):
        self.status = "Closed"
        db.session.commit()

    def set_rating(self, rating):
        self.rating = rating
        db.session.commit()

    def close_by_customer(self):
        self.status = "Closed by Customer"
        db.session.commit()

    # def close_by_professional(self):
    #     self.status = "Closed by Professional"
    #     db.session.commit()

    def set_remarks(self, remarks):
        self.remarks = remarks
        db.session.commit()

    # String representation of the ServiceRequest object
    def __repr__(self):  
        return f"<ServiceRequest {self.id} - {self.customer_id}>"