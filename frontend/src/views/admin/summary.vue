<script setup>
import { onMounted, ref } from 'vue'
import { Chart, registerables } from 'chart.js'

Chart.register(...registerables)

const token = localStorage.getItem('token')
const reservations = ref([])
const totalRevenue = ref(0)
const totalReservations = ref(0)
const totalUsers = ref(0)
const chartInstance = ref(null)

const fetchReservations = async () => {
  try {
    const res = await fetch('http://localhost:5000/reservations', {
      headers: { Authorization: `Bearer ${token}` }
    })
    const data = await res.json()
    reservations.value = data.reservations || []

    calculateSummary()
    renderChart()
  } catch (err) {
    console.error("Failed to fetch reservations:", err)
  }
}

const fetchUserCount = async () => {
  try {
    const res = await fetch('http://localhost:5000/users/count', {
      headers: { Authorization: `Bearer ${token}` }
    })
    const data = await res.json()
    totalUsers.value = data.total_users || 0
  } catch (err) {
    console.error("Failed to fetch user count:", err)
  }
}

const calculateSummary = () => {
  let revenue = 0
  reservations.value.forEach(r => {
    revenue += r.parking_cost || 0
  })

  totalReservations.value = reservations.value.length
  totalRevenue.value = revenue.toFixed(2)
}

const renderChart = () => {
  const ctx = document.getElementById('globalChart')
  if (chartInstance.value) chartInstance.value.destroy()

  const lotCounts = {}

  reservations.value.forEach(r => {
    const lot = r.lot_location || 'Unknown Lot'
    lotCounts[lot] = (lotCounts[lot] || 0) + 1
  })

  const labels = Object.keys(lotCounts)
  const values = labels.map(label => lotCounts[label])

  chartInstance.value = new Chart(ctx, {
    type: 'bar',
    data: {
      labels,
      datasets: [{
        label: 'Total Reservations per Lot',
        data: values,
        backgroundColor: '#2563eb'
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: { display: false },
        title: {
          display: true,
          text: 'Reservations per Parking Lot',
          font: { size: 18 }
        }
      },
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  })
}

const downloadAdminReport = async () => {
  try {
    const res = await fetch('http://localhost:5000/generate_report/1', {
      headers: { Authorization: `Bearer ${token}` }
    })
    const data = await res.json()
    if (res.ok) {
      alert('Report generation started. Please check your static folder or download shortly.')
      window.open(data.url, '_blank')
    } else {
      alert(data.msg || 'Failed to generate report')
    }
  } catch (err) {
    console.error('Report fetch failed:', err)
    alert('Server error')
  }
}

onMounted(() => {
  fetchReservations()
  fetchUserCount()
})
</script>


<template>
  <div class="summary-container">
    <h1>Admin Summary Dashboard</h1>

    <div class="summary-boxes">
      <div class="summary-box">
        <h3>Total Reservations</h3>
        <p>{{ totalReservations }}</p>
      </div>
      <div class="summary-box">
        <h3>Total Users</h3>
        <p>{{ totalUsers }}</p>
      </div>
      <div class="summary-box">
        <h3>Total Revenue</h3>
        <p>₹ {{ totalRevenue }}</p>
      </div>
      <div style="text-align: center; margin-bottom: 1.5rem;">
        <button class="download-btn" @click="downloadAdminReport">
          Download Full Reservation Report (CSV)
        </button>
      </div>
    </div>

    <div class="chart-wrapper">
      <canvas id="globalChart"></canvas>
    </div>
  </div>
</template>

<style scoped>
.summary-container {
  padding: 2.5rem;
  font-family: 'Segoe UI', sans-serif;
  background-color: #f4f7fa;
  min-height: 100vh;
}

h1 {
  font-size: 2rem;
  margin-bottom: 2rem;
  color: #1f2937;
  text-align: center;
}

.summary-boxes {
  display: flex;
  flex-wrap: wrap;
  gap: 1.5rem;
  margin-bottom: 2.5rem;
  justify-content: center;
}

.summary-box {
  flex: 1;
  min-width: 220px;
  background: #ffffff;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 3px 12px rgba(0, 0, 0, 0.08);
  text-align: center;
  transition: transform 0.2s ease;
}

.summary-box:hover {
  transform: translateY(-3px);
}

.summary-box h3 {
  margin-bottom: 0.5rem;
  font-size: 1.2rem;
  color: #374151;
}

.summary-box p {
  font-size: 1.6rem;
  font-weight: bold;
  color: #111827;
}

.chart-wrapper {
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.08);
}

.download-btn {
  background-color: #2563eb;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.download-btn:hover {
  background-color: #1d4ed8;
}

</style>
