import { createRouter, createWebHistory } from 'vue-router';
import UserLogin from './components/UserLogin.vue';
import UserRegister from '@/components/UserRegister.vue';
import HomePage from '@/components/HomePage.vue';  
import CustomerSignup from './components/CustomerSignup.vue';
import ServiceProfessional from './components/ServiceProfessional.vue';
import ProfessionalDashboard from './components/ProfessionalDashboard.vue';
import ProfessionalSearch from './components/ProfessionalSearch.vue';
import ProfessionalSummary from './components/ProfessionalSummary.vue';
import AdminLogin from './components/AdminLogin.vue';
import AdminDashboard from './components/AdminDashboard.vue';
import AdminSearch from './components/AdminSearch.vue';
import AdminSummary from './components/AdminSummary.vue';
import CustomerDashboard from './components/CustomerDashboard.vue';
import CustomerSearch from './components/CustomerSearch.vue'; 
import CustomerSummary from './components/CustomerSummary.vue';
import CreateService from './components/CreateService.vue';
import EditService from './components/EditService.vue';
import BookService from './components/BookService.vue';

const routes = [
  { path: '/login', name: 'UserLogin', component: UserLogin },
  { path: '/register', name: 'UserRegister', component: UserRegister },
  { path: '/', name: 'HomePage', component: HomePage },
  { path: '/customer_signup', name: 'CustomerSignup', component: CustomerSignup },

  { path: '/service_professional_signup', name: 'ServiceProfessional', component: ServiceProfessional },
  { path: '/professional_dashboard', name: 'ProfessionalDashboard', component: ProfessionalDashboard },
  { path: '/service_professional_search', name: 'ProfessionalSearch', component: ProfessionalSearch },
  { path: '/professional_summary', name: 'ProfessionalSummary', component: ProfessionalSummary },
  
  { path: '/admin_login', name: 'AdminLogin', component: AdminLogin },
  { path: '/admin_dashboard', name: 'AdminDashboard', component: AdminDashboard },
  { path: '/create_service', name: 'CreateService', component: CreateService },
  { path: '/edit_service/:service_id', name: 'EditService', component: EditService },
  { path: '/admin_search', name: 'AdminSearch', component: AdminSearch },
  { path: '/admin_summary', name: 'AdminSummary', component: AdminSummary },

  
  { path: '/customer_dashboard', name: 'CustomerDashboard', component: CustomerDashboard },
  { path: '/customer_search', name: 'CustomerSearch', component: CustomerSearch },
  { path: '/book_service/:service_id', name: 'BookService', component: BookService },
  { path: '/customer_summary', name: 'CustomerSummary', component: CustomerSummary },

];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
