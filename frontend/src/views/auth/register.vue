<template>
  <div class="register-container">
    <h2>Create a New Account</h2>

    <form @submit.prevent="handleRegister">
      <div class="form-group">
        <label for="username">Username</label>
        <input
          v-model="username"
          type="text"
          id="username"
          name="username"
          required
          placeholder="Your username"
        />
      </div>

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
          placeholder="Create a password"
        />
      </div>

      <button type="submit" class="btn" :disabled="isLoading">
        {{ isLoading ? 'Registering...' : 'Register' }}
      </button>
    </form>

    <p class="login-link">
      Already have an account?
      <router-link to="/login">Click here to login</router-link>
    </p>
  </div>
</template>

<script>
export default {
  name: 'RegisterPage',
  data() {
    return {
      username: '',
      email: '',
      password: '',
      isLoading: false
    };
  },
  methods: {
    async handleRegister() {
      this.isLoading = true;

      const postData = {
        username: this.username,
        email: this.email,
        password: this.password
      };

      try {
        const response = await fetch('http://localhost:5000/register', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(postData)
        });

        if (!response.ok) {
          if (response.status === 409) {
            alert('Account already exists. Please login.');
          } else if (response.status === 400) {
            alert('Please provide all required information.');
          } else {
            alert('Registration failed.');
          }
          return;
        }

        alert('Registration successful! You can now login.');
        this.$router.push('/login');

      } catch (error) {
        console.error('Registration error:', error);
        alert('An error occurred. Please try again.');
      } finally {
        this.isLoading = false;
      }
    }
  }
};
</script>

<style scoped>
.register-container {
  max-width: 400px;
  margin: auto;
  padding: 2rem;
  border-radius: 8px;
  background-color: #fdfdfd;
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
  background-color: #008cba;
  color: white;
  font-size: 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.btn:hover {
  background-color: #007bb5;
}

.btn:disabled {
  background-color: #9cd3e5;
  cursor: not-allowed;
}

.login-link {
  text-align: center;
  margin-top: 1rem;
}

.login-link a {
  color: #007bff;
  text-decoration: none;
}

.login-link a:hover {
  text-decoration: underline;
}
</style>
