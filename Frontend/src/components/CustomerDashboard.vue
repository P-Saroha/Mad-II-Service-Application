<template>
  <div>
<!-- Header Section -->
<header class="bg-primary text-white py-3 mb-4">
  <div class="container d-flex justify-content-between align-items-center">
    <h3>Welcome {{ customer.username }} to Customer Dashboard</h3>
    <nav>
      <router-link to="/customer_dashboard" class="text-white me-3">Home</router-link>
      <router-link to="/customer_search" class="text-white me-3">Search</router-link>
      <router-link to="/customer_summary" class="text-white me-3">Summary</router-link>
      <router-link to="/" @click="logout" class="text-white me-3">Logout</router-link>
    </nav>
  </div>
</header>

    <!-- Loading Spinner -->
    <div v-if="isLoading" class="text-center mb-4">
      <div class="spinner-border" role="status">
        <span class="sr-only">Loading...</span>
      </div>
    </div>

    <!-- Service Selection Section -->
    <section id="services" class="mb-4" v-if="!isLoading">
      <h2 class="h4 mb-3">Looking For?</h2>
      <div class="row">
        <div v-for="service in services" :key="service.id" class="col-md-3 mb-3">
          <div class="card shadow-sm">
            <div class="card-body text-center">
              <h5 class="card-title">{{ service.name }}</h5>
              <p>{{ service.description }}</p>
              <p>${{ service.base_price }}</p>
              <router-link :to="'/book_service/' + service.id" class="btn btn-outline-primary">Select</router-link>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Service History Section -->
    <section id="service-history" class="mb-4" v-if="!isLoading">
      <h2 class="h4">Service History</h2>
      <table class="table table-bordered">
        <thead class="table-dark">
          <tr>
            <th>ID</th>
            <th>Service Name</th>
            <th>Professional Name</th>
            <th>Professional Phone No</th>
            <th>Status</th>
            <th>Rate Service</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="history in serviceHistory" :key="history.id">
            <td>{{ history.id }}</td>
            <td>{{ history.service_name }}</td>
            <td>{{ history.professional_name }}</td>
            <td>{{ history.professional_phone}}</td>
            <td>{{ history.status }}</td>
            <td>
              <div v-if="(history.status === 'Closed' || history.status === 'Accepted') && !history.rating">
                <select v-model="ratings[history.id]" class="form-select form-select-sm">
                  <option v-for="n in 5" :key="n" :value="n">{{ n }}</option>
                </select>
                <textarea v-model="remarks[history.id]" class="form-control mt-2" placeholder="Enter your remarks here..."></textarea>
                <button @click="rateService(history.id)" class="btn btn-primary btn-sm mt-1">Submit</button>
              </div>
              <div v-else>
                <span class="badge bg-info">{{ history.rating }} / 5</span>
                <p v-if="history.remarks" class="mt-2"><strong>Remarks:</strong> {{ history.remarks }}</p>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </section>

    <!-- Error Message -->
    <div v-if="errorMessage" class="alert alert-danger">
      {{ errorMessage }}
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      services: [],
      serviceHistory: [],
      customer: {
        id: null,
        username: '',
        email: '',
      },
      isLoading: true,
      errorMessage: '',
      ratings: {}, // For storing temporary ratings
      remarks: {}, // For storing temporary remarks
    };
  },
  created() {
    this.fetchCustomerDashboard();
  },
  methods: {
    async fetchCustomerDashboard() {
      this.isLoading = true;
      const token = localStorage.getItem('token');
      if (!token) {
        this.$router.push('/login');
        return;
      }
      try {
        const response = await fetch('http://127.0.0.1:5000/customer_dashboard', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
          },
        });
        if (!response.ok) throw new Error('Failed to fetch data');
        const { customer, service_history, available_services } = await response.json();
        this.customer = customer;
        this.serviceHistory = service_history;
        this.services = available_services;
      } catch (error) {
        this.errorMessage = `Error: ${error.message}`;
      } finally {
        this.isLoading = false;
      }
    },
    async closeService(serviceId) {
      try {
        const token = localStorage.getItem('token');
        const response = await fetch(`http://127.0.0.1:5000/close_service/${serviceId}`, {
          method: 'POST',
          headers: { 
            'Authorization': `Bearer ${token}` 
          },
        });
        if (response.ok) this.fetchCustomerDashboard();
        else throw new Error('Failed to close service');
      } catch (error) {
        this.errorMessage = `Error: ${error.message}`;
      }
    },
    async rateService(serviceId) {
      try {
        const token = localStorage.getItem('token');
        const data = { 
          rating: this.ratings[serviceId], 
          remarks: this.remarks[serviceId] 
        };
        
        const response = await fetch(`http://127.0.0.1:5000/rate_service/${serviceId}`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(data),
        });
        
        if (response.ok) {
          this.fetchCustomerDashboard();
        } else {
          const errorResponse = await response.json();
          throw new Error(errorResponse.error || 'Failed to rate service');
        }
      } catch (error) {
        this.errorMessage = `Error: ${error.message}`;
      }
    },
    logout() {
      localStorage.removeItem('token');
      this.$router.push({ name: 'HomePage' });
    },
  },
};
</script>


<style scoped>
  /* General header styles */
  header {
    background-color: #007bff; /* Bootstrap primary color */
    color: white;
  }

  /* Styling for the navigation links */
  nav router-link {
    color: white;
    font-weight: bold;
    text-decoration: none;
    transition: color 0.3s, transform 0.3s;
  }

  /* Container spacing */
  .container {
    padding: 0 15px;
  }

  /* Margin for header */
  .mb-4 {
    margin-bottom: 1.5rem;
  }

  /* Padding for header */
  .py-3 {
    padding-top: 1rem;
    padding-bottom: 1rem;
  }
</style>
