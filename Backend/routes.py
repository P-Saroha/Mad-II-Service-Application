from flask import current_app as app, jsonify, render_template, request , session  ,send_file
from Backend.models import db, User, Role, UserRoles, ServiceProfessional,Customer, Service , ServiceRequest
import os 
import json
from datetime import datetime
from werkzeug.utils import secure_filename 
from flask_jwt_extended import JWTManager
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_restful import Api, Resource,reqparse
from sqlalchemy.exc import IntegrityError
from flask import send_from_directory
from sqlalchemy.orm import joinedload
from Backend.celery.tasks import add, create_csv
from celery.result import AsyncResult
from sqlalchemy import func  # Import for using SQLAlchemy functions

cache = app.cache

api = Api(app)
jwt = JWTManager(app)

@app.get('/celery')
def celery():
    task = add.delay(10, 20)
    return {'task_id' : task.id}

@jwt_required()
@app.get('/get-csv/<id>')
def getCSV(id):
    result = AsyncResult(id)

    if result.ready():
        return send_file(f'./Backend/celery/user-downloads/{result.result["professional_file"]}'), 200

    else:
        return {'message' : 'task not ready'}, 405
    
@jwt_required()
@app.get('/create-csv')
def createCSV():
    task = create_csv.delay()
    print(task)
    return {'task_id' : task.id}, 200

# cache routes
# @app.get('/cache')
# @cache.cached(timeout = 5)
# def cache():
#     return { 'time' : str(datetime.now()),}

@app.route('/clear_cache', methods=['POST'])
def clear_cache():
    cache.clear()
    return jsonify({'message': 'Cache cleared successfully'}),200

@app.get('/protected')
@jwt_required()
def protected():
    return '<h1> only accessible by auth user</h1>'


# Home route
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    """
    Login route to authenticate users based on role.
    """
    data = request.get_json()

    # Extract email, password, and role from the request data
    email = data.get('email')
    password = data.get('password')
    role = data.get('role')
    
    if not email or not password or not role:
        return jsonify({"message": "Invalid inputs"}), 400

    # Query the user by role and email
    if role == "Customer":
        customer = Customer.query.filter_by(email=email).first()
        if customer and customer.status == "rejected":
            # If the customer is rejected, still allow login (continue to the dashboard)
            return jsonify({"message": "Your account has been blocked. Please contact support for more information."}), 404
        
    elif role == "ServiceProfessional":
        service_professional = ServiceProfessional.query.filter_by(email=email).first()
        if service_professional and service_professional.status == "rejected":
            # If the service professional is rejected, still allow login (continue to the dashboard)
            return jsonify({"message":"Your account has been blocked. Please contact support for more information."}), 404
        
    # Query the user based on email (User should be found for both role types)
    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({"message": "Invalid email"}), 404

    
    if user.password == password:  
        identity = {'email': user.email, 'id': user.id, 'role': role}
        
        # Generate a token for the user
        token = create_access_token(identity=json.dumps(identity))  # Pass identity as a string

        return jsonify({
            'token': token,
            'email': user.email,
            'role': role,  # The role passed during login
            'id': user.id
        }), 200

    return jsonify({'message': 'Password is incorrect'}), 400


# ############# Register route ####################################
@app.route('/register', methods=['GET'])

def register():
    return jsonify({"message": "Redirect handled by frontend"}), 200



# Allowed file extensions for resume uploads
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}

# Function to check if the file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/service_professional_signup', methods=['POST'])
def service_professional_signup():
    if request.method == 'POST':
        data = request.form.to_dict()
        
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        service_id = data.get('service_id')
        service_type = Service.query.get(service_id).name
        experience = data.get('experience')
        pincode = data.get('pincode')
        address = data.get('address')
        mobile_no = data.get('mobile_no')
        resume_file = request.files.get('resume_file')  # Handling the file upload

        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

        resume_path = None
        if resume_file and allowed_file(resume_file.filename):
            filename = secure_filename(resume_file.filename)
            resume_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            resume_file.save(resume_path)  # Save the uploaded file

        # Check if username already exists
        if ServiceProfessional.query.filter_by(username=username).first():
            return jsonify({"message": "Username already exists. Please choose a different one."}), 400

        # Check if email already exists
        if ServiceProfessional.query.filter_by(email=email).first():
            return jsonify({"message": "Email already exists. Please use a different email."}), 400

        
        password = (password) #generate_password_hash
        
        # Step 1: Create a User
        if not User.query.filter_by(email=email).first(): 
            user = User(email=email, password=password)
            db.session.add(user)
            db.session.commit()

        user = User.query.filter_by(email=email).first()

        # Create new service professional object
        new_professional = ServiceProfessional(user_id = user.id,
            username=username,
            email=email,
            password=password,
            service_id=service_id,
            service_type=service_type,
            experience=experience,
            pincode=pincode,
            address=address,
            status=ServiceProfessional.STATUS_PENDING,
            mobile_no=mobile_no,
            resume_file_path=resume_path  # Store the resume path in the database
        )

        db.session.add(new_professional)
        db.session.commit()

        # Generate JWT token for the new user
        token = create_access_token(identity={'username': username, 'id': new_professional.id, 'role': 'service_professional'})

        return jsonify({
            "success": True,
            "message": "Account created successfully! You can log in now.",
            "token": token
        }), 201

    # For GET requests, return available services
    services = Service.query.all()
    services_data = [{"id": service.id, "name": service.name} for service in services]
    return jsonify({"services": services_data}), 200

