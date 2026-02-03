export interface Company {
    ans_id: number;
    cnpj: string;
    company_name: string;
    modality: string;
    state: string;
}

export interface AggregatedData {
    company_name: string
    state: string

    total_amount: number
    avg_amount: number
    stddev_amount: number | null
}

export interface Expense {
    id: number;
    year: number;
    quarter: number;
    amount: number;
    reference_date: string;
}

export interface MetaData {
    page: number;
    size: number;
    total_records: number;
    total_pages: number;
}

export interface CompanyResponse {
    data: Company[];
    meta: MetaData;
}