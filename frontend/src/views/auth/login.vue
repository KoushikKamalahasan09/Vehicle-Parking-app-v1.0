<template>
  <div class="login-container">
    <h2>Login to Your Account</h2>

    <form @submit.prevent="handleLogin">
      <div class="form-group">
        <label for="email">Email</label>
        <input
          v-model="email"
          type="email"
          id="email"
          name="email"
          required
          placeholder="you@example.com"
        />
      </div>

      <div class="form-group">
        <label for="password">Password</label>
        <input
          v-model="password"
          type="password"
          id="password"
          name="password"
          required
          placeholder="Enter your password"
        />
      </div>

      <button type="submit" class="btn" :disabled="isLoading">
        {{ isLoading ? 'Logging in...' : 'Login' }}
      </button>
    </form>

    <p class="register-link">
      Don't have an account?
      <router-link to="/register">Click here to register</router-link>
    </p>
  </div>
</template>

<script>
export default {
  name: 'LoginPage',
  data() {
    return {
      email: '',
      password: '',
      isLoading: false
    };
  },
  methods: {
    async handleLogin() {
      this.isLoading = true;
      const postData = { email: this.email, password: this.password };

      try {
        const response = await fetch('http://localhost:5000/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(postData)
        });

        if (!response.ok) {
          if (response.status === 404) {
            alert('Account does not exist. Please register first.');
          } else if (response.status === 401) {
            alert('Invalid credentials.');
          } else {
            alert(`Login failed with status ${response.status}`);
          }
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();

        localStorage.setItem('token', data.token);
        localStorage.setItem('user_id', data.user_id);
        localStorage.setItem('isadmin', data.isadmin);

        if (data.isadmin) {
          this.$router.push('/admin/dashboard');
        } else {
          this.$router.push('/dashboard');
        }

      } catch (error) {
        console.error('Login failed:', error);
      } finally {
        this.isLoading = false;
      }
    }
  },
  mounted() {
    // Auto-redirect if already logged in
    const token = localStorage.getItem('token');
    const isAdmin = localStorage.getItem('isadmin');

    if (token) {
      if (isAdmin === 'true') {
        this.$router.push('/admin/dashboard');
      } else {
        this.$router.push('/dashboard');
      }
    }
  }
};
</script>

<style scoped>
.login-container {
  max-width: 400px;
  margin: auto;
  padding: 2rem;
  border-radius: 8px;
  background-color: #f9f9f9;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

h2 {
  text-align: center;
  margin-bottom: 1.5rem;
}

.form-group {
  margin-bottom: 1.2rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
}

input {
  width: 100%;
  padding: 0.6rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 1rem;
}

.btn {
  width: 100%;
  padding: 0.7rem;
  background-color: #4caf50;
  color: white;
  font-size: 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.btn:hover {
  background-color: #45a049;
}

.btn:disabled {
  background-color: #a5d6a7;
  cursor: not-allowed;
}

.register-link {
  text-align: center;
  margin-top: 1rem;
}

.register-link a {
  color: #007bff;
  text-decoration: none;
}

.register-link a:hover {
  text-decoration: underline;
}
</style>
