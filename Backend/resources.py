
from flask_restful import Api
from Backend.routes import (AdminLogin, AdminDashboard, GetService, GetServices, UpdateProfessionalStatus, DeleteProfessional,
                     CreateService, DeleteService, EditService, DeleteService, ProfessionalDashboard,AcceptService,
                     RejectService, CustomerDashboard, CloseService, RateService, BookService
                     )

api = Api()

################################ Adding API Resource ###################

##########  Admin API ####################################################
# Add the AdminLogin resource to the API
api.add_resource(AdminLogin, '/admin_login')
api.add_resource(AdminDashboard, '/admin_dashboard')
# Register routes
api.add_resource(GetService, "/get_service/<int:service_id>")
# Register the resource
api.add_resource(GetServices, '/get_services')
# API Routes for managing service professionals
api.add_resource(UpdateProfessionalStatus, '/update_professional_status/<int:professional_id>')
api.add_resource(DeleteProfessional, '/delete_professional/<int:professional_id>')
# API Routes
api.add_resource(CreateService, '/create_service')  # Create Service
api.add_resource(EditService, '/edit_service/<int:service_id>')  # Edit Service
api.add_resource(DeleteService, '/delete_service/<int:service_id>')  # Delete Service

##################### Professional Api ############################################
# Add API routes
api.add_resource(ProfessionalDashboard, '/professional_dashboard')
api.add_resource(AcceptService, '/accept_service/<int:service_id>')
api.add_resource(RejectService, '/reject_service/<int:service_id>')

######################################## Customer Api #################################

# Add the resources to the API
api.add_resource(CustomerDashboard, '/customer_dashboard')
api.add_resource(CloseService, '/close_service/<int:service_id>')
api.add_resource(RateService, '/rate_service/<int:service_id>')
api.add_resource(BookService, '/book_service/<int:service_id>')

####################################################################################