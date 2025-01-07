<template>
  <div class="container mt-5">
    <!-- Alert Messages -->
    <div v-if="message" :class="`alert alert-${messageType}`" role="alert">
      {{ message }}
    </div>

    <h2 class="mb-4">Book Service</h2>

    <!-- Booking Form -->
    <form @submit.prevent="bookService">
      <div class="mb-3">
        <label for="date_of_booking" class="form-label">Date of Booking</label>
        <input
          type="date"
          class="form-control"
          id="date_of_booking"
          v-model="dateOfBooking"
          required
        />
      </div>
      <button type="submit" class="btn btn-primary" :disabled="loading">
        {{ loading ? "Booking..." : "Book Now" }}
      </button>
    </form>
  </div>
</template>

<script>
export default {
  name: "BookService",
  
  data() {
    return {
      dateOfBooking: "", // Model for the booking date
      message: null, // Alert message
      messageType: "", // Alert type (success, error)
      loading: false, // Loading state
    };
  },
  methods: {
    async bookService() {
      // Clear previous messages
      this.message = null;
      this.messageType = "";
      this.loading = true;

      try {
        // Get the JWT token from local storage
        const token = localStorage.getItem("token");

        if (!token) {
          throw new Error("Authentication token is missing. Please log in.");
        }
        const serviceId = this.$route.params.service_id; // Get the service ID from the route
        // Send POST request using Fetch API
        const response = await fetch(`http://127.0.0.1:5000/book_service/${serviceId}`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`, // Include the JWT token
          },
          body: JSON.stringify({
            date_of_booking: this.dateOfBooking,
          }),
        });

        // Parse the response
        const data = await response.json();

        if (!response.ok) {
          // Handle API errors
          throw new Error(data.error || "An error occurred while booking the service.");
        }

        // Display success message
        this.message = data.message;
        this.messageType = "success";
      } catch (error) {
        // Handle errors and display error message
        this.message = error.message || "An unexpected error occurred.";
        this.messageType = "danger";
      } finally {
        // Reset loading state
        this.loading = false;
      }
    },
  },
};
</script>

<style scoped>
.container {
  max-width: 600px;
  margin: auto;
}
</style>