############ Customer Signup ###########################
@app.route('/customer_signup', methods=['POST'])
def create_customer_account():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    address = data.get('address')
    pincode = data.get('pincode')
    mobile = data.get('mobile')



    # Validate inputs
    if not all([username, email, password, address, pincode, mobile]):
        return jsonify({"success": False, "message": "All fields are required."}), 400

    # Check if username or email already exists
    if Customer.query.filter_by(username=username).first():
        return jsonify({"success": False, "message": "Username already exists."}), 400

    if Customer.query.filter_by(email=email).first():
        return jsonify({"success": False, "message": "Email already exists."}), 400
    

    if not User.query.filter_by(email=email).first(): 
        user = User(email=email, password=password)
        db.session.add(user)
        db.session.commit()

    user = User.query.filter_by(email=email).first()

    # Step 2: Create a Customer
    new_customer = Customer(user_id = user.id, username=username, email=email, password=password,
                            address=address, pincode=pincode, mobile=mobile)
    db.session.add(new_customer)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Account created successfully!",
    }), 201


############### Admin login #########################

# Simulated Superuser credentials
SUPERUSER_CREDENTIALS = {"Parveen": "saroha123"}

class AdminLogin(Resource):
    def post(self):
        """
        Handle admin login.
        Accepts JSON data with `username` and `password`.
        """
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        # Validate credentials
        if username in SUPERUSER_CREDENTIALS and SUPERUSER_CREDENTIALS[username] == password:
            # Generate JWT token for admin
            identity = {"username": username, "role": "Admin"}
            token = create_access_token(identity=json.dumps(identity))  # Pass identity as a string
            return {"message": "Login successful", "token": token}, 200
        else:
            return {"message": "Invalid username or password"}, 401



############# Admin Dashboard #########################



# Directory containing the resumes
RESUME_DIR = 'uploads'
@app.route('/serve_resume/<string:filename>')
def resume(filename):
    """
    Serves resume files from the uploads directory.
    """
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)



class AdminDashboard(Resource):
    @jwt_required()
    @cache.cached(timeout=50)
    def get(self):

        """
        Admin Dashboard Endpoint
        Retrieves services, service professionals, service requests, and customers data.
        """
        current_user = get_jwt_identity()

        # Fetch data (query all)
        services = [service.to_dict() for service in Service.query.all()]
        # print(services)
        professionals = [professional.to_dict() for professional in ServiceProfessional.query.all()]
        service_requests = [request for request in ServiceRequest.query.all()]
        # print(service_requests)
        customers = [customer.to_dict() for customer in Customer.query.all()]

        # Modify professionals to only include the filename for resume_file_path
        for professional in professionals:
            professional['resume_file_path'] = os.path.basename(professional['resume_file_path'])

        # Return the data as a JSON response
        return {
            "services": services,
            "professionals": professionals,

            "service_requests": [

                { "customer_name": Customer.query.filter_by(user_id=req.customer_id).first().username,
                 "professional_name": ServiceProfessional.query.filter_by(user_id=req.professional_id).first().username if req.professional_id else "",
                 "service_name" : ServiceProfessional.query.filter_by(user_id=req.professional_id).first().service_type if req.professional_id else "",
                 "request_date" : req.request_date.strftime("%Y-%m-%d"),
                 "status" : req.status,
                 "rating" : req.rating if req.rating else None,
                 "id" : req.id,
                } 
                for req in service_requests
            ],
            "customers": customers
        }, 200
    
