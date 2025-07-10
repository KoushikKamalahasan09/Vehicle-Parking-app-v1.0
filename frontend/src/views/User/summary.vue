<script setup>
import { onMounted, ref } from 'vue'
import { Chart, registerables } from 'chart.js'

Chart.register(...registerables)

const token = localStorage.getItem('token')
const reservations = ref([])
const totalHours = ref(0)
const totalAmount = ref(0)
const chartInstance = ref(null)
const userId = localStorage.getItem('user_id')


const fetchReservations = async () => {
  try {
    const res = await fetch('http://localhost:5000/reservations', {
      headers: { Authorization: `Bearer ${token}` }
    })
    const data = await res.json()
    reservations.value = data.reservations || []

    calculateStats()
    renderChart()
  } catch (err) {
    console.error("Failed to fetch reservations:", err)
  }
}

const calculateStats = () => {
  let hours = 0, amount = 0
  reservations.value.forEach(r => {
    if (!r.leaving_timestamp) return  // ✅ Skip active reservations

    const start = new Date(r.parking_timestamp)
    const end = new Date(r.leaving_timestamp)
    const diff = (end - start) / (1000 * 60 * 60)
    
    if (!isNaN(diff)) {
      hours += diff
      amount += r.parking_cost || 0
    }
  })

  totalHours.value = hours.toFixed(2)
  totalAmount.value = amount.toFixed(2)
}

const downloadCsv = async () => {
  try {
    const res = await fetch(`http://localhost:5000/generate_report/${userId}`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    const data = await res.json()

    if (res.ok) {
      alert(data.msg || 'Report generation started.')
      if (data.url) {
        // optional delay
        setTimeout(() => {
          window.open(data.url, '_blank')
        }, 2000)
      }
    } else {
      alert(data.msg || 'Failed to generate report.')
    }
  } catch (err) {
    console.error('CSV Download Error:', err)
    alert('Server error')
  }
}


const renderChart = () => {
  const ctx = document.getElementById('reservationChart')
  if (chartInstance.value) chartInstance.value.destroy()

  const lotCounts = {}

  reservations.value.forEach(r => {
    const lot = r.lot_location || "Unknown Lot"
    lotCounts[lot] = (lotCounts[lot] || 0) + 1
  })

  const labels = Object.keys(lotCounts)
  const values = labels.map(label => lotCounts[label])

  chartInstance.value = new Chart(ctx, {
    type: 'bar',
    data: {
      labels,
      datasets: [{
        label: 'Reservation Count',
        data: values,
        backgroundColor: '#4e73df'
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: { display: false },
        title: {
          display: true,
          text: 'Reservations per Parking Lot'
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


onMounted(fetchReservations)
</script>

<template>
  <div class="summary-container">
    <h1>User Parking Summary</h1>

    <div class="summary-boxes">
      <div class="summary-box">
        <h3>Total Reservations</h3>
        <p>{{ reservations.length }}</p>
      </div>
      <div class="summary-box">
        <h3>Total Hours Parked</h3>
        <p>{{ totalHours }}</p>
      </div>
      <div class="summary-box">
        <h3>Total Amount Spent</h3>
        <p>₹ {{ totalAmount }}</p>
      </div>
      <div style="text-align: center; margin-top: 1.5rem;">
        <button class="csv-button" @click="downloadCsv">Download Full CSV Report</button>
      </div>
    </div>

    <div class="chart-container">
      <canvas id="reservationChart"></canvas>
    </div>
  </div>
</template>

<style scoped>
.summary-container {
  max-width: 960px;
  margin: 2rem auto;
  padding: 2rem;
  background: #f6f9fc;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
}

h1 {
  text-align: center;
  font-size: 2rem;
  color: #2c3e50;
  margin-bottom: 2rem;
}

.summary-boxes {
  display: flex;
  justify-content: space-between;
  gap: 1.5rem;
  flex-wrap: wrap;
  margin-bottom: 2rem;
}

.summary-box {
  flex: 1;
  background: #ffffff;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
  text-align: center;
  transition: transform 0.3s ease;
  min-width: 200px;
}

.summary-box:hover {
  transform: translateY(-5px);
}

.summary-box h3 {
  font-size: 1.2rem;
  margin-bottom: 0.5rem;
  color: #34495e;
}

.summary-box p {
  font-size: 1.6rem;
  font-weight: bold;
  color: #2980b9;
}

.chart-container {
  background: #ffffff;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
  animation: fadeInUp 0.4s ease;
}

canvas {
  width: 100% !important;
  height: 400px !important;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
.csv-button {
  background-color: #28a745;
  color: white;
  border: none;
  padding: 0.6rem 1.2rem;
  font-size: 1rem;
  border-radius: 6px;
  cursor: pointer;
  transition: background 0.2s ease;
}

.csv-button:hover {
  background-color: #218838;
}

.lot-summary-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 1.5rem;
  margin-top: 1.5rem;
  justify-content: center;
}

.lot-summary-box {
  background: #ffffff;
  padding: 1rem 1.2rem;
  border-radius: 8px;
  min-width: 200px;
  box-shadow: 0 1px 6px rgba(0, 0, 0, 0.08);
  text-align: center;
}

.lot-summary-box h4 {
  color: #2c3e50;
  margin-bottom: 0.5rem;
}


</style>
