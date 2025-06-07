<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-6">
        <div class="card">
          <div class="card-header text-center">
            <h3>Create Customer Account</h3>
          </div>
          <div class="card-body">
            <!-- Success or Error Message -->
            <div v-if="message" :class="['alert', messageClass]" role="alert">
              {{ message }}
            </div>

            <form @submit.prevent="submitForm">
              <!-- Username -->
              <div class="form-group">
                <label for="username">Username:</label>
                <input
                  type="text"
                  id="username"
                  v-model="username"
                  class="form-control"
                  required
                  placeholder="Enter username"
                />
              </div>

              <!-- Email -->
              <div class="form-group mt-3">
                <label for="email">Email:</label>
                <input
                  type="email"
                  id="email"
                  v-model="email"
                  class="form-control"
                  required
                  placeholder="Enter email"
                />
              </div>

              <!-- Password -->
              <div class="form-group mt-3">
                <label for="password">Password:</label>
                <input
                  type="password"
                  id="password"
                  v-model="password"
                  class="form-control"
                  required
                  placeholder="Enter password"
                />
              </div>

              <!-- Address -->
              <div class="form-group mt-3">
                <label for="address">Address:</label>
                <input
                  type="text"
                  id="address"
                  v-model="address"
                  class="form-control"
                  required
                  placeholder="Enter address"
                />
              </div>

              <!-- Pincode -->
              <div class="form-group mt-3">
                <label for="pincode">Pincode:</label>
                <input
                  type="text"
                  id="pincode"
                  v-model="pincode"
                  class="form-control"
                  required
                  placeholder="Enter pincode"
                />
              </div>

              <!-- Mobile -->
              <div class="form-group mt-3">
                <label for="mobile">Mobile:</label>
                <input
                  type="text"
                  id="mobile"
                  v-model="mobile"
                  class="form-control"
                  maxlength="10"
                  required
                  placeholder="Enter mobile number"
                />
              </div>

              <!-- Submit Button -->
              <button type="submit" class="btn btn-success btn-block mt-4">
                Sign Up
              </button>
            </form>
            <p class="text-center mt-3">
              Already have an account? <router-link to="/login">Login</router-link>
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      username: "",
      email: "",
      password: "",
      address: "",
      pincode: "",
      mobile: "",
      message: "",
      messageClass: "",
    };
  },
  methods: {
    async submitForm() {
      // Prepare payload with user input
      const payload = {
        username: this.username,
        email: this.email,
        password: this.password,
        address: this.address,
        pincode: this.pincode,
        mobile: this.mobile,
      };

      try {
        // Log request data for debugging
        console.log("Sending request with payload:", payload);

        // Make the POST request to the backend
        const response = await fetch("/api/customer_signup", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",  // Ensure Content-Type is application/json
          },
          body: JSON.stringify(payload),
        });

        // Log the response status for debugging
        console.log("Response status:", response.status);

        // Check if the request was successful (HTTP 2xx)
        if (response.ok) {
          // Parse JSON response
          const result = await response.json();
          console.log("Success response:", result);

          this.message = result.message || "Account created successfully!";
          this.messageClass = "alert-success";

          // Redirect after 2 seconds
          setTimeout(() => {
            this.$router.push("/login");
          }, 2000);
        } else {
          // If the request failed, parse the error response
          const errorResult = await response.json();
          console.log("Error response:", errorResult);

          this.message = errorResult.message || "An error occurred. Please try again.";
          this.messageClass = "alert-danger";
        }
      } catch (error) {
        // Log any unexpected errors (like network errors)
        console.error("Error during form submission:", error);

        this.message = "An error occurred. Please try again.";
        this.messageClass = "alert-danger";
      }
    },
  },
};
</script>

<style scoped>
.container {
  max-width: 100%;
}
.card {
  width: 100%;
  max-width: 800px; /* Set a max width */
  margin: auto; /* Center the card */
}
.card-header {
  background-color: #28a745;
  color: white;
}
</style>
