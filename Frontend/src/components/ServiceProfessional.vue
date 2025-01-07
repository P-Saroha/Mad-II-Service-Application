<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-6">
        <div class="card">
          <div class="card-header text-center">
            <h3>Create Service Professional Account</h3>
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

              <!-- Service ID -->
              <div class="form-group mt-3">
                <label for="service_id">Service:</label>
                <select
                  id="service_id"
                  v-model="service_id"
                  class="form-control"
                  required
                >
                  <option v-for="service in services" :key="service.id" :value="service.id">
                    {{ service.name }}
                  </option>
                </select>
              </div>

              <!-- Experience -->
              <div class="form-group mt-3">
                <label for="experience">Experience:</label>
                <input
                  type="text"
                  id="experience"
                  v-model="experience"
                  class="form-control"
                  required
                  placeholder="Enter years of experience"
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
                <label for="mobile_no">Mobile:</label>
                <input
                  type="text"
                  id="mobile_no"
                  v-model="mobile_no"
                  class="form-control"
                  required
                  placeholder="Enter mobile number"
                />
              </div>

              <!-- Resume File -->
              <div class="form-group mt-3">
                <label for="resume_file">Resume (PDF, DOC, DOCX):</label>
                <input
                  type="file"
                  id="resume_file"
                  @change="handleFileUpload"
                  class="form-control"
                  required
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
      service_id: "",
      experience: "",
      address: "",
      pincode: "",
      mobile_no: "",
      resume_file: null,
      services: [],
      message: "",
      messageClass: "",
    };
  },
  created() {
    // Fetch services when the component is created
    this.fetchServices();
  },
  methods: {
    async fetchServices() {
      try {
        const response = await fetch("http://127.0.0.1:5000/get_services"); // Ensure correct endpoint
        const data = await response.json();
        this.services = data.services;
      } catch (error) {
        console.error("Error fetching services:", error);
      }
    },
    handleFileUpload(event) {
      this.resume_file = event.target.files[0]; // Capture the uploaded file
    },
    async submitForm() {
      const formData = new FormData();
      formData.append("username", this.username);
      formData.append("email", this.email);
      formData.append("password", this.password);
      formData.append("service_id", this.service_id);
      formData.append("experience", this.experience);
      formData.append("address", this.address);
      formData.append("pincode", this.pincode);
      formData.append("mobile_no", this.mobile_no);
      if (this.resume_file) {
        formData.append("resume_file", this.resume_file); // Append the file to FormData
      }

      try {
        const response = await fetch("http://127.0.0.1:5000/service_professional_signup", { // Correct endpoint
          method: "POST",
          body: formData,
        });

        const result = await response.json();

        if (result.success) {
          this.message = result.message;
          this.messageClass = "alert-success";
          setTimeout(() => {
            this.$router.push("/login");
          }, 2000);
        } else {
          this.message = result.message;
          this.messageClass = "alert-danger";
        }
      } catch (error) {
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
  margin: auto;  /* Center the card */
}
.card-header {
  background-color: #007bff;
  color: white;
}
</style>