# Create Service Resource
class CreateService(Resource):
    # @jwt_required()
    def post(self):
        """
        Handle creation of a new service.
        Accepts JSON data with `name`, `description`, and `base_price`.
        """
        # current_user = get_jwt_identity()  # Get current logged-in user

        data = request.get_json()
        
        name = data.get('name')
        description = data.get('description')
        base_price = data.get('base_price')

        if not name or not description or not base_price:
            return {"message": "Missing required fields"}, 400

        new_service = Service(name=name, description=description, base_price=base_price)

        try:
            db.session.add(new_service)
            db.session.commit()
            return {"message": f"Service '{name}' created successfully!"}, 201
        except IntegrityError:
            db.session.rollback()
            return {"message": "Service creation failed due to integrity issues."}, 500
        
# Fetch Service Details Resource
class GetService(Resource):
    @jwt_required()
    def get(self, service_id):
        """
        Fetch details of a specific service by ID.
        """
        service = Service.query.get_or_404(service_id)
        return {
            "id": service.id,
            "name": service.name,
            "description": service.description,
            "base_price": service.base_price,
        }, 200


# Get All Services Resource
class GetServices(Resource):
    def get(self):
        """
        Fetch all services from the database and return as a list of dictionaries.
        """
        try:
            # Query all services from the database
            services = Service.query.all()

            # Convert service objects to dictionaries
            services_list = [service.to_dict() for service in services]

            # Return the list of services
            return {"services": services_list}, 200
        except Exception as e:
            # Log and return error response in case of failure
            print(f"Error fetching services: {e}")
            return {"message": "Failed to fetch services."}, 500


# Edit Service Resource
class EditService(Resource):
    @jwt_required()
    def put(self, service_id):
        """
        Handle editing an existing service by ID.
        Accepts JSON data with name, description, and base_price.
        """
        current_user = get_jwt_identity()

        service = Service.query.get_or_404(service_id)

        data = request.get_json()
        service.name = data.get('name', service.name)
        service.description = data.get('description', service.description)
        service.base_price = data.get('base_price', service.base_price)

        try:
            db.session.commit()
            return {"message": f"Service '{service.name}' updated successfully!"}, 200
        except IntegrityError:
            db.session.rollback()
            return {"message": "Service update failed due to integrity issues."}, 500

# Delete Service Resource
class DeleteService(Resource):
    @jwt_required()
    def delete(self, service_id):
        """
        Handle deletion of an existing service by ID.
        """
        current_user = get_jwt_identity()

        service = Service.query.get_or_404(service_id)

        try:
            db.session.delete(service)
            db.session.commit()
            return {"message": f"Service '{service.name}' deleted successfully!"}, 200
        except IntegrityError:
            db.session.rollback()
            return {"message": "Failed to delete service due to integrity issues."}, 500

############ Admin handel Professional #####################################
class UpdateProfessionalStatus(Resource):
    @jwt_required()
    def put(self, professional_id):
        """
        Update the status of a service professional.
        Accepts JSON input with `status` (approved/rejected).
        """
        professional = ServiceProfessional.query.get_or_404(professional_id)
        data = request.get_json()
        new_status = data.get('status')

        if new_status not in ['approved', 'rejected']:
            return {"message": "Invalid status value. Allowed values: 'approved', 'rejected'."}, 400

        try:
            professional.status = new_status
            db.session.commit()
            return {"message": f"Professional status updated to {new_status.capitalize()}."}, 200
        except IntegrityError:
            db.session.rollback()
            return {"message": "Failed to update professional status due to database integrity issues."}, 500
        

class DeleteProfessional(Resource):
    @jwt_required()
    def delete(self, professional_id):
        """
        Delete a service professional by ID.
        """
        professional = ServiceProfessional.query.get_or_404(professional_id)

        try:
            db.session.delete(professional)
            db.session.commit()
            return {"message": f"Professional with ID {professional_id} deleted successfully."}, 200
        except IntegrityError:
            db.session.rollback()
            return {"message": "Failed to delete professional due to database integrity issues."}, 500

@app.route('/block_customer/<int:customer_id>', methods=['PUT'])
@jwt_required()  # Add JWT token validation for admin
def block_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if customer:
        customer.status = Customer.STATUS_REJECTED
        db.session.commit()
        return jsonify({"message": "Customer has been blocked successfully."}), 200
    else:
        return jsonify({"message": "Customer not found"}), 404
    
@app.route('/unblock_customer/<int:customer_id>', methods=['PUT'])
@jwt_required()  # Add JWT token validation for admin
def unblock_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if customer:
        customer.status = Customer.STATUS_ACCEPTED
        db.session.commit()
        return jsonify({"message": "Customer has been unblocked successfully."}), 200
    else:
        return jsonify({"message": "Customer not found"}), 404
    
