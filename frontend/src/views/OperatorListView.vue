<script setup lang="ts">
import { ref } from 'vue'

const searchQuery = ref('')

const handleSearch = () => {
  console.log('Buscando por:', searchQuery.value)
}
</script>

<template>
  <main class="container">
    <header class="page-header">
      <h1>Painel de Operadoras</h1>
      <p class="subtitle">Gerencie e analise as despesas das operadoras de saúde</p>
    </header>

    <section class="control-panel">
      <div class="search-box">
        <input 
          type="text" 
          v-model="searchQuery" 
          placeholder="Digite a Razão Social ou CNPJ..."
          class="search-input"
        >
        
        <button @click="handleSearch" class="search-button">
          Buscar
        </button>
      </div>
    </section>

    <section class="chart-section">
      <h2>Distribuição por Estado</h2>
      <div class="chart-placeholder">
        [Gráfico será inserido aqui]
      </div>
    </section>

    <section class="data-section">
      <h2>Listagem de Operadoras</h2>
      <div class="table-placeholder">
        [Tabela será inserida aqui]
      </div>
    </section>
  </main>
</template>

<style scoped>
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
  font-family: sans-serif;
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
  font-size: 1rem;
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
  font-weight: bold;
}

.search-button:hover {
  background-color: #0056b3;
}
</style>