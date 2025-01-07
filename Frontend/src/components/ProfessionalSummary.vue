<template>
    <div class="container mt-5">
      <h1 class="text-center text-success mb-5">Service Professional Summary</h1>
      
      <!-- Average Rating Section -->
      <div class="row">
        <div class="col-md-6 text-center">
          <h2>Average Rating for Each Professional</h2>
          <ul class="list-group">
            <li class="list-group-item d-flex justify-content-between align-items-center" 
                v-for="(rating, professional) in avgRatingDict" :key="professional">
              {{ professional }}
              <span class="badge badge-success badge-pill">{{ rating }}</span>
            </li>
          </ul>
        </div>
  
        <!-- Bar Graph Section -->
        <div class="col-md-6 text-center">
          <h2>Service Request Status Summary</h2>
          <img :src="'data:image/png;base64,' + chartImage" alt="Service Request Status Summary" class="img-fluid">
        </div>
      </div>
  
      <!-- Service Request Status Section -->
      <div class="mt-5">
        <h3>Service Request Status Details:</h3>
        <ul class="list-group">
          <li class="list-group-item" 
              v-for="(count, status) in statusDict" :key="status">
            <strong>{{ status }}:</strong> {{ count }} requests
          </li>
        </ul>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        avgRatingDict: {},  // Dictionary to store average ratings for each professional
        statusDict: {},     // Dictionary to store status count (Accepted, Rejected, Closed)
        chartImage: "",     // Base64-encoded image for the bar graph
      };
    },
    mounted() {
      this.fetchProfessionalSummary();
    },
    methods: {
      async fetchProfessionalSummary() {
        try {
          const response = await fetch("http://127.0.0.1:5000/professional_summary", {
            method: "GET",
            headers: {
              "Authorization": `Bearer ${localStorage.getItem("token")}`,  // If you are using JWT token for auth
            },
          });
          const data = await response.json();
  
          this.avgRatingDict = data.avg_rating_dict; // Store average ratings for each professional
          this.statusDict = data.status_dict;       // Store request status details
          this.chartImage = data.chart_image;        // Store the chart image (base64)
        } catch (error) {
          console.error("Error fetching data:", error);
        }
      },
    },
  };
  </script>
  
  <style scoped>
  .badge.badge-success.badge-pill
  {
    color: #6816ec;
  }
  </style>
  