@app.route('/delete_customer/<int:customer_id>', methods=['DELETE'])
@jwt_required()  # Add JWT token validation for admin
def delete_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if customer:
        # Deleting the customer will automatically delete related service requests due to cascade
        db.session.delete(customer)
        db.session.commit()
        return jsonify({"message": "Customer deleted successfully!"}), 200
    else:
        return jsonify({"message": "Customer not found!"}), 404

######################### Admin Search #########################
@app.route('/admin_search', methods=['POST'])
@jwt_required()  # Require a valid JWT for access
def admin_search():
    # Get the current admin identity from the JWT
    current_user = get_jwt_identity()

    # Get the search query and selected category from the request body
    data = request.get_json()
    search_query = data.get('search_query', '').strip()
    category = data.get('category')

    # Initialize empty lists to hold search results for each category
    service_requests = []
    customers = []
    professionals = []

    # Filter based on the selected category
    if category == 'service_requests':
        service_requests = ServiceRequest.query.filter(
            # Filter for matching customer username
            ServiceRequest.customer.has(Customer.username.ilike(f"%{search_query}%")) |
            # Filter for matching professional username
            ServiceRequest.service_professional.has(ServiceProfessional.username.ilike(f"%{search_query}%")) |
            # Filter for matching service name
            ServiceRequest.service.has(Service.name.ilike(f"%{search_query}%"))
        ).all()
        # Serialize results
        service_requests = [
            {
                "id": req.id,
                "customer_name": Customer.query.filter_by(user_id=req.customer_id).first().username,
                "professional_name": ServiceProfessional.query.filter_by(user_id=req.professional_id).first().username,
                "requested_date": req.request_date.strftime("%Y-%m-%d"),
                "service_name": ServiceProfessional.query.filter_by(user_id=req.professional_id).first().service_type,
                "rating": req.rating,
                "status": req.status,
            }
            for req in service_requests
        ]
    elif category == 'customers':
        customers = Customer.query.filter(Customer.username.ilike(f"%{search_query}%")).all()
        # Serialize results
        customers = [
            {
                "id": customer.id,
                "username": customer.username,
                "mobile": customer.mobile,
                "email": customer.email,
                "address": customer.address,
                "pincode": customer.pincode,
            }
            for customer in customers
        ]
    elif category == 'professionals':
        professionals = ServiceProfessional.query.filter(
            ServiceProfessional.username.ilike(f"%{search_query}%")
        ).all()
        # Serialize results
        professionals = [
            {
                "id": prof.id,
                "username": prof.username,
                "experience": prof.experience,
                "mobile_no": prof.mobile_no,
                "email": prof.email,
                "address": prof.address,
                "service_type": prof.service_type,
            }
            for prof in professionals
        ]

    # Return results as JSON
    return jsonify({
        "service_requests": service_requests,
        "customers": customers,
        "professionals": professionals,
        "category": category,
    }), 200

##########################  admin summary route ####################################
import matplotlib.pyplot as plt
import base64
from io import BytesIO

@app.route('/admin_summary', methods=['GET'])
@jwt_required()
def admin_summary():
    # Get the identity of the current user (optional if needed)
    current_user = get_jwt_identity()

# Query to get average rating for each service professional 
    avg_rating_query = (
        ServiceProfessional.query
        .join(ServiceRequest, ServiceProfessional.user_id == ServiceRequest.professional_id)
        .filter(ServiceRequest.rating.isnot(None))  # Only consider non-null ratings
        .group_by(ServiceProfessional.username)
        .with_entities(ServiceProfessional.username, func.avg(ServiceRequest.rating).label('avg_rating'))
        .all()
    )


    # Check the query result for debugging
    print("Avg Rating Query Result:", avg_rating_query)

    # Ensure the query is returning the correct data
    if not avg_rating_query:
        return jsonify({'message': 'No ratings found for service professionals.'}), 404

    # Correctly unpacking the query result into a dictionary
    avg_rating_dict = {}
    for result in avg_rating_query:
        try:
            professional = result[0]  # Username (Service Professional)
            avg_rating = result[1]    # Average Rating (should be a number)

            # Ensure the average rating is properly rounded to 2 decimal places
            avg_rating_dict[professional] = round(float(avg_rating), 2)

        except ValueError as e:
            # If an error occurs, log the error (useful for debugging)
            print(f"Error processing average rating for {result[0]}: {e}")
            avg_rating_dict[result[0]] = 'N/A'  # You can assign 'N/A' or some default value

    # Query to get the count of service requests by status
    status_counts_query = (
        db.session.query(ServiceRequest.status, func.count(ServiceRequest.id))
        .group_by(ServiceRequest.status)
        .all()
    )
    request_status_dict = {status: count for status, count in status_counts_query}

    # Populate the dictionary with service request statuses
    service_requests = ServiceRequest.query.all()
    status_dict = {'Closed': 0, 'Accepted': 0, 'Rejected': 0, 'Pending': 0}
    for service in service_requests:
        status_dict[service.status] += 1

    # Create a histogram using Matplotlib
    labels = list(status_dict.keys())
    values = list(status_dict.values())
    
    plt.figure(figsize=(8, 5))
    plt.bar(labels, values, color=['blue', 'orange', 'red'])
    plt.xlabel('Status')
    plt.ylabel('Count')
    plt.title('Service Request Status Summary')

    # Setting y-axis values to integer
    plt.yticks(range(0, max(values) + 1, 1))

    # Save the histogram to a BytesIO object
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    
    # Convert the BytesIO object to a base64-encoded image
    image = base64.b64encode(buf.getvalue()).decode('utf8')
    buf.close()

    # Return the data as a JSON response
    return jsonify({
        'avg_rating_dict': avg_rating_dict,
        'chart_image': image,
        'service_requests': [{'status': service.status, 'remarks': service.remarks} for service in service_requests]
    })

