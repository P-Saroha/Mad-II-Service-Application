<template>
    <div>
      <header class="navbar navbar-dark bg-teal">
  <div class="container">
    <h3>Welcome {{ customer }} to Customer Search</h3>
    <div class="navbar-right">
      <router-link to="/customer_dashboard">Home</router-link>
      <router-link to="/customer_search">Search</router-link>
      <router-link to="/customer_summary">Summary</router-link>
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
              <option value="service_type">Service Type</option>
              <option value="location">Location</option>
              <option value="pincode">Pincode</option>
            </select>
            <input
              type="text"
              v-model="searchQuery"
              placeholder="Enter your search text"
              class="form-control mr-3"
            />
            <button type="submit" class="btn btn-primary">Search</button>
          </form>
          <p class="mt-2"><small>(Example: Plumber, 12345 for location or pincode)</small></p>
        </div>
  
        <!-- Search Results Section -->
        <div class="search-results" v-if="searchResults.length > 0">
          <h3>Search Results</h3>
          <table class="table table-bordered table-striped">
            <thead class="thead-dark">
              <tr>
                <!-- <th>Request ID</th> -->
                <th>Service Provider</th>
                <th>Service Name</th>
                <th>Pincode</th>
                <th>Address</th>
                <th>Mobile No.</th>   
                <!-- <th>Status</th> -->
              </tr>
            </thead>
            <tbody>
              <tr v-for="result in searchResults" :key="result.id">
                <!-- <td>{{ result.id }}</td> -->
                <td>{{ result.username }}</td>
                <td>{{ result.service_type }}</td>
                <td>{{ result.pincode }}</td>
                <td>{{ result.address }}</td>
                <td> {{ result.mobile_no}} </td>
                <!-- <td>{{ result.status }}</td> -->
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
    name: "CustomerSearch",
    data() {
      return {
        customer: "", // Dynamically fetched customer name
        selectedCategory: "service_type", // Default search category
        searchQuery: "",
        searchResults: [],
        searchAttempted: false,
      };
    },
    methods: {
      // Perform search functionality with GET request
      async performSearch() {
        // Reset search results and attempt flag
        this.searchResults = [];
        this.searchAttempted = false;
  
        // Ensure that both search criteria and text are provided
        if (!this.selectedCategory || !this.searchQuery) {
          alert("Please select a search criterion and enter search text.");
          return;
        }
  
        try {
          // Perform the GET request with query parameters
          const response = await fetch(`http://127.0.0.1:5000/customer_search?search_criteria=${this.selectedCategory}&search_query=${this.searchQuery}`, {
            method: 'GET',
            headers: {
              "Authorization": `Bearer ${localStorage.getItem("token")}`,
            },
          });
  
          // Check if the response was successful
          if (!response.ok) {
            throw new Error("Network response was not ok");
          }
  
          // Parse the response data
          const data = await response.json();
  
          // Assign the search results and mark the search as attempted
          this.searchResults = data.professionals || [];
          this.searchAttempted = true;
        } catch (error) {
          console.error("Error fetching search results:", error);
          alert("An error occurred while fetching search results. Please try again.");
        }
      },
  
      // Handle logout functionality
      logout() {
        localStorage.removeItem("token"); // Clear the stored token
        this.$router.push({ name: "HomePage" }); // Redirect to the home page
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
    margin-bottom: 10px;
  }

  .navbar-right a {
    color: white;
    font-weight: bold;
    margin: 0 15px;
    text-decoration: none;
    transition: color 0.3s, transform 0.3s;
  }

  .navbar-right a:hover {
    color: #00d1b2; /* Change to a teal-like color when hovered */
    transform: scale(1.1); /* Slightly enlarges the link */
  }

  .search-container {
    margin-top: 20px;
  }

  .table {
    margin-top: 20px;
  }

  .text-center {
    margin-top: 20px;
  }
</style>