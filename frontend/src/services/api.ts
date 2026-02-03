import axios from 'axios';
import type { CompanyResponse } from '../types';
import type { AggregatedData } from '../types';

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

export const getStatistics = () => {
    let url = `/estatisticas`;
    return api.get<AggregatedData[]>(url);
};

export default api;