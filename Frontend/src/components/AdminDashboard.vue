<template>
  <div>
    <!-- Navbar -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
      <div class="container">
        <!-- Left Side (Welcome to Admin) -->
        <h3> Welcome to Admin </h3>

        <!-- Right Side -->
        <button
          class="navbar-toggler"
          type="button"
          data-toggle="collapse"
          data-target="#navbarNav"
          aria-controls="navbarNav"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav ml-auto">
            <li class="nav-item">
              <router-link to="/admin_dashboard" class="nav-link"
                >Home</router-link
              >
            </li>
            <li class="nav-item">
              <router-link to="/admin_search" class="nav-link"
                >Search</router-link
              >
            </li>
            <li class="nav-item">
              <router-link to="/admin_summary" class="nav-link"
                >Summary</router-link
              >
            </li>
            <li class="nav-item">
              <router-link to="/" @click="logout" class="nav-link"
                >Logout</router-link
              >
            </li>
            <li class="nav-item">
              <button type = "submit" @click = "cacheClear" class="nav-link">
                ClearCache</button>

            </li>

            <li class="nav-item">
              <button class="btn btn-outline-light ml-2" @click="create_csv">
                Get CSV Data
              </button>
            </li>
          </ul>
        </div>
      </div>
    </nav>

    <!-- Dashboard Tables -->
    <div class="container">
      <h3>Services</h3>
      <table class="table table-bordered table-striped">
        <thead>
          <tr>
            <th>ID</th>
            <th>Service Name</th>
            <th>Base Price</th>
            <th>Description</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="service in services" :key="service.id">
            <td>{{ service.id }}</td>
            <td>{{ service.name }}</td>
            <td>${{ service.price }}</td>
            <td>{{ service.description }}</td>
            <td>
              <router-link
                :to="'/edit_service/' + service.id"
                class="btn btn-warning"
                >Edit</router-link
              >
              <button @click="deleteService(service.id)" class="btn btn-danger">
                Delete
              </button>
            </td>
          </tr>
        </tbody>
      </table>
      <router-link to="/create_service" class="btn btn-primary my-3"
        >Create New Service</router-link
      >

      <!-- Professionals Table -->
      <h3 class="mt-4">Professionals</h3>
      <table class="table table-bordered table-striped">
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Experience (Yrs)</th>
            <th>Service Name</th>
            <th>Resume</th>
            <th>Status</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="professional in professionals" :key="professional.id">
            <td>{{ professional.id }}</td>
            <td>{{ professional.username }}</td>
            <td>{{ professional.experience }}</td>
            <td>{{ professional.service_type }}</td>
            <td>
              <a
                :href="
                  'http://127.0.0.1:5000/serve_resume/' +
                  professional.resume_file_path
                "
                target="_blank"
                >View Resume</a
              >
            </td>
            <td>{{ professional.status }}</td>
            <td>
              <button
                v-if="professional.status === 'pending'"
                @click="updateProfessionalStatus(professional.id, 'approved')"
                class="btn btn-success btn-action"
              >
                Accept
              </button>
              <button
                v-if="professional.status === 'approved'"
                @click="updateProfessionalStatus(professional.id, 'rejected')"
                class="btn btn-danger btn-action"
              >
                Reject
              </button>
              <button
                v-if="professional.status === 'rejected'"
                @click="updateProfessionalStatus(professional.id, 'approved')"
                class="btn btn-success btn-action"
              >
                Accept
              </button>
              <button
                @click="deleteProfessional(professional.id)"
                class="btn btn-secondary btn-action"
              >
                Delete
              </button>
            </td>
          </tr>
        </tbody>
      </table>

      <!-- Customers Table -->
      <h3>Customers</h3>
      <table class="table table-bordered table-striped">
        <thead>
          <tr>
            <th>ID</th>
            <th>Username</th>
            <th>Email</th>
            <th>Address</th>
            <th>Pincode</th>
            <th>Mobile</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="customer in customers" :key="customer.id">
            <td>{{ customer.id }}</td>
            <td>{{ customer.username }}</td>
            <td>{{ customer.email }}</td>
            <td>{{ customer.address }}</td>
            <td>{{ customer.pincode }}</td>
            <td>{{ customer.mobile }}</td>
            <td>{{ customer.status }}</td>
            <td>
              <button
                v-if="customer.status !== 'rejected'"
                @click="blockCustomer(customer.id)"
                class="btn btn-warning btn-action"
              >
                Block
              </button>
              <button
                v-if="customer.status === 'rejected'"
                @click="unblockCustomer(customer.id)"
                class="btn btn-success btn-action"
              >
                Unblock
              </button>
              <button
                @click="deleteCustomer(customer.id)"
                class="btn btn-danger btn-action"
              >
                Delete
              </button>
            </td>
          </tr>
        </tbody>
      </table>

      <!-- Service Requests Table -->
      <h3>Service Requests</h3>
      <table class="table table-bordered table-striped">
        <thead>
          <tr>
            <th>ID</th>
            <th>Customer Name</th>
            <th>Professional Name</th>
            <th>Requested Date</th>
            <th>Service Name</th>
            <th>Rating</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="request in serviceRequests" :key="request.id">
            <td>{{ request.id }}</td>
            <td>{{ request.customer_name }}</td>
            <td>{{ request.professional_name }}</td>
            <td>{{ request.request_date }}</td>
            <td>{{ request.service_name }}</td>
            <td>{{ request.rating || 'Not Rated Yet' }}</td>
            <td>{{ request.status }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      service: {
        name: '',
        description: '',
        base_price: '',
      },
      services: [],
      professionals: [],
      customers: [],
      serviceRequests: [],
    }
  },
  created() {
    this.fetchData()
  },
  methods: {
    getAuthToken() {
      console.log(location.origin)
      return localStorage.getItem('token')
    },

    // ################################  CSV   #######################################

    async create_csv() {
      const token = this.getAuthToken() // Fetch token from local storage
      const res = await fetch('http://127.0.0.1:5000/' + '/create-csv', {
        headers: {
          'Authentication-Token': token, // Add token in the headers
          // 'Content-Type': 'application/json',
        },
      })
      const task_id = (await res.json()).task_id

      const interval = setInterval(async () => {
        const res = await fetch(`http://127.0.0.1:5000/get-csv/${task_id}`)
        if (res.ok) {
          console.log('data is ready')
          window.open(`http://127.0.0.1:5000/get-csv/${task_id}`)

          clearInterval(interval)
        }
      }, 100)
    },

    // ##########################################################
    async createService() {
      try {
        const token = this.getAuthToken()
        const response = await fetch('http://127.0.0.1:5000/create_service', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify(this.service),
        })

        if (response.ok) {
          alert('Service created successfully!')
          this.$router.push('/admin_dashboard')
        } else {
          alert('Failed to create service. Please try again.')
        }
      } catch (error) {
        console.error('Error creating service:', error)
      }
    },

    async fetchData() {
      try {
        const token = this.getAuthToken()
        const response = await fetch('http://127.0.0.1:5000/admin_dashboard', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token}`,
          },
        })

        const data = await response.json()
        this.services = data.services || []
        this.professionals = data.professionals || []
        this.customers = data.customers || []
        this.serviceRequests = data.service_requests || []
      } catch (error) {
        console.error('Error fetching data:', error)
      }
    },

    async deleteService(id) {
      const token = this.getAuthToken()
      const response = await fetch(
        `http://127.0.0.1:5000/delete_service/${id}`,
        {
          method: 'DELETE',
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      )

      if (response.ok) {
        alert('Service deleted successfully!')
        this.fetchData() // Refresh the data
      } else {
        alert('Failed to delete service.')
      }
    },

    async deleteProfessional(id) {
      const token = this.getAuthToken()
      const response = await fetch(
        `http://127.0.0.1:5000/delete_professional/${id}`,
        {
          method: 'DELETE',
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      )

      if (response.ok) {
        alert('Professional deleted successfully!')
        this.fetchData()
      } else {
        alert('Failed to delete professional.')
      }
    },

    async deleteCustomer(id) {
      const token = this.getAuthToken()
      const response = await fetch(
        `http://127.0.0.1:5000/delete_customer/${id}`,
        {
          method: 'DELETE',
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      )

      if (response.ok) {
        alert('Customer deleted successfully!')
        this.fetchData()
      } else {
        alert('Failed to delete customer.')
      }
    },

    async updateProfessionalStatus(id, status) {
      const token = this.getAuthToken()
      const response = await fetch(
        `http://127.0.0.1:5000/update_professional_status/${id}`,
        {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({ status }),
        }
      )

      if (response.ok) {
        alert(`Professional status updated to ${status}`)
        this.fetchData()
      } else {
        alert('Failed to update status.')
      }
    },

    async blockCustomer(id) {
      const token = this.getAuthToken()
      const response = await fetch(
        `http://127.0.0.1:5000/block_customer/${id}`,
        {
          method: 'PUT',
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      )

      if (response.ok) {
        alert('Customer blocked successfully!')
        this.fetchData()
      } else {
        alert('Failed to block customer.')
      }
    },

    async unblockCustomer(id) {
      const token = this.getAuthToken()
      const response = await fetch(
        `http://127.0.0.1:5000/unblock_customer/${id}`,
        {
          method: 'PUT',
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      )

      if (response.ok) {
        alert('Customer unblocked successfully!')
        this.fetchData()
      } else {
        alert('Failed to unblock customer.')
      }
    },
    // ################## cache ###################
    async cacheClear() {
      try {
        const response = await fetch('http://127.0.0.1:5000/clear_cache', {
          method: 'POST'
        });
        const data = await response.json();
        if (response.ok) {
          alert(data.message);
          this.fetchData(); // Refresh the data after cache is cleared
        } else {
          console.error('Error clearing cache:', data);
        }
      } catch (error) {
        console.error('Error clearing cache:', error);
      }
    },
    logout() {
      localStorage.removeItem('token')
      this.$router.push({ name: 'HomePage' })
    },
  },
}
</script>

<style scoped>
/* Navbar Styling */
.navbar {
  background-color: #007bff; /* Blue background */
  padding: 0.5rem 1rem;
}

h3{
  margin-top: 0;
    margin-bottom: .5rem;
    font-weight: 500;
    line-height: 1.2;
    color: rgb(1, 18, 25);
    margin-right: 400px;
}
.navbar-brand {
  color: #ffffff; /* White text for "Welcome to Admin" */
  font-size: 1.5rem;
}

.navbar-brand:hover {
  text-decoration: none;
  color: #ffc107; /* Gold hover effect */
}

/* Links Styling */
.navbar-nav .nav-link {
  color: #ffffff !important; /* White text for links */
  margin-right: 15px;
  transition: color 0.3s ease-in-out;
}

.navbar-nav .nav-link:hover {
  color: #ffc107 !important; /* Gold hover effect */
  text-decoration: underline; /* Underline on hover */
}

/* Buttons Styling */
.nav-item .btn {
  color: #ffffff !important; /* White text for buttons */
  border-color: #ffffff !important; /* White border */
  margin-left: 15px;
  transition: all 0.3s ease-in-out;
}

.nav-item .btn:hover {
  color: #343a40 !important; /* Dark text on hover */
  background-color: #ffc107 !important; /* Gold background on hover */
  border-color: #ffc107 !important; /* Gold border on hover */
}

/* Toggler Styling */
.navbar-toggler {
  border-color: rgba(255, 255, 255, 0.1); /* Subtle border for toggler */
}

.navbar-toggler-icon {
  background-color: #ffffff; /* White toggler icon */
}

/* Responsive Adjustments */
@media (max-width: 768px) {
  .navbar-nav {
    text-align: center;
  }

  .nav-item {
    margin-bottom: 10px;
  }

  .nav-item .btn {
    width: 100%;
  }
}

.bg-primary {
    --bs-bg-opacity: 1;
    background-color: rgba(var(--bs-primary-rgb), var(--bs-bg-opacity)) !important;
    margin-bottom: 15px;
}
</style>
