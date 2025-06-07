<template>
  <div class="container">
    <h1>Edit Service</h1>
    <form @submit.prevent="editService">
      <div class="form-group">
        <label for="name">Service Name</label>
        <input
          type="text"
          class="form-control"
          id="name"
          v-model="service.name"
          required
          placeholder="Enter service name"
        />
      </div>
      <div class="form-group">
        <label for="description">Description</label>
        <textarea
          class="form-control"
          id="description"
          v-model="service.description"
          required
          placeholder="Enter service description"
        ></textarea>
      </div>
      <div class="form-group">
        <label for="base_price">Base Price</label>
        <input
          type="number"
          class="form-control"
          id="base_price"
          v-model="service.base_price"
          required
          placeholder="Enter base price"
        />
      </div>
      <button type="submit" class="btn btn-primary">Update</button>
      <router-link to="/admin_dashboard" class="btn btn-secondary">Back to Dashboard</router-link>
    </form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      service: {
        name: "",
        description: "",
        base_price: "",
      },
    };
  },
  methods: {
    async fetchServiceDetails() {
      const serviceId = this.$route.params.service_id; // Get the service ID from the route
      const token = localStorage.getItem("token"); // Fetch the token from localStorage

      if (!serviceId) {
        alert("Service ID is missing.");
        this.$router.push("/api/admin_dashboard");
        return;
      }

      try {
        const response = await fetch(`/api/get_service/${serviceId}`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        if (response.ok) {
          this.service = await response.json();
        } else {
          alert("Failed to fetch service details.");
          this.$router.push("/admin_dashboard");
        }
      } catch (error) {
        console.error("Error fetching service details:", error);
        alert("An error occurred while fetching the service details.");
        this.$router.push("/admin_dashboard");
      }
    },
    async editService() {
      const serviceId = this.$route.params.service_id; // Get the service ID from the route
      const token = localStorage.getItem("token"); // Fetch the token from localStorage

      try {
        const response = await fetch(`/api/edit_service/${serviceId}`, {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify(this.service),
        });

        if (response.ok) {
          alert("Service updated successfully!");
          this.$router.push("/admin_dashboard");
        } else {
          const errorData = await response.json();
          alert(errorData.message || "Failed to update service.");
        }
      } catch (error) {
        console.error("Error updating service:", error);
        alert("An error occurred while updating the service.");
      }
    },
  },
  mounted() {
    this.fetchServiceDetails(); // Fetch service details on component mount
  },
};
</script>

<style>

</style>
