<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { requireNonAdminAccess } from '@/utils/auth'

const router = useRouter()
requireNonAdminAccess(router)

const token = localStorage.getItem('token')
const userId = localStorage.getItem('user_id')

const user = ref({})
const editing = ref(false)
const updatedUsername = ref('')
const updatedEmail = ref('')
const message = ref('')

const fetchProfile = async () => {
  try {
    const res = await fetch(`http://127.0.0.1:5000/users/${userId}`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    const data = await res.json()
    if (res.ok && data.user) {
      user.value = data.user
      updatedUsername.value = data.user.username
      updatedEmail.value = data.user.email
    } else {
      message.value = data.msg || 'Failed to fetch profile.'
    }
  } catch (err) {
    message.value = 'Error fetching profile.'
  }
}

const updateProfile = async () => {
  try {
    const res = await fetch(`http://127.0.0.1:5000/users/${userId}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`
      },
      body: JSON.stringify({
        username: updatedUsername.value,
        email: updatedEmail.value
      })
    })
    const data = await res.json()
    if (res.ok && data.user) {
      user.value = data.user
      message.value = 'Profile updated successfully!'
      editing.value = false
    } else {
      message.value = data.msg || 'Update failed.'
    }
  } catch (err) {
    message.value = 'Error updating profile.'
  }
}

onMounted(fetchProfile)
</script>

<template>
  <div class="profile-container">
    <div class="profile-card">
      <h1>User Profile</h1>

      <p v-if="message" class="status-msg">{{ message }}</p>

      <div v-if="user && user.username && !editing" class="profile-view">
        <p><strong>Username:</strong> {{ user.username }}</p>
        <p><strong>Email:</strong> {{ user.email }}</p>
        <button @click="editing = true" class="btn primary">Update Profile</button>
      </div>

      <div v-else-if="editing" class="profile-edit">
        <label>Username:</label>
        <input v-model="updatedUsername" type="text" />

        <label>Email:</label>
        <input v-model="updatedEmail" type="email" />

        <div class="btn-group">
          <button @click="updateProfile" class="btn success">Save</button>
          <button @click="editing = false" class="btn gray">Cancel</button>
        </div>
      </div>

      <div v-else class="loading">Loading profile...</div>
    </div>
  </div>
</template>

<style scoped>
.profile-container {
  display: flex;
  justify-content: center;
  align-items: flex-start;
  padding: 3rem 1rem;
  background-color: #f0f2f5;
  min-height: 100vh;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.profile-card {
  background: #fff;
  padding: 2rem 2.5rem;
  border-radius: 12px;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.12);
  width: 100%;
  max-width: 500px;
  transition: box-shadow 0.3s ease;
}

.profile-card:hover {
  box-shadow: 0 6px 22px rgba(0, 0, 0, 0.16);
}

h1 {
  font-size: 1.8rem;
  margin-bottom: 1.5rem;
  color: #333;
  text-align: center;
}

.status-msg {
  text-align: center;
  margin-bottom: 1rem;
  color: #c0392b;
  font-weight: 500;
}

.profile-view p {
  margin: 0.75rem 0;
  font-size: 1rem;
  color: #444;
}

.profile-edit label {
  display: block;
  margin-top: 1rem;
  font-weight: 600;
  color: #555;
}

.profile-edit input {
  width: 100%;
  padding: 0.6rem;
  border-radius: 6px;
  border: 1px solid #ccc;
  margin-top: 0.25rem;
  font-size: 1rem;
}

.btn-group {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 1.5rem;
}

.btn {
  padding: 0.6rem 1.2rem;
  border: none;
  border-radius: 6px;
  font-weight: 600;
  font-size: 0.95rem;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.btn.primary {
  background-color: #2563eb;
  color: #fff;
}

.btn.primary:hover {
  background-color: #1d4ed8;
}

.btn.success {
  background-color: #16a34a;
  color: white;
}

.btn.success:hover {
  background-color: #15803d;
}

.btn.gray {
  background-color: #6b7280;
  color: white;
}

.btn.gray:hover {
  background-color: #4b5563;
}

.loading {
  text-align: center;
  color: #777;
  font-style: italic;
  margin-top: 1rem;
}
</style>