############################ Professional Dashboard #############################
class ProfessionalDashboard(Resource):
    @jwt_required()
    def get(self):
        """
        Fetch data for the professional dashboard.
        Returns the logged-in professional's details, pending service requests, and closed service requests.
        """
        professional_id = get_jwt_identity()  # Get the ID of the logged-in professional
        professional_id = json.loads(professional_id)
        professional_id = professional_id["id"]
        # print(professional_id)
        # Retrieve the professional's details
        professional = ServiceProfessional.query.filter_by(user_id = professional_id).first()
        # print(professional)
        if not professional:
            return {"message": "Professional not found"}, 404
        
        # Get pending service requests
        pending_requests = ServiceRequest.query.filter(
            ServiceRequest.status == 'Pending',
            ServiceRequest.service_id == professional.service_id,
            ServiceRequest.professional_id.is_(None)  # Not yet assigned to a professional
        ).all()
        
        # Get closed service requests
        closed_service_requests = ServiceRequest.query.filter(
            ServiceRequest.status == 'Closed',
            ServiceRequest.service_id == professional.service_id,
            ServiceRequest.professional_id == professional.user_id  # Closed by this professional
        ).all()

        # Format the response
        return {
            "professional": {
                "id": professional.user_id,
                "name": professional.username,
                "email": professional.email,
                "service_id": professional.service_id,
            },

            "pending_requests": [

                
                {"id": req.id, "customer_name": Customer.query.filter_by(user_id=req.customer_id).first().username,
                 "phone_number" : Customer.query.filter_by(user_id=req.customer_id).first().mobile,
                  "address" : Customer.query.filter_by(user_id=req.customer_id).first().address
                    ,"status": req.status, "date": req.request_date.strftime("%Y-%m-%d"),
                     } # "service_name": req.service
                for req in pending_requests
            ],
            "closed_requests": [
                {"id": req.id, "customer_name": Customer.query.filter_by(user_id=req.customer_id).first().username, "status": req.status,
                "phone_no" :Customer.query.filter_by(user_id=req.customer_id).first().mobile,
                "customer_address" : Customer.query.filter_by(user_id=req.customer_id).first().address,
                  "request_date" : req.request_date.strftime("%Y-%m-%d"),
                  "rating" : req.rating,
                  "remarks" : req.remarks}
                for req in closed_service_requests
            ]
        }, 200

########################## Accept #########################################  
class AcceptService(Resource):
    @jwt_required()
    def post(self, service_id):
        """
        Accept a service request by its ID.
        Updates the request status and assigns it to the logged-in professional.
        """
        professional_id = get_jwt_identity()  # Get the ID of the logged-in professional
        professional_id = json.loads(professional_id)
        professional_id = professional_id["id"]
        
        # Retrieve the service request
        service_request = ServiceRequest.query.get(service_id)
        if not service_request:
            return {"message": "Service request not found"}, 404
        
        # Update service request details
        service_request.status = 'Accepted'
        service_request.professional_id = professional_id
        
        try:
            db.session.commit()
            return {"message": f"Service Request {service_id} accepted successfully!"}, 200
        except Exception as e:
            db.session.rollback()
            return {"message": f"Failed to accept service request: {str(e)}"}, 500
        
