<template>
  <div class="container mt-5">
    <h1 class="text-center">Login</h1>

    <!-- Flash messages if any -->
    <div v-if="flashMessages.length" class="mt-3">
      <ul class="list-unstyled">
        <li
          v-for="(message, index) in flashMessages"
          :key="index"
          class="alert alert-danger"
        >
          {{ message }}
        </li>
      </ul>
    </div>

    <!-- Login Form -->
    <form @submit.prevent="handleSubmit">
      <div class="mb-3">
        <label for="email" class="form-label">Email:</label>
        <input
          type="email"
          id="email"
          class="form-control"
          v-model="email"
          required
          placeholder="Enter your email"
        />
      </div>
      <div class="mb-3">
        <label for="password" class="form-label">Password:</label>
        <input
          type="password"
          id="password"
          class="form-control"
          v-model="password"
          required
          placeholder="Enter your password"
        />
      </div>
      <div class="mb-3">
        <label for="role" class="form-label">Login as:</label>
        <select class="form-select" v-model="role" required>
          <option value="Customer">Customer</option>
          <option value="ServiceProfessional">Service Professional</option>
        </select>
      </div>
      <button type="submit" class="btn btn-primary w-100">Login</button>
    </form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      email: '',
      password: '',
      role: '',
      flashMessages: [],
    }
  },
  methods: {
    async handleSubmit() {
      try {
        // Send a POST request to the backend login route
        const response = await fetch('/api/login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            email: this.email,
            password: this.password,
            role: this.role,
          }),
        })

        const data = await response.json()

        // Check if login is successful
        if (response.ok) {
          // Store the token in localStorage
          localStorage.setItem('token', data.token)

          // Redirect user based on the role
          if (this.role === 'Customer') {
            this.$router.push('/customer_dashboard')
          } else if (this.role === 'ServiceProfessional') {
            this.$router.push('/professional_dashboard')
          }
        } else {
          // Show flash messages if login fails
          this.flashMessages = [
            data.message || 'Login failed. Please try again.',
          ]
        }
      } catch (error) {
        // Handle any errors
        const errorMessage = 'An unexpected error occurred. Please try again.'
        this.flashMessages = [errorMessage]
        console.error(error)
      }
    },
  },
}
</script>

<style scoped>
/* Add any custom styles you may need here */
</style>