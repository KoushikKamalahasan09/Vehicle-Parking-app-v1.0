<script setup>
import { ref, onMounted } from 'vue'

const token = localStorage.getItem('token')
const userId = localStorage.getItem('user_id')

const currentReservations = ref([])
const pastReservations = ref([])

const fetchReservations = async () => {
  try {
    const res = await fetch('http://localhost:5000/reservations', {
      headers: { Authorization: `Bearer ${token}` }
    })
    const data = await res.json()
    if (res.ok) {
      const all = data.reservations?.filter(r => r.user_id === Number(userId)) || []

      // Updated filtering logic
      currentReservations.value = all.filter(r =>
        r.leaving_timestamp === null || r.leaving_timestamp === 'Still using'
      )
      pastReservations.value = all.filter(r =>
        r.leaving_timestamp !== null && r.leaving_timestamp !== 'Still using'
      )

      console.log("User ID from localStorage:", userId)
      console.log("Fetched reservations:", data.reservations)
      console.log("Current:", currentReservations.value)
      console.log("Past:", pastReservations.value)
    } else {
      alert(data.msg || 'Failed to fetch reservations')
    }
  } catch (err) {
    console.error('Error fetching reservations:', err)
  }
}

const downloadCsv = async (reservationId) => {
  try {
    const res = await fetch(`http://localhost:5000/reservations/${reservationId}/csv`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    const data = await res.json()

    if (res.ok) {
      alert(data.msg || 'CSV requested')
      if (data.url) {
        // Optional: wait a bit if needed
        setTimeout(() => {
          window.open(data.url, '_blank')
        }, 2000)
      }
    } else {
      alert(data.msg || 'Failed to request CSV')
    }
  } catch (err) {
    console.error(err)
    alert('Server error')
  }
}


const endReservation = async (r) => {
  const now = new Date().toISOString()
  try {
    const res = await fetch(`http://localhost:5000/reservations/${r.id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`
      },
      body: JSON.stringify({ leaving_timestamp: now })
    })
    const data = await res.json()
    if (res.ok) {
      alert('Reservation ended')
      fetchReservations()
    } else {
      alert(data.msg || 'End failed')
    }
  } catch (err) {
    console.error(err)
    alert('Server error')
  }
}

const formatDateTime = (isoString) => {
  if (!isoString || isoString === 'Still using') return 'N/A'
  const date = new Date(isoString)
  return isNaN(date)
    ? 'Invalid Date'
    : `${date.toLocaleDateString()} ${date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}`
}

onMounted(fetchReservations)
</script>


<template>
  <div class="container">
    <h2>Current Reservations</h2>
    <div v-if="currentReservations.length" class="grid">
      <div v-for="r in currentReservations" :key="r.id" class="card">
        <p><strong>Spot:</strong> {{ r.spot_number || r.spot_id }}</p>
        <p><strong>From:</strong> {{ formatDateTime(r.parking_timestamp) }}</p>
        <button class="end" @click="endReservation(r)">End</button>
      </div>
    </div>
    <p v-else>No current reservations.</p>

    <h2 style="margin-top: 2rem;">Past Reservations</h2>
    <div v-if="pastReservations.length" class="grid">
      <div v-for="r in pastReservations" :key="r.id" class="card">
        <p><strong>Spot:</strong> {{ r.spot_number || r.spot_id }}</p>
        <p><strong>From:</strong> {{ formatDateTime(r.parking_timestamp) }}</p>
        <p><strong>To:</strong> {{ formatDateTime(r.leaving_timestamp) }}</p>
        <p><strong>Cost:</strong> ₹{{ r.parking_cost }}</p>
        <button class="csv" @click="downloadCsv(r.id)">Download CSV</button>
      </div>
    </div>
    <p v-else>No past reservations.</p>
  </div>
</template>

<style scoped>
.container {
  padding: 2rem;
  font-family: Arial, sans-serif;
}

h2 {
  font-size: 1.5rem;
  margin-bottom: 1rem;
}

.grid {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
}

.card {
  background: #fff;
  padding: 1rem;
  border-radius: 10px;
  box-shadow: 0 2px 6px rgba(0,0,0,0.1);
  flex: 0 0 300px;
}

.end {
  background-color: #dc3545;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  margin-top: 0.5rem;
  border-radius: 6px;
  cursor: pointer;
}
.csv {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 0.4rem 0.8rem;
  margin-top: 0.5rem;
  border-radius: 6px;
  cursor: pointer;
}

</style>
