<template>
    <div class="container mt-5">
      <h1 class="text-center text-primary mb-5">Admin Summary</h1>
  
      <!-- Average Rating Section -->
      <div class="row">
        <div class="col-md-6 text-center">
          <h2>Average Rating for Service Professionals</h2>
          <ul class="list-group">
            <li 
              v-for="(avgRating, professional) in avgRatingDict" 
              :key="professional" 
              class="list-group-item d-flex justify-content-between align-items-center"
            >
              {{ professional }}
              <span class="badge badge-primary badge-pill">{{ avgRating.toFixed(2) }}</span>
            </li>
          </ul>
        </div>
  
        <!-- Bar Graph Section -->
        <div class="col-md-6 text-center">
          <h2>Service Request Status Summary</h2>
          <img :src="'data:image/png;base64,' + chartImage" alt="Service Request Status Summary" class="img-fluid">
        </div>
      </div>
  
      <!-- Service Request Details Section -->
      <div class="mt-5">
        <h3>Service Requests Details:</h3>
        <ul class="list-group">
          <li 
            v-for="service in serviceRequests" 
            :key="service.id" 
            class="list-group-item"
          >
            <strong>Status:</strong> {{ service.status }} - 
            <strong>Details:</strong> {{ service.remarks || 'No details available' }}
          </li>
        </ul>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        avgRatingDict: {},
        chartImage: '',
        serviceRequests: []
      };
    },
    created() {
      this.fetchAdminSummary();
    },
    methods: {
      async fetchAdminSummary() {
        const token = localStorage.getItem('token'); // Assuming you store the token in localStorage
        
        if (!token) {
          console.error('Authentication token is missing');
          return;
        }
  
        try {
          const response = await fetch('/api/admin_summary', {
            method: 'GET',
            headers: {
              'Authorization': `Bearer ${token}`
            }
          });
  
          if (!response.ok) {
            console.error('Error fetching admin summary:', response.statusText);
            return;
          }
  
          const data = await response.json();
  
          // Set the data from API response
          this.avgRatingDict = data.avg_rating_dict;
          this.chartImage = data.chart_image;
          this.serviceRequests = data.service_requests;
        } catch (error) {
          console.error('Error fetching admin summary data:', error);
        }
      }
    }
  };
  </script>
  
<style scoped>
  .badge.badge-primary.badge-pill {
    color: #6816ec; /* Example color */
  }
</style>



  