########################## Reject service request ##############################
class RejectService(Resource):
    @jwt_required()
    def post(self, service_id):
        """
        Reject a service request by its ID.
        Updates the request status to 'Rejected'.
        """
        professional_id = get_jwt_identity()  # Get the ID of the logged-in professional
        professional_id = json.loads(professional_id)
        professional_id = professional_id["id"]
        
        # Retrieve the service request
        service_request = ServiceRequest.query.get(service_id)
        if not service_request:
            return {"message": "Service request not found"}, 404
        
        # Update service request details
        service_request.status = 'Rejected'
        service_request.professional_id = professional_id  # Reset professional assignment
        
        try:
            db.session.commit()
            return {"message": f"Service Request {service_id} rejected successfully!"}, 200
        except Exception as e:
            db.session.rollback()
            return {"message": f"Failed to reject service request: {str(e)}"}, 500
        
# Parser for setting remarks and rating
service_request_parser = reqparse.RequestParser()
service_request_parser.add_argument('remarks', type=str, required=False, help="Remarks are optional.")
service_request_parser.add_argument('rating', type=int, required=False, help="Rating must be an integer.")


#############################  searching service requests or customers ##########################

@app.route('/service_professional_search', methods=['POST'])
def api_service_professional_search():
    # Get the search criteria and search text from the JSON body
    data = request.get_json()
    search_by = data.get('category')  # Category by which to search (date, location, or pin)
    search_text = data.get('search_query')  # Text to search for based on selected criteria
    search_results = []  # Initialize an empty list for search results

    if search_by and search_text:
        # If searching by date
        if search_by == 'date':
            try:
                # Convert the search text into a date object (expects format dd/mm/yyyy)
                search_date = datetime.strptime(search_text, '%d/%m/%Y').date()
                # Query for service requests on the specified date
                service_requests = ServiceRequest.query.filter(
                    func.date(ServiceRequest.request_date) == search_date
                ).all()

                search_results = [
                    {
                        "id": sr.id,
                        "customer_name": Customer.query.filter_by(user_id=sr.customer_id).first().username,
                        "customer_phone_no": Customer.query.filter_by(user_id=sr.customer_id).first().mobile,
                        "customer_address": Customer.query.filter_by(user_id=sr.customer_id).first().address,
                        "request_date": sr.request_date.strftime('%Y-%m-%d'),
                        "rating": sr.rating,
                    } for sr in service_requests
                ]
            except ValueError:
                # If date format is incorrect, return an empty result set
                search_results = []

        # If searching by location
        elif search_by == 'location':
            # Search for customers with an address that includes the search text, case-insensitive
            customers = Customer.query.filter(Customer.address.ilike(f'%{search_text}%')).all()

            search_results = [
                {
                    "id": cust.id,
                    "customer_name": cust.username,
                    "customer_phone_no": cust.mobile,
                    "customer_address": cust.address,
                    # Fetch the service request associated with the customer
                    "request_date": ServiceRequest.query.filter_by(customer_id=cust.id).first().request_date.strftime('%Y-%m-%d') if ServiceRequest.query.filter_by(customer_id=cust.id).first() else None,
                    "rating": ServiceRequest.query.filter_by(customer_id=cust.id).first().rating if ServiceRequest.query.filter_by(customer_id=cust.id).first() else None
                } for cust in customers
            ]

        # If searching by pin code
        elif search_by == 'pin':
            # Query for customers with a matching pin code
            customers = Customer.query.filter(Customer.pincode == search_text).all()

            search_results = [
                {
                    "id": cust.id,
                    "customer_name": cust.username,
                    "customer_phone_no": cust.mobile,
                    "customer_address": cust.address,
                    # Fetch the service request associated with the customer
                    "request_date": ServiceRequest.query.filter_by(customer_id=cust.id).first().request_date.strftime('%Y-%m-%d') if ServiceRequest.query.filter_by(customer_id=cust.id).first() else None,
                    "rating": ServiceRequest.query.filter_by(customer_id=cust.id).first().rating if ServiceRequest.query.filter_by(customer_id=cust.id).first() else None
                } for cust in customers
            ]

    # Return the search results as JSON
    return jsonify({"search_results": search_results})

