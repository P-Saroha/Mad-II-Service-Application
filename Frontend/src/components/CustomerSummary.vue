<template>
  <div>
    <h1>Customer Service Request Summary</h1>
    
    <!-- Display the bar graph image -->
    <div v-if="image">
      <img :src="'data:image/png;base64,' + image" alt="Customer Service Request Status Summary" />
    </div>
    
    <!-- Display the service request status details -->
    <div v-if="statusDict">
      <ul>
        <li v-for="(count, status) in statusDict" :key="status">
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
      statusDict: null,
      image: null
    };
  },
  created() {
    this.fetchCustomerSummary();
  },
  methods: {
    async fetchCustomerSummary() {
      try {
        const token = localStorage.getItem("token");  // Get JWT token from localStorage

        const response = await fetch("/api/customer_summary", {
          method: "GET",
          headers: {
            "Authorization": `Bearer ${token}`
          }
        });

        const data = await response.json();

        this.statusDict = data.status_dict;
        this.image = data.image;
      } catch (error) {
        console.error("Error fetching customer summary:", error);
      }
    }
  }
};
</script>
<style scoped>
.badge.badge-success.badge-pill
{
  color: #6816ec;
}
</style>