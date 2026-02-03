import axios from 'axios';
import type { Company, CompanyResponse, AggregatedData, Expense } from '../types';

const api = axios.create({
    baseURL: 'http://localhost:8000/api',
});

export const getCompanies = (page: number = 1, size: number = 10, search: string = '') => {
    let url = `/operadoras?page=${page}&size=${size}`;
    if (search) {
        url += `&search=${search}`;
    }
    return api.get<CompanyResponse>(url);
};

export const getCompanyByCnpj = (cnpj: string) => {
    return api.get<Company>(`/operadoras/${cnpj}`);
};

export const getCompanyExpenses = (cnpj: string) => {
    return api.get<Expense[]>(`/operadoras/${cnpj}/despesas`);
};

export const getStatistics = () => {
    let url = `/estatisticas`;
    return api.get<AggregatedData[]>(url);
};

export default api;