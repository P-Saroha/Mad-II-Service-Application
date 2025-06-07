<template>
  <div>
    <header class="navbar navbar-dark bg-teal">
  <div class="container">
    <h3>Welcome {{ professional.name }} to Professional Dashboard</h3>
    <div class="navbar-right">
      <router-link to="/professional_dashboard">Home</router-link>
      <router-link to="/service_professional_search">Search</router-link>
      <router-link to="/professional_summary">Summary</router-link>
     <router-link to="/" @click="logout" >Logout</router-link>
    </div>
  </div>
</header>

    <div class="container">
      <!-- Pending Service Requests Section -->
      <section>
        <h3>Pending Service Requests</h3>
        <table class="table table-striped table-bordered">
          <thead>
            <tr>
              <th>ID</th>
              <th>Customer Name</th>
              <th>Phone Number</th>
              <th>Customer Address</th>
              <th>Request Date</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="request in pendingRequests" :key="request.id">
              <td>{{ request.id }}</td>
              <td>{{ request.customer_name }}</td>
              <td>{{ request.phone_number }}</td>
              <td>{{ request.address }}</td>
              <td>{{ request.date }}</td>
              <td>
                <span :class="{
                  'text-warning': request.status === 'Pending',
                  'text-success': request.status === 'Accepted',
                  'text-danger': request.status === 'Rejected'
                }">
                  {{ request.status }}
                </span>
              </td>
              <td>
                <button @click="acceptService(request.id)" class="btn btn-success btn-sm" :disabled="request.status !== 'Pending'">
                  Accept
                </button>
                <button @click="rejectService(request.id)" class="btn btn-danger btn-sm" :disabled="request.status !== 'Pending'">
                  Reject
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </section>

      <!-- Closed Services Section -->
      <section>
        <h3>Closed Services</h3>
        <table class="table table-striped table-bordered">
          <thead>
            <tr>
              <th>Request ID</th>
              <th>Customer Name</th>
              <th>Phone Number</th>
              <th>Customer Address</th>
              <th>Request Date</th>
              <th>Rating</th>
              <th>Remarks</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="closedRequest in closedRequests" :key="closedRequest.id">
              <td>{{ closedRequest.id }}</td>
              <td>{{ closedRequest.customer_name }}</td>
              <td>{{ closedRequest.phone_no }}</td>
              <td>{{ closedRequest.customer_address }}</td>
              <td>{{ closedRequest.request_date }}</td>
              <td>{{ closedRequest.rating }}</td>
              <td>{{ closedRequest.remarks }}</td>
            </tr>
          </tbody>
        </table>
      </section>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      professional: {},
      pendingRequests: [],
      closedRequests: [],
    };
  },
  created() {
    this.fetchDashboardData();
  },
  methods: {
    // Helper to get JWT token from localStorage
    getToken() {
      return localStorage.getItem("token"); // Ensure your token is stored in localStorage after login
    },

    // Fetch data for the dashboard
    async fetchDashboardData() {
      try {
        const token = this.getToken();
        const response = await fetch("/api/professional_dashboard", {
          method: "GET",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        if (!response.ok) {
          if (response.status === 401) {
            alert("Unauthorized. Please log in again.");
            this.logout();
          }
          throw new Error("Error fetching dashboard data");
        }

        const data = await response.json();
        if (data.error) {
          console.error(data.error);
        } else {
          this.professional = data.professional;
          this.pendingRequests = data.pending_requests;
          this.closedRequests = data.closed_requests;
        }
      } catch (error) {
        console.error("Error fetching dashboard data:", error);
      }
    },

    // Accept a service request
    async acceptService(serviceId) {
      try {
        const token = this.getToken();
        const response = await fetch(`/api/accept_service/${serviceId}`, {
          method: "POST",
          headers: {
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({}), // empty body since no payload is sent
        });

        if (!response.ok) {
          if (response.status === 401) {
            alert("Unauthorized. Please log in again.");
            this.logout();
          }
          throw new Error("Error accepting service");
        }

        const data = await response.json();
        if (data.message) {
          alert(data.message); // Success message
          this.fetchDashboardData(); // Refresh dashboard data
        } else {
          alert("Error: Unable to accept service");
        }
      } catch (error) {
        console.error("Error accepting service:", error);
      }
    },

    // Reject a service request
    async rejectService(serviceId) {
      try {
        const token = this.getToken();
        const response = await fetch(`/api/reject_service/${serviceId}`, {
          method: "POST",
          headers: {
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({}), // empty body since no payload is sent
        });

        if (!response.ok) {
          if (response.status === 401) {
            alert("Unauthorized. Please log in again.");
            this.logout();
          }
          throw new Error("Error rejecting service");
        }

        const data = await response.json();
        if (data.message) {
          alert(data.message); // Success message
          this.fetchDashboardData(); // Refresh dashboard data
        } else {
          alert("Error: Unable to reject service");
        }
      } catch (error) {
        console.error("Error rejecting service:", error);
      }
    },

    // Log out the professional
    logout() {
      localStorage.removeItem("token"); // Clear JWT token
      this.$router.push({ name: "HomePage" });
    },
  },
};
</script>


<style scoped>
body {
  font-family: Arial, sans-serif;
  background-color: #f8f9fa;
}

.bg-teal {
  background-color: #008080;
  color: white;
}

header h2 {
  font-size: 1.5rem;
}

.navbar-right a {
  color: white;
  font-weight: bold;
  margin: 0 15px;
  text-decoration: none;
  transition: color 0.3s; /* Smooth color transition */
}

/* Hover effect for links */
.navbar-right :hover {
  color: #db9f88; /* Coral/Orange */

 
  /* Change text color on hover */
}

</style>
