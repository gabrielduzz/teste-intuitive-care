<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import ExpenseChart from '../components/ExpenseChart.vue'
import { getCompanies } from '../services/api'
import type { Company } from '../types'

const searchQuery = ref('')
const companies = ref<Company[]>([])
const loading = ref(true)
const currentPage = ref(1)
const totalPages = ref(0)
const totalRecords = ref(0)

const fetchCompanies = async () => {
  loading.value = true;
  try {
    const response = await getCompanies(currentPage.value, 10, searchQuery.value);
    companies.value = response.data.data;
    totalPages.value = response.data.meta.total_pages;
    totalRecords.value = response.data.meta.total_records;
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

const paginationRange = computed(() => {
  const range = [];
  const delta = 2;
  const left = Math.max(2, currentPage.value - delta);
  const right = Math.min(totalPages.value - 1, currentPage.value + delta);

  range.push(1);

  if (left > 2) {
    range.push('...');
  }

  for (let i = left; i <= right; i++) {
    range.push(i);
  }

  if (right < totalPages.value - 1) {
    range.push('...');
  }

  if (totalPages.value > 1) {
    range.push(totalPages.value);
  }

  return range;
});

onMounted(() => {
  fetchCompanies();
});
</script>

<template>
  <main class="container">
    <header class="page-header">
      <div class="header-top">
        <div>
          <h1>Operadoras de Saúde</h1>
          <p class="header-description">Gerencie e acompanhe as operadoras cadastradas</p>
        </div>
        <div class="total-badge">
          {{ totalRecords }} operadoras
        </div>
      </div>
    </header>

    <section class="search-bar">
      <input type="text" v-model="searchQuery" @keyup.enter="handleSearch"
        placeholder="Buscar por razão social ou CNPJ..." class="search-input">
      <button @click="handleSearch" class="btn-search">
        Buscar
      </button>
    </section>

    <section class="content-card">
      <div class="card-header">
        <h2>Lista de Operadoras</h2>
        <span class="results-count">{{ companies.length }} de {{ totalRecords }} registros</span>
      </div>

      <div v-if="loading" class="loading">
        <div class="spinner"></div>
        <p>Carregando...</p>
      </div>

      <div v-else-if="companies.length === 0" class="empty">
        <p>Nenhuma operadora encontrada</p>
        <span>Tente ajustar os filtros de busca</span>
      </div>

      <div v-else class="table-container">
        <table class="data-table">
          <thead>
            <tr>
              <th>ANS</th>
              <th>CNPJ</th>
              <th>Razão Social</th>
              <th>Modalidade</th>
              <th>UF</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="company in companies" :key="company.ans_id">
              <td class="mono">{{ company.ans_id }}</td>
              <td class="mono secondary">{{ company.cnpj }}</td>
              <td class="strong">{{ company.company_name }}</td>
              <td><span class="tag tag-yellow">{{ company.modality }}</span></td>
              <td><span class="tag tag-blue">{{ company.state }}</span></td>
              <td class="actions">
                <router-link :to="`/operadora/${company.cnpj}`" class="btn-link">
                  Ver detalhes →
                </router-link>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="pagination" v-if="!loading && companies.length > 0">
        <button @click="changePage(currentPage - 1)" :disabled="currentPage === 1" class="btn-page">
          ← Anterior
        </button>

        <div class="page-numbers">
          <button v-for="(page, index) in paginationRange" :key="index"
            @click="typeof page === 'number' ? changePage(page) : null" :class="['page-num', {
              active: page === currentPage,
              dots: page === '...'
            }]" :disabled="page === '...'">
            {{ page }}
          </button>
        </div>

        <button @click="changePage(currentPage + 1)" :disabled="currentPage === totalPages" class="btn-page">
          Próximo →
        </button>
      </div>
    </section>

    <section class="content-card">
      <div class="card-header">
        <h2>Distribuição por Estado</h2>
      </div>
      <div class="chart-wrapper">
        <ExpenseChart />
      </div>
    </section>
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

