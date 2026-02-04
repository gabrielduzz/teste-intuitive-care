<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getCompanyByCnpj, getCompanyExpenses } from '../services/api'
import type { Company, Expense } from '../types'

const route = useRoute()
const router = useRouter()

const cnpjParam = route.params.cnpj as string

const company = ref<Company | null>(null)
const expenses = ref<Expense[]>([])
const loading = ref(true)
const error = ref('')

const formatCurrency = (value: number) => {
  if (!value || isNaN(value)) return 'R$ 0,00'
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL'
  }).format(value)
}

const formatDate = (dateString: string) => {
  if (!dateString) return '-'
  return new Date(dateString).toLocaleDateString('pt-BR', {
    day: '2-digit',
    month: 'short',
    year: 'numeric'
  })
}

const totalExpenses = computed(() => {
  if (!expenses.value || expenses.value.length === 0) return 0
  return expenses.value.reduce((sum, expense) => {
    const val = Number(expense.amount);
    return sum + (isNaN(val) ? 0 : val);
  }, 0)
})

const averageExpense = computed(() => {
  if (!expenses.value || expenses.value.length === 0) return 0
  return totalExpenses.value / expenses.value.length
})

const latestExpense = computed(() => {
  if (!expenses.value || expenses.value.length === 0) return null

  const sorted = [...expenses.value].sort((a, b) =>
    new Date(b.reference_date).getTime() - new Date(a.reference_date).getTime()
  )

  return sorted[0]
})

