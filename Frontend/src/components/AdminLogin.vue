<template>
  <div class="container">
    <div class="row justify-content-center mt-5">
      <div class="col-md-6">
        <h2 class="text-center">Admin Login</h2>
        <form @submit.prevent="submitLogin">
          <div class="form-group">
            <label for="username">Username</label>
            <input
              type="text"
              v-model="username"
              id="username"
              class="form-control"
              placeholder="Enter username"
              required
            />
          </div>
          <div class="form-group">
            <label for="password">Password</label>
            <input
              type="password"
              v-model="password"
              id="password"
              class="form-control"
              placeholder="Enter password"
              required
            />
          </div>
          <button type="submit" class="btn btn-primary btn-block">Login</button>
        </form>

        <!-- Display error message if credentials are wrong -->
        <div v-if="error" class="alert alert-danger mt-3">{{ error }}</div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      username: "",
      password: "",
      error: "",
    };
  },
  methods: {
    async submitLogin() {
      const loginData = {
        username: this.username,
        password: this.password,
      };

      try {
        const response = await fetch("/api/admin_login", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(loginData),
        });

        const result = await response.json();

        if (response.ok) {
          localStorage.setItem("token", result.token);
          // Redirect to admin dashboard
          this.$router.push('/admin_dashboard'); // Path-based redirection
        } else {
          this.error = result.message || "Invalid credentials. Please try again.";
        }
      } catch (error) {
        console.error("Login failed:", error);
        this.error = "An error occurred. Please try again.";
      }
    },
  },
};
</script>

<style scoped>

</style>
