<template>
  <div>
    <!-- Header Section -->
    <header class="navbar navbar-dark bg-teal">
      <div class="container">
        <h3>Welcome {{ professional.name }} to Professional Search</h3>
        <div class="navbar-right">
          <router-link to="/professional_dashboard">Home</router-link>
          <router-link to="/service_professional_search">Search</router-link>
          <router-link to="/professional_summary">Summary</router-link>
          <router-link to="/" @click="logout">Logout</router-link>
        </div>
      </div>
    </header>

    <!-- Search Section -->
    <div class="container mt-4">
      <h3>Search Functionality</h3>
      <div class="search-container">
        <form @submit.prevent="performSearch" class="form-inline">
          <label for="search_by" class="mr-2">Search by:</label>
          <select v-model="selectedCategory" id="search_by" class="form-control mr-3">
            <option value="date">Date</option>
            <option value="location">Location</option>
            <option value="pin">Pin Code</option>
          </select>
          <input
            type="text"
            v-model="searchQuery"
            placeholder="Search text"
            class="form-control mr-3"
          />
          <button type="submit" class="btn btn-primary">Search</button>
        </form>
        <p class="mt-2"><small>(Example: 07/08/2024 for date)</small></p>
      </div>

      <!-- Search Results Section -->
      <div class="search-results" v-if="searchResults.length > 0">
        <h3>Search Results</h3>
        <table class="table table-bordered table-striped">
          <thead class="thead-dark">
            <tr>
              <th>ID</th>
              <th>Customer Name</th>
              <th>Customer Phone NO.</th>
              <th>Customer Address</th>
              <th>Request Date</th>
              <th>Rating</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="result in searchResults" :key="result.id">
              <td>{{ result.id }}</td>
              <td>{{ result.customer_name }}</td>
              <td>{{ result.customer_phone_no }}</td>
              <td>{{ result.customer_address }}</td>
              <td>{{ result.request_date }}</td>
              <td>{{ result.rating }}</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- No Results Found -->
      <div v-else-if="searchAttempted" class="text-center">
        <p>No results found.</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "ProfessionalSearch",
  data() {
    return {
      professional: {}, // Replace with dynamic data if needed
      selectedCategory: "date", // Default search category
      searchQuery: "",
      searchResults: [],
      searchAttempted: false,
    };
  },
  created() {
    this.fetchDashboardData();
  },
  methods: {
    getToken() {
      return localStorage.getItem("token"); // Ensure your token is stored in localStorage after login
    },

    async fetchDashboardData() {
      const token = this.getToken();
      if (!token) {
        alert("You are not authorized. Please log in.");
        this.$router.push("/");
        return;
      }
      try {
        const response = await fetch("/api/professional_dashboard", {
          method: "GET",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        const data = await response.json();
        if (data.error) {
          console.error(data.error);
        } else {
          this.professional = data.professional || {};
        }
      } catch (error) {
        console.error("Error fetching dashboard data:", error);
      }
    },

    async performSearch() {
      if (!this.selectedCategory || !this.searchQuery) {
        alert("Please select a search criterion and enter search text.");
        return;
      }
      try {
        const response = await fetch("/api/service_professional_search", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${this.getToken()}`,
          },
          body: JSON.stringify({
            search_query: this.searchQuery,
            category: this.selectedCategory,
          }),
        });
        const data = await response.json();
        this.searchResults = data.search_results || [];
        this.searchAttempted = true;
      } catch (error) {
        console.error("Error fetching search results:", error);
        alert("An error occurred while fetching search results.");
      }
    },

    logout() {
      localStorage.removeItem("token");
      this.$router.push("/");
    },
  },
};
</script>

<style scoped>
.bg-teal {
  background-color: #008080;
  color: white;
}

.navbar-right a {
  color: white;
  font-weight: bold;
  margin: 0 15px;
  text-decoration: none;
  transition: color 0.3s;
}

::v-deep(.navbar-right a:hover) {
  color: #db9f88;
}
</style>