.page-header {
  margin-bottom: 2.5rem;
}

.header-top {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 2rem;
}

.page-header h1 {
  font-size: 2rem;
  font-weight: 600;
  margin: 0 0 0.5rem 0;
  color: #000;
}

.header-description {
  color: #666;
  margin: 0;
  font-size: 0.95rem;
}

.total-badge {
  background: #f5f5f5;
  padding: 0.75rem 1.25rem;
  border-radius: 6px;
  font-weight: 500;
  white-space: nowrap;
  font-size: 0.9rem;
}

.search-bar {
  display: flex;
  gap: 0.75rem;
  margin-bottom: 2rem;
}

.search-input {
  flex: 1;
  padding: 0.875rem 1rem;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 0.95rem;
  transition: border-color 0.2s;
}

.search-input:focus {
  outline: none;
  border-color: #000;
}

.btn-search {
  background: #000;
  color: white;
  border: none;
  padding: 0.875rem 2rem;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.2s;
}

.btn-search:hover {
  background: #333;
}

.content-card {
  background: white;
  border: 1px solid #e5e5e5;
  border-radius: 8px;
  padding: 2rem;
  margin-bottom: 2rem;
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

.results-count {
  color: #666;
  font-size: 0.875rem;
}

.loading {
  text-align: center;
  padding: 3rem;
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

.mono {
  font-family: 'SF Mono', Monaco, 'Courier New', monospace;
  font-size: 0.85rem;
}

.secondary {
  color: #666;
}

.strong {
  font-weight: 500;
  color: #000;
}

.tag {
  display: inline-block;
  padding: 0.35rem 0.75rem;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: 500;
}

.tag-yellow {
  background: #fff3cd;
  color: #856404;
}

.tag-blue {
  background: #e7f3ff;
  color: #004085;
}

.actions {
  text-align: right;
}

.btn-link {
  color: #000;
  text-decoration: none;
  font-weight: 500;
  font-size: 0.875rem;
  transition: opacity 0.2s;
}

.btn-link:hover {
  opacity: 0.6;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 0.5rem;
  margin-top: 2rem;
  padding-top: 2rem;
  border-top: 1px solid #f0f0f0;
}

.btn-page {
  padding: 0.5rem 1rem;
  border: 1px solid #ddd;
  background: white;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  font-size: 0.875rem;
  transition: all 0.2s;
}

.btn-page:hover:not(:disabled) {
  border-color: #000;
  background: #fafafa;
}

.btn-page:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.page-numbers {
  display: flex;
  gap: 0.25rem;
}

.page-num {
  min-width: 36px;
  padding: 0.5rem;
  border: 1px solid #ddd;
  background: white;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  font-size: 0.875rem;
  transition: all 0.2s;
}

.page-num:hover:not(:disabled):not(.active) {
  border-color: #000;
  background: #fafafa;
}

.page-num.active {
  background: #000;
  color: white;
  border-color: #000;
}

.page-num.dots {
  border: none;
  cursor: default;
  background: transparent;
}

.chart-wrapper {
  min-height: 400px;
  padding: 1rem 0;
}

@media (max-width: 768px) {
  .container {
    padding: 2rem 1rem;
  }

  .page-header h1 {
    font-size: 1.5rem;
  }

  .header-top {
    flex-direction: column;
    align-items: flex-start;
  }

  .search-bar {
    flex-direction: column;
  }

  .btn-search {
    width: 100%;
  }

  .content-card {
    padding: 1.25rem;
  }

  .data-table th,
  .data-table td {
    padding: 0.75rem 0.5rem;
    font-size: 0.85rem;
  }

  .btn-page {
    font-size: 0;
    padding: 0.5rem 0.75rem;
  }

  .btn-page::before {
    content: '←';
    font-size: 1rem;
  }

  .btn-page:last-child::before {
    content: '→';
  }
}
</style>