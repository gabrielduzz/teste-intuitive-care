SELECT
	dc.state,
	SUM(fe.amount) as total,
	COUNT(DISTINCT fe.ans_id) AS num_companies,
	SUM(fe.amount) / NULLIF(COUNT(DISTINCT fe.ans_id), 0) AS mean_by_company
FROM fact_expenses fe
JOIN dim_companies dc 
	ON fe.ans_id = dc.ans_id 
GROUP BY state
ORDER BY total DESC 
LIMIT 5;