######################## Professional search #################################
@app.route('/professional_summary', methods=['GET'])
@jwt_required()
def professional_summary():
    # Query to get average rating for each service professional
    avg_rating_query = (
        ServiceProfessional.query
        .join(ServiceRequest, ServiceProfessional.user_id == ServiceRequest.professional_id)
        .filter(ServiceRequest.rating.isnot(None))  # Exclude NULL ratings
        .group_by(ServiceProfessional.id, ServiceProfessional.username)
        .with_entities(ServiceProfessional.username, func.avg(ServiceRequest.rating).label('avg_rating'))
        .all()
    )
    # Convert query result to dictionary
    avg_rating_dict = {professional: round(avg_rating, 2) for professional, avg_rating in avg_rating_query}
    print("Average Ratings:", avg_rating_dict)  # Debugging output

    # Query to get the count of service requests by status
    status_counts_query = (
        ServiceRequest.query
        .with_entities(ServiceRequest.status, func.count(ServiceRequest.id))
        .group_by(ServiceRequest.status)
        .all()
    )
    status_dict = {'Accepted': 0, 'Rejected': 0, 'Closed': 0}
    for status, count in status_counts_query:
        if status in status_dict:
            status_dict[status] += count

    # Create a bar graph for service request statuses
    labels = list(status_dict.keys())
    values = list(status_dict.values())

    plt.figure(figsize=(8, 5))
    plt.bar(labels, values, color=['green', 'red', 'gray'])
    plt.xlabel('Status')
    plt.ylabel('Count')
    plt.title('Service Request Status for Professionals')

    # Save the bar graph to a BytesIO object
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

    # Convert the BytesIO object to a base64-encoded image
    image = base64.b64encode(buf.getvalue()).decode('utf8')
    buf.close()

    # Return the data as a JSON response
    return jsonify({
        'avg_rating_dict': avg_rating_dict,
        'status_dict': status_dict,
        'chart_image': image
    })

######################################## Customer API Resources ########################################

