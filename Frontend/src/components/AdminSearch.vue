<template>
    <div>
      <!-- Navbar -->
      <nav class="navbar navbar-expand-lg navbar-dark">
        <div class="container">
          <h3>Welcome to Admin Search</h3>
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
                <router-link class="nav-link" to="/admin_dashboard">Home</router-link>
              </li>
              <li class="nav-item">
                <router-link class="nav-link" to="/admin_search">Search</router-link>
              </li>
              <li class="nav-item">
                <router-link class="nav-link" to="/admin_summary">Summary</router-link>
              </li>
              <li class="nav-item">
              <router-link to="/" @click="logout" class="nav-link"
                >Logout</router-link
              >
            </li>
            </ul>
          </div>
        </div>
      </nav>
  
      <!-- Search Form -->
      <div class="container mt-5">
        <form @submit.prevent="performSearch">
          <div class="form-group">
            <label for="category">Select Category</label>
            <select
              v-model="selectedCategory"
              id="category"
              class="form-control"
            >
              <option value="service_requests">Service Requests</option>
              <option value="customers">Customers</option>
              <option value="professionals">Professionals</option>
            </select>
          </div>
          <div class="form-group">
            <label for="search_query">Search</label>
            <input
              type="text"
              v-model="searchQuery"
              id="search_query"
              class="form-control"
              placeholder="Enter search term"
            />
          </div>
          <button type="submit" class="btn btn-primary">Search</button>
        </form>
  
        <!-- Conditional Tables -->
        <div v-if="selectedCategory === 'service_requests'" class="mt-5">
          <h3>Service Requests</h3>
          <table class="table table-bordered">
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
                <td>{{ request.requested_date }}</td>
                <td>{{ request.service_name }}</td>
                <td>{{ request.rating }}</td>
                <td>{{ request.status }}</td>
              </tr>
            </tbody>
          </table>
        </div>
  
        <div v-if="selectedCategory === 'customers'" class="mt-5">
          <h3>Customers</h3>
          <table class="table table-bordered">
            <thead>
              <tr>
                <th>ID</th>
                <th>Username</th>
                <th>Mobile No</th>
                <th>Email</th>
                <th>Address</th>
                <th>Pin Code</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="customer in customers" :key="customer.id">
                <td>{{ customer.id }}</td>
                <td>{{ customer.username }}</td>
                <td>{{ customer.mobile }}</td>
                <td>{{ customer.email }}</td>
                <td>{{ customer.address }}</td>
                <td>{{ customer.pincode }}</td>
              </tr>
            </tbody>
          </table>
        </div>
  
        <div v-if="selectedCategory === 'professionals'" class="mt-5">
          <h3>Service Professionals</h3>
          <table class="table table-bordered">
            <thead>
              <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Experience (Yrs)</th>
                <th>Mobile No</th>
                <th>Email</th>
                <th>Address</th>
                <th>Service Type</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="professional in professionals" :key="professional.id">
                <td>{{ professional.id }}</td>
                <td>{{ professional.username }}</td>
                <td>{{ professional.experience }}</td>
                <td>{{ professional.mobile_no }}</td>
                <td>{{ professional.email }}</td>
                <td>{{ professional.address }}</td>
                <td>{{ professional.service_type }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        selectedCategory: "service_requests",
        searchQuery: "",
        serviceRequests: [],
        customers: [],
        professionals: [],
      };
    },
    methods: {
      async performSearch() {
        try {
          const response = await fetch("http://127.0.0.1:5000/admin_search", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${localStorage.getItem("token")}`,
            },
            body: JSON.stringify({
              search_query: this.searchQuery,
              category: this.selectedCategory,
            }),
          });
  
          if (!response.ok) {
            throw new Error("Failed to fetch search results.");
          }
  
          const data = await response.json();
          if (this.selectedCategory === "service_requests") {
            this.serviceRequests = data.service_requests || [];
          } else if (this.selectedCategory === "customers") {
            this.customers = data.customers || [];
          } else if (this.selectedCategory === "professionals") {
            this.professionals = data.professionals || [];
          }
        } catch (error) {
          console.error("Error:", error);
          alert("Error occurred while fetching data.");
        }
        
      },
      logout() {
      localStorage.removeItem('token')
      this.$router.push({name: 'HomePage'});
    }
    },
  };
  </script>
  
  <style scoped>
  h2 {
    color: #ffffff;
  }
  h3 { margin-top: 0;
    margin-bottom: .5rem;
    font-weight: 500;
    line-height: 1.2;
    color: white;;
    margin-right: 600px;
}
  body {
    background-color: #f8f9fa;
  }
  
  .container {
    margin-top: 30px;
  }
  
  /* Navbar styling */
  .navbar {
    background-color: #343a40;
  }
  
  .navbar-brand,
  .navbar-nav .nav-link {
    color: #ffffff !important;
  }
  
  .navbar-nav .nav-link:hover {
    color: #ffc107 !important;
    text-decoration: underline;
  }
  
  .navbar-nav .nav-item.active .nav-link {
    color: #ffc107 !important;
  }
  
  .navbar-toggler {
    border-color: rgba(255, 255, 255, 0.1);
  }
  </style>
  