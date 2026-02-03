WITH general_average AS (
  SELECT
    AVG(amount) as average
  FROM fact_expenses
)
SELECT
  COUNT(*) as companies_total 
FROM (
    SELECT 
      fe.ans_id
    FROM fact_expenses fe
    CROSS JOIN general_average ga
    WHERE fe.amount > ga.average
    GROUP BY fe.ans_id
    HAVING COUNT(*) >= 2
) AS filtered_companies; 