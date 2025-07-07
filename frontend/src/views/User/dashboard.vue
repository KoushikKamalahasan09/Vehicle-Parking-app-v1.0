<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { requireNonAdminAccess } from '@/utils/auth'

const lots = ref([])
const router = useRouter()

const token = localStorage.getItem('token')
const userId = localStorage.getItem('user_id')

// Fetch all parking lots
const fetchLots = async () => {
  try {
    const response = await fetch('http://127.0.0.1:5000/lots', {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })

    if (response.status === 401) {
      router.push('/login')
      return
    }

    const data = await response.json()
    lots.value = data.lots || []
  } catch (error) {
    console.error('Failed to fetch lots:', error)
  }
}

const bookSpot = async (lotId) => {
  const confirmBook = confirm('Do you want to book the first available spot in this lot?')
  if (!confirmBook) return

  try {
    const response = await fetch('http://127.0.0.1:5000/reservations', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`
      },
      body: JSON.stringify({
        user_id: Number(userId),
        lot_id: Number(lotId)
      })
    })

    const data = await response.json()

    if (response.ok) {
      alert(`Reservation successful! Spot: ${data.spot_number}`)
    } else {
      alert(data.msg || 'Failed to book spot')
    }
  } catch (error) {
    console.error('Error booking spot:', error)
    alert('Something went wrong while booking.')
  }
}

onMounted(() => {
  fetchLots()
  requireNonAdminAccess(router)
})
</script>

<template>
  <div style="padding: 2rem; font-family: Arial, sans-serif;">
    <h1 style="margin-bottom: 1rem;">Available Parking Lots</h1>

    <!-- Parking Lot Cards -->
    <div v-if="lots.length > 0">
      <div
        v-for="lot in lots"
        :key="lot.id"
        style="background-color: #f9f9f9; border: 1px solid #ddd; padding: 1rem 1.5rem; margin-bottom: 1.5rem; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);"
      >
        <h2 style="margin: 0 0 0.5rem;">{{ lot.location_name }}</h2>
        <p><strong>Address:</strong> {{ lot.address }}</p>
        <p><strong>Pin Code:</strong> {{ lot.pin_code }}</p>
        <p><strong>Price per Hour:</strong> ₹{{ lot.price_per_hour }}</p>
        <p><strong>Total Spots:</strong> {{ lot.number_of_spots }}</p>

        <!-- Book Button -->
        <div style="margin-top: 1rem;">
          <button @click="() => bookSpot(lot.id)">Book Spot</button>
        </div>
      </div>
    </div>

    <!-- No lots -->
    <div v-else>
      <p>No parking lots available.</p>
    </div>
  </div>
</template>

<style scoped>
button {
  background-color: #ffffff;
  border: 1px solid #bbb;
  padding: 6px 12px;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

button:hover {
  background-color: #f0f0f0;
}
</style>
