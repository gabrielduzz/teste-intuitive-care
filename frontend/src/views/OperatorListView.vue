<script setup lang="ts">
import { ref, onMounted } from 'vue'
import ExpenseChart from '../components/ExpenseChart.vue'
import { getCompanies } from '../services/api'
import type { Company } from '../types'

const searchQuery = ref('')
const companies = ref<Company[]>([])
const loading = ref(true)
const currentPage = ref(1)
const totalPages = ref(0)

const fetchCompanies = async () => {
  loading.value = true;
  try {
    const response = await getCompanies(currentPage.value, 10, searchQuery.value);

    companies.value = response.data.data;

    totalPages.value = response.data.meta.total_pages;
  } catch (error) {
    console.error("Erro ao buscar empresas:", error);
  } finally {
    loading.value = false;
  }
}

const changePage = (newPage: number) => {
  if (newPage >= 1 && newPage <= totalPages.value) {
    currentPage.value = newPage;
    fetchCompanies();
  }
}

const handleSearch = () => {
  currentPage.value = 1;
  fetchCompanies();
}

const jumpToPage = (event: Event) => {
  const target = event.target as HTMLInputElement;
  const page = parseInt(target.value);

  if (page >= 1 && page <= totalPages.value) {
    changePage(page);
  } else {
    target.value = currentPage.value.toString();
    alert(`Por favor, digite um número entre 1 e ${totalPages.value}`);
  }
}

onMounted(() => {
  fetchCompanies();
});

</script>

<template>
  <main class="container">
    <header class="page-header">
      <h1>Painel de Operadoras</h1>
      <p class="subtitle">Gerencie e analise as despesas das operadoras de saúde</p>
    </header>

    <section class="control-panel">
      <div class="search-box">
        <input type="text" v-model="searchQuery" placeholder="Digite a Razão Social ou CNPJ..." class="search-input">
        <button @click="handleSearch" class="search-button">Buscar</button>
      </div>
    </section>

    <section class="data-section">
      <h2>Listagem de Operadoras</h2>

      <div v-if="loading" class="loading-state">
        Carregando dados...
      </div>

      <div v-else class="table-container">
        <table class="operator-table">
          <thead>
            <tr>
              <th>Registro ANS</th>
              <th>CNPJ</th>
              <th>Razão Social</th>
              <th>UF</th>
              <th>Ações</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="company in companies" :key="company.ans_id">
              <td>{{ company.ans_id }}</td>
              <td>{{ company.cnpj }}</td>
              <td>{{ company.company_name }}</td>
              <td>
                <span class="badge">{{ company.state }}</span>
              </td>
              <td>
                <router-link :to="`/operadora/${company.ans_id}`" class="details-link">
                  Ver Detalhes
                </router-link>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="pagination-controls">
        <button @click="changePage(currentPage - 1)" :disabled="currentPage === 1" class="page-btn">
          Anterior
        </button>

        <div class="page-input-container">
          <span>Página</span>
          <input type="number" :value="currentPage" @change="jumpToPage" min="1" :max="totalPages"
            class="page-number-input">
          <span>de {{ totalPages }}</span>
        </div>

        <button @click="changePage(currentPage + 1)" :disabled="currentPage === totalPages" class="page-btn">
          Próximo
        </button>
      </div>
    </section>

    <section class="chart-section">
      <h2>Distribuição por Estado</h2>
      <div class="chart-container">
        <ExpenseChart />
      </div>
    </section>
  </main>
</template>

<style scoped>
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
  font-family: 'Inter', sans-serif;
}

.control-panel {
  margin: 2rem 0;
  padding: 1.5rem;
  background-color: #f8f9fa;
  border-radius: 8px;
}

.search-box {
  display: flex;
  gap: 10px;
}

.search-input {
  flex: 1;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.search-button {
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.table-container {
  overflow-x: auto;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
}

.operator-table {
  width: 100%;
  border-collapse: collapse;
  background: rgba(0, 0, 0, 0.1);
}

.operator-table th,
.operator-table td {
  padding: 12px 15px;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

.operator-table th {
  background-color: #343a40;
  color: white;
  text-transform: uppercase;
  font-size: 0.85rem;
  letter-spacing: 0.05em;
}

.operator-table tr:hover {
  background-color: #f1f1f1;
  color: #343a40;
}

.badge {
  background-color: #e9ecef;
  padding: 4px 8px;
  border-radius: 12px;
  font-weight: bold;
  font-size: 0.8rem;
  color: #495057;
}

.details-link {
  color: #007bff;
  text-decoration: none;
  font-weight: 500;
}

.details-link:hover {
  text-decoration: underline;
}

.loading-state {
  text-align: center;
  padding: 2rem;
  font-size: 1.2rem;
  color: #666;
}

.pagination-controls {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 1.5rem;
  gap: 15px;
}

.page-btn {
  padding: 8px 16px;
  border: 1px solid #007bff;
  background-color: white;
  color: #007bff;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s;
}

.page-btn:hover:not(:disabled) {
  background-color: #007bff;
  color: white;
}

.page-btn:disabled {
  border-color: #ccc;
  color: #ccc;
  cursor: not-allowed;
}

.page-info {
  font-size: 0.9rem;
  color: #555;
}

.page-input-container {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.9rem;
  color: #555;
}

.page-number-input {
  width: 60px;
  padding: 5px;
  text-align: center;
  border: 1px solid #ccc;
  border-radius: 4px;
}

input[type=number]::-webkit-inner-spin-button,
input[type=number]::-webkit-outer-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

.chart-section {
  padding: 3rem;
}
</style>