<template>
  <div>
    <!-- Navigation Bar -->
    <nav class="navbar navbar-expand-lg">
      <div class="container-fluid">
        <h3>Household Services</h3>
        <button
          class="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarNav"
          aria-controls="navbarNav"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav ms-auto">
            <li class="nav-item">
              <router-link class="nav-link" to="/login">Login</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/admin_login">Admin Login</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/register">Register</router-link>
            </li>
          </ul>
        </div>
      </div>
    </nav>

    <!-- Services We Provide Section -->
    <div class="services-section">
      <div class="container">
        <h2>Services We Provide</h2>
        <div class="row">
          <div
            v-for="(service, index) in services"
            :key="index"
            class="col-md-4"
          >
            <div class="card">
              <div class="card-body">
                <h5 class="card-title">{{ service.title }}</h5>
                <p class="card-text">{{ service.description }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Footer Section -->
    <footer>
      <p>&copy; 2024 Household Services. All Rights Reserved.</p>
    </footer>
  </div>
</template>

<script>
export default {
  name: "HomePage",  // Updated component name
  data() {
    return {
      services: [
        {
          title: "Cleaning Services",
          description:
            "We offer professional cleaning services for your home. From deep cleaning to regular maintenance, our team ensures your home stays fresh and tidy."
        },
        {
          title: "Plumbing Services",
          description:
            "Our expert plumbers can handle any household plumbing issue, from leaky faucets to major installations, complex repairs, and maintenance. We've got you covered."
        },
        {
          title: "Electrical Services",
          description:
            "Our licensed electricians provide safe and reliable electrical repairs, installations, and upgrades to ensure your home is running smoothly."
        },
        {
          title: "Home Repairs",
          description:
            "From fixing broken appliances to repairing structural issues, our team offers comprehensive home repair services to keep your house in top shape."
        },
        {
          title: "Gardening Services",
          description:
            "Our gardening experts provide lawn care, landscaping, and garden maintenance services to keep your outdoor spaces beautiful and well-maintained."
        },
        {
          title: "Painting Services",
          description:
            "Whether it's a fresh coat of paint for your home or decorative touch-ups, our painting team offers professional services that enhance the look of your property."
        }
      ]
    };
  },
  methods: {
    fetchHomeData() {
      fetch("/")
        .then(response => response.json())
        .then(data => {
          // Assuming you receive a JSON response from the server
          // Update local state with the data if needed
          console.log(data);
        })
        .catch(error => console.error("Error fetching data:", error));
    }
  },
  mounted() {
    this.fetchHomeData();
  }
};
</script>

<style scoped>
body {
  background-image: url('static/hh_3.jpg');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  height: 100vh;
  font-family: 'Arial', sans-serif;
  color: #fff;
}

.navbar {
  background-color: #e47cac;
  padding: 0.75rem 2rem;
}

.navbar-brand {
  color: #ffffff;
  font-size: 1.5rem;
  font-weight: bold;
  margin-right: 2rem;
}

.nav-link {
  color: #ffffff !important;
  margin-right: 20px;
  font-size: 1.1rem;
  transition: color 0.3s ease;
}

.nav-link:hover {
  color: #73ff48 !important;
}

.services-section {
  padding: 50px 0;
  margin-top: 20px;
}

.services-section h2 {
  text-align: center;
  color: #73ff48;
  margin-bottom: 30px;
  font-size: 2rem;
}

.card {
  border: none;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  margin-bottom: 30px;
}

.card-title {
  color: #e47cac;
  font-size: 1.5rem;
}

.card-body p {
  color: #333;
  font-size: 1.1rem;
}

footer {
  background-color: #e47cac;
  color: #fff;
  padding: 10px 0;
  text-align: center;
  width: 100%;
}
</style>
