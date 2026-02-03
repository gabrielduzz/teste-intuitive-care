CREATE TABLE dim_companies (
    ans_id INT PRIMARY KEY,           
    cnpj VARCHAR(14) NOT NULL,        
    company_name VARCHAR(255),        
    modality VARCHAR(100),            
    state CHAR(2)                    
);

CREATE INDEX idx_company_cnpj ON dim_companies(cnpj);


CREATE TABLE fact_expenses (
    id SERIAL PRIMARY KEY,
    ans_id INT REFERENCES dim_companies(ans_id),
    year INT NOT NULL,
    quarter INT NOT NULL,
    reference_date DATE,             
    amount DECIMAL(18, 2),           
    CONSTRAINT uk_expense_unique UNIQUE (ans_id, year, quarter)
);

CREATE INDEX idx_expenses_period ON fact_expenses(year, quarter);
CREATE INDEX idx_expenses_amount ON fact_expenses(amount);  

CREATE VIEW aggregated_data AS
SELECT
    c.company_name,
    c.state,
    SUM(e.amount) AS total_amount,
    AVG(e.amount) AS avg_amount,
    STDDEV(e.amount) AS stddev_amount
FROM
    fact_expenses e
JOIN
    dim_companies c ON e.ans_id = c.ans_id
GROUP BY
    c.company_name, c.state;