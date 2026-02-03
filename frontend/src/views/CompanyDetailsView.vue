<script setup lang="ts">
import { ref, onMounted } from 'vue'
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
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL'
  }).format(value)
}

const formatDate = (dateString: string) => {
  if (!dateString) return '-'
  return new Date(dateString).toLocaleDateString('pt-BR')
}

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
      &larr; Voltar
    </button>

    <div v-if="loading" class="loading">Carregando detalhes...</div>

    <div v-else-if="error" class="error-msg">{{ error }}</div>

    <div v-else class="content">
      <section class="company-card" v-if="company">
        <header>
          <h1>{{ company.company_name }}</h1>
          <span class="badge">{{ company.state }}</span>
        </header>
        <div class="details-grid">
          <div class="detail-item">
            <strong>CNPJ:</strong> {{ company.cnpj }}
          </div>
          <div class="detail-item">
            <strong>Registro ANS:</strong> {{ company.ans_id }}
          </div>
          <div class="detail-item">
            <strong>Modalidade:</strong> {{ company.modality }}
          </div>
        </div>
      </section>

      <section class="history-section">
        <h2>Histórico de Despesas</h2>

        <div v-if="expenses.length === 0" class="no-data">
          Nenhuma despesa registrada para esta operadora.
        </div>

        <table v-else class="expenses-table">
          <thead>
            <tr>
              <th>Data Ref.</th>
              <th>Ano/Trimestre</th>
              <th>Valor Informado</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="expense in expenses" :key="expense.id">
              <td>{{ formatDate(expense.reference_date) }}</td>
              <td>{{ expense.year }} / Q{{ expense.quarter }}</td>
              <td class="amount-cell">{{ formatCurrency(expense.amount) }}</td>
            </tr>
          </tbody>
        </table>
      </section>
    </div>
  </main>
</template>

<style scoped>
.container {
  max-width: 900px;
  margin: 0 auto;
  padding: 2rem;
  font-family: 'Inter', sans-serif;
}

.back-btn {
  background: none;
  border: none;
  color: #007bff;
  font-size: 1rem;
  cursor: pointer;
  margin-bottom: 1rem;
  padding: 0;
}

.back-btn:hover {
  text-decoration: underline;
}

.company-card {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  margin-bottom: 2rem;
  border-left: 5px solid #007bff;
}

.company-card header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  border-bottom: 1px solid #eee;
  padding-bottom: 1rem;
}

.company-card h1 {
  margin: 0;
  font-size: 1.5rem;
  color: #333;
}

.badge {
  background-color: #007bff;
  color: white;
  padding: 5px 12px;
  border-radius: 20px;
  font-weight: bold;
}

.details-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.detail-item strong {
  display: block;
  color: #666;
  font-size: 0.9rem;
  margin-bottom: 4px;
}

.detail-item {
  font-size: 1.1rem;
  color: #333;
}

.history-section h2 {
  margin-bottom: 1rem;
  color: #444;
}

.expenses-table {
  width: 100%;
  border-collapse: collapse;
  background: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  border-radius: 8px;
  overflow: hidden;
}

.expenses-table th,
.expenses-table td {
  padding: 12px 20px;
  color: #333;
  text-align: left;
  border-bottom: 1px solid #eee;
}

.expenses-table th {
  background-color: #f8f9fa;
  color: #666;
  font-weight: 600;
}

.amount-cell {
  font-family: 'Courier New', monospace;
  font-weight: bold;
  color: #28a745;
}

.loading,
.error-msg,
.no-data {
  text-align: center;
  padding: 2rem;
  color: #777;
  font-size: 1.1rem;
}

.error-msg {
  color: #dc3545;
}
</style>