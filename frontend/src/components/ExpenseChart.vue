<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import {
    Chart as ChartJS,
    Title,
    Tooltip,
    Legend,
    BarElement,
    CategoryScale,
    LinearScale
} from 'chart.js'
import { Bar } from 'vue-chartjs'
import { getStatistics } from '../services/api'
import type { AggregatedData } from '../types'

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend)

const rawData = ref<AggregatedData[]>([])
const loading = ref(true)

const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
        legend: { display: false },
        title: {
            display: true,
            text: 'Total de Despesas por Estado (R$)'
        }
    }
}

const chartData = computed(() => {
    const expensesByState: Record<string, number> = {}

    rawData.value.forEach(item => {
        const estado = item.state || 'Outros';
        const valor = Number(item.total_amount);

        if (expensesByState[estado]) {
            expensesByState[estado] += valor;
        } else {
            expensesByState[estado] = valor;
        }
    });

    const sortedStates = Object.entries(expensesByState)
        .sort(([, a], [, b]) => b - a)

    const labels = sortedStates.map(([uf]) => uf)
    const data = sortedStates.map(([, total]) => total)

    return {
        labels: labels,
        datasets: [
            {
                label: 'Despesas Totais',
                backgroundColor: '#007bff',
                data: data
            }
        ]
    }
})

onMounted(async () => {
    try {
        const response = await getStatistics()
        rawData.value = response.data
    } catch (error) {
        console.error("Erro ao carregar estatísticas:", error)
    } finally {
        loading.value = false
    }
})
</script>

<template>
    <div class="chart-wrapper">
        <div v-if="loading" class="loading-chart">Carregando gráfico...</div>
        <div v-else-if="rawData.length === 0" class="no-data">Sem dados para exibir</div>

        <Bar v-else :data="chartData" :options="chartOptions" />
    </div>
</template>

<style scoped>
.chart-wrapper {
    position: relative;
    height: 300px;
    width: 100%;
}

.loading-chart,
.no-data {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 100%;
    color: #666;
    font-style: italic;
}
</style>