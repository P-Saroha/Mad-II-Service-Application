<template>
  <div class="container mt-5 text-center">
    <div class="signup-box">
      <h1>Register</h1>
      <p>Choose your role to proceed with registration:</p>

      <div class="mt-4">
        <!-- Button for Customer Signup -->
        <router-link to="/customer_signup">
          <button class="btn btn-primary me-3">Sign up as Customer</button>
        </router-link>

        <!-- Button for Service Professional Signup -->
        <router-link to="/service_professional_signup">
          <button class="btn btn-secondary">Sign up as Service Professional</button>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "RegisterPage",
};
</script>

<style scoped>
/* Center alignment */
.container {
  max-width: 500px;
  margin: auto;
}

/* Simple box styling */
.signup-box {
  padding: 30px;
  background-color: #f8f9fa;
  border: 1px solid #ddd;
  border-radius: 8px;
}

h1 {
  font-size: 24px;
  margin-bottom: 20px;
}

p {
  font-size: 16px;
  margin-bottom: 30px;
}

button {
  padding: 10px 20px;
  font-size: 16px;
  border-radius: 4px;
  border: none;
}

.btn-primary {
  background-color: #007bff;
  color: white;
}

.btn-secondary {
  background-color: #6c757d;
  color: white;
}

/* Margin on the right of the first button */
.me-3 {
  margin-right: 1rem !important;
  margin-bottom: 1.5rem;
}
</style>
