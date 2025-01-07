<template>
  <div class="container">
    <h1>Create New Service</h1>
    <form @submit.prevent="submitForm">
      <div class="form-group">
        <label for="name">Service Name</label>
        <input
          type="text"
          class="form-control"
          id="name"
          v-model="serviceName"
          required
        />
      </div>
      <div class="form-group">
        <label for="description">Description</label>
        <textarea
          class="form-control"
          id="description"
          v-model="serviceDescription"
          required
        ></textarea>
      </div>
      <div class="form-group">
        <label for="base_price">Base Price</label>
        <input
          type="number"
          class="form-control"
          id="base_price"
          v-model="servicePrice"
          required
        />
      </div>
      <button type="submit" class="btn btn-primary">Create</button>
      <button type="button" class="btn btn-secondary" @click="resetForm">
        Reset
      </button>
    </form>
    <div v-if="errorMessage" class="alert alert-danger mt-3">
      {{ errorMessage }}
    </div>
    <div v-if="successMessage" class="alert alert-success mt-3">
      {{ successMessage }}
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      serviceName: "",
      serviceDescription: "",
      servicePrice: "",
      errorMessage: null,
      successMessage: null,
    };
  },
  methods: {
    async submitForm() {
      const token = localStorage.getItem("token"); // Retrieve token from localStorage
      if (!token) {
        this.errorMessage = "Authentication token is missing. Please log in.";
        return;
      }

      const data = {
        name: this.serviceName,
        description: this.serviceDescription,
        base_price: this.servicePrice,
      };

      try {
        const response = await fetch("http://127.0.0.1:5000/create_service", {
          method: "POST",
          headers: {
            Authorization: `Bearer ${token}`, // Include JWT token in the request header
            "Content-Type": "application/json",
          },
          body: JSON.stringify(data),
        });

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.message || "An error occurred.");
        }

        const responseData = await response.json();
        this.successMessage = responseData.message;
        this.errorMessage = null;
        this.resetForm(); // Reset form after successful submission
      } catch (error) {
        this.successMessage = null;
        this.errorMessage = error.message || "An error occurred. Please try again.";
      }
    },
    resetForm() {
      this.serviceName = "";
      this.serviceDescription = "";
      this.servicePrice = "";
      this.errorMessage = null;
      this.successMessage = null;
    },
  },
};
</script>

<style scoped>
.container {
  margin-top: 50px;
}
.alert {
  margin-top: 20px;
}
</style>
