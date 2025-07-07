<template>
  <div class="home-container">
    <div class="hero">
      <h1>Welcome to ParkEasy</h1>
      <p class="tagline">Find, reserve, and manage your parking spots with ease.</p>

      <div class="auth-buttons">
        <router-link to="/login" class="btn login-btn">Login</router-link>
        <router-link to="/register" class="btn register-btn">Register</router-link>
      </div>
    </div>

    <div class="info-section">
      <h2>Why ParkEasy?</h2>
      <ul>
        <li>🅿️ Easily locate available parking spots near you.</li>
        <li>🕒 Reserve spots ahead of time and avoid the hassle.</li>
        <li>📱 Manage your bookings and view parking history.</li>
        <li>🔐 Secure and reliable service for your vehicle.</li>
      </ul>

      <p class="note">You need to <strong>log in or create an account</strong> to access all features like booking and tracking.</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HomePage',
};
</script>

<style scoped>
.home-container {
  max-width: 900px;
  margin: auto;
  padding: 2rem;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.hero {
  background-color: #e6f7ff;
  padding: 2.5rem 2rem;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
  text-align: center;
}

.hero h1 {
  font-size: 2.2rem;
  margin-bottom: 0.5rem;
  color: #2c3e50;
}

.tagline {
  font-size: 1.25rem;
  margin-top: 1rem;
  color: #555;
}

.auth-buttons {
  margin-top: 2rem;
}

.btn {
  text-decoration: none;
  padding: 0.75rem 1.6rem;
  margin: 0 0.75rem;
  border-radius: 6px;
  font-weight: 600;
  font-size: 1rem;
  display: inline-block;
  transition: background-color 0.3s ease, transform 0.2s ease;
}

.login-btn {
  background-color: #28a745;
  color: white;
}

.login-btn:hover {
  background-color: #218838;
  transform: translateY(-2px);
}

.register-btn {
  background-color: #007bff;
  color: white;
}

.register-btn:hover {
  background-color: #0056b3;
  transform: translateY(-2px);
}

.info-section {
  margin-top: 3rem;
  text-align: left;
  background: #fff;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.06);
}

.info-section h2 {
  margin-bottom: 1rem;
  font-size: 1.6rem;
  color: #2c3e50;
}

.info-section ul {
  list-style: none;
  padding-left: 0;
  margin: 0;
}

.info-section li {
  margin-bottom: 0.75rem;
  font-size: 1.05rem;
  color: #444;
}

.note {
  margin-top: 1.5rem;
  font-style: italic;
  color: #888;
  font-size: 0.95rem;
}

@media (max-width: 600px) {
  .btn {
    display: block;
    margin: 0.75rem auto;
    width: 80%;
    text-align: center;
  }

  .info-section {
    padding: 1.5rem;
  }
}
</style>