onMounted(async () => {
  try {
    const [companyResponse, expensesResponse] = await Promise.allSettled([
      getCompanyByCnpj(cnpjParam),
      getCompanyExpenses(cnpjParam)
    ])

    if (companyResponse.status === 'fulfilled') {
      company.value = companyResponse.value.data
    } else {
      error.value = "Não foi possível carregar os dados da empresa."
    }

    if (expensesResponse.status === 'fulfilled') {
      expenses.value = expensesResponse.value.data
    } else {
      console.warn("Sem despesas ou erro ao buscar despesas.")
    }

  } catch (err) {
    error.value = "Erro fatal ao conectar com o servidor."
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <main class="container">
    <button @click="router.back()" class="back-btn">
      ← Voltar
    </button>

    <div v-if="loading" class="loading">
      <div class="spinner"></div>
      <p>Carregando...</p>
    </div>

    <div v-else-if="error" class="error-state">
      <h2>Erro ao carregar dados</h2>
      <p>{{ error }}</p>
      <button @click="router.back()" class="btn-primary">Voltar</button>
    </div>

    <div v-else>
      <section class="company-header" v-if="company">
        <div class="company-main">
          <h1>{{ company.company_name }}</h1>
          <div class="company-info">
            <span class="info-item">
              <strong>Registro ANS:</strong> {{ company.ans_id }}
            </span>
            <span class="divider">•</span>
            <span class="info-item">
              <strong>CNPJ:</strong> {{ company.cnpj }}
            </span>
          </div>
        </div>
        <div class="company-tags">
          <span class="tag tag-blue">{{ company.state }}</span>
          <span class="tag tag-outline">{{ company.modality }}</span>
        </div>
      </section>

      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-label">Total de Despesas</div>
          <div class="stat-value">{{ formatCurrency(totalExpenses) }}</div>
        </div>

        <div class="stat-card">
          <div class="stat-label">Média por Período</div>
          <div class="stat-value">{{ formatCurrency(averageExpense) }}</div>
        </div>

        <div class="stat-card">
          <div class="stat-label">Total de Registros</div>
          <div class="stat-value">{{ expenses.length }}</div>
        </div>

        <div class="stat-card" v-if="latestExpense">
          <div class="stat-label">Última Despesa</div>
          <div class="stat-value">{{ formatCurrency(latestExpense.amount) }}</div>
          <div class="stat-meta">{{ formatDate(latestExpense.reference_date) }}</div>
        </div>
      </div>

      <section class="content-card">
        <div class="card-header">
          <h2>Histórico de Despesas</h2>
          <button class="btn-secondary">Exportar</button>
        </div>

        <div v-if="expenses.length === 0" class="empty">
          <p>Nenhuma despesa registrada</p>
          <span>Não há histórico disponível para esta operadora</span>
        </div>

        <div v-else class="table-container">
          <table class="data-table">
            <thead>
              <tr>
                <th>Período</th>
                <th>Ano</th>
                <th>Trimestre</th>
                <th>Data de Referência</th>
                <th class="text-right">Valor</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="expense in expenses" :key="expense.id">
                <td>
                  <span class="period-badge">{{ expense.year }}-Q{{ expense.quarter }}</span>
                </td>
                <td class="mono">{{ expense.year }}</td>
                <td class="secondary">Trimestre {{ expense.quarter }}</td>
                <td class="secondary">{{ formatDate(expense.reference_date) }}</td>
                <td class="text-right">
                  <span class="amount">{{ formatCurrency(expense.amount) }}</span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>
    </div>
  </main>
</template>

<style scoped>
* {
  box-sizing: border-box;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 3rem 2rem;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  color: #1a1a1a;
}

.back-btn {
  background: none;
  border: none;
  color: #666;
  font-weight: 500;
  cursor: pointer;
  padding: 0.5rem 0;
  margin-bottom: 2rem;
  transition: color 0.2s;
}

.back-btn:hover {
  color: #000;
}

.loading {
  text-align: center;
  padding: 4rem;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 3px solid #f0f0f0;
  border-top-color: #000;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin: 0 auto 1rem;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.loading p {
  color: #666;
  margin: 0;
}

.error-state {
  text-align: center;
  padding: 4rem;
}

.error-state h2 {
  margin: 0 0 0.5rem 0;
  font-size: 1.5rem;
  font-weight: 600;
}

.error-state p {
  color: #666;
  margin: 0 0 2rem 0;
}

.btn-primary {
  background: #000;
  color: white;
  border: none;
  padding: 0.75rem 2rem;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.2s;
}

.btn-primary:hover {
  background: #333;
}

.company-header {
  background: white;
  border: 1px solid #e5e5e5;
  border-radius: 8px;
  padding: 2rem;
  margin-bottom: 2rem;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 2rem;
}

.company-main h1 {
  font-size: 1.75rem;
  font-weight: 600;
  margin: 0 0 0.75rem 0;
  color: #000;
}

.company-info {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex-wrap: wrap;
  color: #666;
  font-size: 0.9rem;
}

.info-item strong {
  font-weight: 500;
  color: #000;
}

.divider {
  color: #ddd;
}

.company-tags {
  display: flex;
  gap: 0.5rem;
  flex-shrink: 0;
}

.tag {
  padding: 0.5rem 1rem;
  border-radius: 6px;
  font-size: 0.85rem;
  font-weight: 500;
}

.tag-blue {
  background: #e7f3ff;
  color: #004085;
}

.tag-outline {
  background: white;
  border: 1px solid #ddd;
  color: #666;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: white;
  border: 1px solid #e5e5e5;
  border-radius: 8px;
  padding: 1.5rem;
}

.stat-label {
  color: #666;
  font-size: 0.85rem;
  font-weight: 500;
  margin-bottom: 0.5rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.stat-value {
  color: #000;
  font-size: clamp(1.25rem, 1.5vw, 1.75rem);
  font-weight: 600;
  line-height: 1.1;
  margin-bottom: 0.25rem;
  white-space: normal;
  overflow-wrap: break-word;
  word-wrap: break-word;
}

.stat-meta {
  color: #999;
  font-size: 0.8rem;
  margin-top: 0.25rem;
}

.content-card {
  background: white;
  border: 1px solid #e5e5e5;
  border-radius: 8px;
  padding: 2rem;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #f0f0f0;
}

.card-header h2 {
  font-size: 1.25rem;
  font-weight: 600;
  margin: 0;
  color: #000;
}

.btn-secondary {
  background: white;
  border: 1px solid #ddd;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  font-size: 0.875rem;
  transition: all 0.2s;
}

.btn-secondary:hover {
  border-color: #000;
  background: #fafafa;
}

.empty {
  text-align: center;
  padding: 3rem;
  color: #666;
}

.empty p {
  margin: 0 0 0.5rem 0;
  font-weight: 500;
}

.empty span {
  font-size: 0.875rem;
  color: #999;
}

.table-container {
  overflow-x: auto;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
}

.data-table th {
  text-align: left;
  font-weight: 600;
  font-size: 0.8rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: #666;
  padding: 0.75rem 1rem;
  border-bottom: 1px solid #e5e5e5;
}

.data-table td {
  padding: 1rem;
  border-bottom: 1px solid #f5f5f5;
  font-size: 0.9rem;
}

.data-table tbody tr:hover {
  background: #fafafa;
}

.text-right {
  text-align: right;
}

.mono {
  font-family: 'SF Mono', Monaco, 'Courier New', monospace;
  font-size: 0.85rem;
}

.secondary {
  color: #666;
}

.period-badge {
  display: inline-block;
  background: #f5f5f5;
  padding: 0.35rem 0.75rem;
  border-radius: 4px;
  font-family: 'SF Mono', Monaco, 'Courier New', monospace;
  font-size: 0.8rem;
  font-weight: 600;
}

.amount {
  font-weight: 600;
  color: #000;
  font-family: 'SF Mono', Monaco, 'Courier New', monospace;
}

@media (max-width: 768px) {
  .container {
    padding: 2rem 1rem;
  }

  .company-header {
    flex-direction: column;
    padding: 1.5rem;
  }

  .company-main h1 {
    font-size: 1.35rem;
  }

  .company-tags {
    width: 100%;
    justify-content: flex-start;
  }

  .stats-grid {
    grid-template-columns: 1fr;
  }

  .stat-value {
    font-size: 1.5rem;
  }

  .content-card {
    padding: 1.25rem;
  }

  .card-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }

  .btn-secondary {
    width: 100%;
  }

  .data-table th,
  .data-table td {
    padding: 0.75rem 0.5rem;
    font-size: 0.85rem;
  }
}
</style>