class CustomerDashboard(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        current_user = json.loads(current_user)
        if not current_user or "id" not in current_user:
            return {"error": "Invalid or missing token."}, 401

        user_id = current_user["id"]

        # Retrieve customer details
        customer = Customer.query.filter_by(user_id=user_id).first()
        if not customer:
            return {"error": "Customer not found."}, 404

        # Retrieve service history
        service_history = [
            {
                "id": req.id,
                "service_name": req.service.name if req.service else "N/A",
                "status": req.status,
                "request_date": req.request_date.strftime("%Y-%m-%d"),
                "remarks": req.remarks,
                "rating": req.rating,
                "professional_name": ServiceProfessional.query.filter_by(user_id=req.professional_id).first().username if req.status == "Accepted" or req.status == "Closed" else "N/A",
                "professional_phone": ServiceProfessional.query.filter_by(user_id=req.professional_id).first().mobile_no if req.status == "Accepted" or req.status == "Closed" else "N/A" ,
            }
            for req in ServiceRequest.query.filter_by(customer_id=customer.id).all()
        ]

        # Retrieve all available services
        services = [
            {
                "id": service.id,
                "name": service.name,
                "description": service.description,
                "base_price": service.base_price,
            }
            for service in Service.query.all()
        ]

        # Serialize customer data
        customer_data = {
            "id": customer.id,
            "username": customer.username,
            "email": customer.email,
        }

        return {
            "customer": customer_data,
            "service_history": service_history,
            "available_services": services,
        }, 200
    

# Close Service Resource
class CloseService(Resource):
    @jwt_required()
    def post(self, service_id):
        # Get current user identity (from JWT)
        current_user = get_jwt_identity()
        current_user = json.loads(current_user)
        
        if not current_user or "id" not in current_user:
            return {"error": "Invalid or missing token."}, 401

        user_id = current_user["id"]
        customer = Customer.query.filter_by(user_id=user_id).first()

        # Retrieve the service request
        service_request = ServiceRequest.query.filter_by(id=service_id, customer_id=customer.id).first()
        if not service_request:
            return {"error": "Service request not found or unauthorized action."}, 403

        # Optionally accept remarks from the frontend
        remarks = request.json.get("remarks", "Service closed by customer.")  # Default remark

        # Update service status to 'Closed'
        service_request.status = "Closed"
        service_request.remarks = remarks
        db.session.commit()

        return {"message": "Service closed successfully.", "remarks": remarks}, 200

    
# Rate Service Resource
class RateService(Resource):
    @jwt_required()
    def post(self, service_id):
        current_user = get_jwt_identity()
        current_user = json.loads(current_user)

        if not current_user or "id" not in current_user:
            return {"error": "Invalid or missing token."}, 401

        user_id = current_user["id"]
        data = request.get_json()

        # Log incoming data for debugging (consider removing in production)
        print("Received data:", data)

        # Validate rating input
        try:
            rating = int(data.get("rating"))
            if not (1 <= rating <= 5):
                raise ValueError("Rating must be between 1 and 5.")
        except (ValueError, TypeError):
            return {"error": "Invalid rating. Must be an integer between 1 and 5."}, 400

        remarks = data.get("remarks", "")  # Remarks are optional

        # Retrieve the service request
        service_request = ServiceRequest.query.filter_by(id=service_id, customer_id=user_id).first()
        if not service_request:
            return {"error": "Service request not found or unauthorized action."}, 403

        # Update the rating and remarks
        service_request.status = "Closed"
        service_request.rating = rating
        service_request.remarks = remarks
        db.session.commit()

        return {"message": "Service rated successfully.", "rating": rating}, 200
    
################################ Customer serach #######################################
@app.route('/customer_search', methods=['GET'])
def api_customer_search():
    # Retrieve the search criteria and search query from the request arguments
    search_criteria = request.args.get('search_criteria')
    search_query = request.args.get('search_query')

    # Initialize an empty list to hold the search results (Service Professionals)
    professionals = []

    # Check if both search criteria and query are provided
    if search_criteria and search_query:
        # Perform search based on the selected criteria
        if search_criteria == 'service_type':
            # Search for professionals based on the service type
            professionals = ServiceProfessional.query.filter(
                ServiceProfessional.service_type.ilike(f"%{search_query}%")
            ).all()
        elif search_criteria == 'location':
            # Search for professionals based on their address location
            professionals = ServiceProfessional.query.filter(
                ServiceProfessional.address.ilike(f"%{search_query}%")
            ).all()
        elif search_criteria == 'pincode':
            # Search for professionals based on their pincode
            professionals = ServiceProfessional.query.filter(
                ServiceProfessional.pincode.ilike(f"%{search_query}%")
            ).all()

    # Convert professionals to a list of dictionaries to return as JSON
    professionals_data = [
        {

            "username": professional.username,
            "service_type": professional.service_type,
            "address": professional.address,
            "pincode": professional.pincode,
            "mobile_no": professional.mobile_no,
            # "status": professional.status
        }
        for professional in professionals
    ]

    # Return the JSON response with search results and the original search query
    return jsonify({
        "professionals": professionals_data,
        "search_query": search_query
    })

####################### Customer summary information ######################
@app.route('/customer_summary', methods=['GET'])
@jwt_required()  # Ensure the user is authenticated via JWT
def customer_summary():
    # Get the current user's identity (optional if you need to filter by user)
    current_user = get_jwt_identity()

    # Query to get the count of service requests by status for customers (without session)
# Query to get the count of service requests by status for customers (without session)
    status_counts_query = (
        ServiceRequest.query
        .group_by(ServiceRequest.status)
        .with_entities(ServiceRequest.status, func.count(ServiceRequest.id).label('count'))
        .all()
    )
        
    # Initialize dictionary for statuses
    status_dict = {'Accepted': 0, 'Rejected': 0, 'Closed': 0}
    for status, count in status_counts_query:
        if status in status_dict:
            status_dict[status] += count

    # Create a bar graph for service request statuses for customers
    labels = list(status_dict.keys())
    values = list(status_dict.values())
    
    plt.figure(figsize=(8, 5))
    plt.bar(labels, values, color=['blue', 'red', 'gray'])
    plt.xlabel('Status')
    plt.ylabel('Count')
    plt.title('Customer Service Request Status Summary')

    # Save the bar graph to a BytesIO object
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    
    # Convert the BytesIO object to a base64-encoded image
    image = base64.b64encode(buf.getvalue()).decode('utf8')
    buf.close()

    # Return the data as JSON for Vue.js to handle
    return jsonify({
        'status_dict': status_dict,
        'image': image
    })

# Parser for booking service
booking_parser = reqparse.RequestParser()
booking_parser.add_argument('date_of_booking', type=str, required=True, help="Booking date in YYYY-MM-DD format is required.")

####################################### Booking Service API Resource #########################################################

class BookService(Resource):
    @jwt_required()
    def post(self, service_id):
        customer_id = get_jwt_identity()
        customer_id = json.loads(customer_id)
        customer_id = customer_id["id"]

        if not customer_id:
            return {"error": "Please log in to book a service."}, 401

        args = booking_parser.parse_args()
        date_of_booking = args.get('date_of_booking')

        if not date_of_booking:
            return {"error": "Booking date is required."}, 400

        try:
            # Parse the booking date
            booking_date = datetime.strptime(date_of_booking, "%Y-%m-%d")

            # Check if the customer already has a booking for the same service on the same date
            existing_booking = ServiceRequest.query.filter_by(
                service_id=service_id,
                customer_id=customer_id,
                request_date=booking_date,
            ).first()

            if existing_booking:
                return {"error": "You already have a booking for this service on the selected date."}, 400

            # Create a new service request
            new_request = ServiceRequest(
                service_id=service_id,
                customer_id=customer_id,
                request_date=booking_date,
                status="Pending",
                professional_id=None,
            )

            db.session.add(new_request)
            db.session.commit()

            return {"message": "Service booked successfully.", "booking_id": new_request.id}, 201

        except ValueError:
            return {"error": "Invalid date format. Please use YYYY-MM-DD."}, 400


