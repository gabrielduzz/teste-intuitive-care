WITH dates AS (
	SELECT
	ans_id,
		MIN(reference_date) as initial_date,
		MAX(reference_date) as final_date
	FROM
		fact_expenses
	GROUP BY
		ans_id
)
SELECT
	dc.company_name,
	((fe_final.amount - fe_initial.amount)/fe_initial.amount) * 100 as percentual_growth
FROM dates dl 
JOIN fact_expenses fe_initial 
    ON dl.ans_id = fe_initial.ans_id 
    AND dl.initial_date = fe_initial.reference_date 
JOIN fact_expenses fe_final 
    ON dl.ans_id = fe_final.ans_id 
    AND dl.final_date = fe_final.reference_date 
JOIN dim_companies dc 
    ON dl.ans_id = dc.ans_id 
WHERE fe_initial.amount >= 100000
ORDER BY percentual_growth DESC 
LIMIT 5;
