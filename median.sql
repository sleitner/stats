WITH avg_table AS (
SELECT prop1, prop2, AVG(value) as mean
  FROM tablehh
 GROUP BY prop1, prop2
), 
med_part_table AS (
SELECT [loan_identification_number], prop1, prop2,  value, 
        ROW_NUMBER() over (partition by prop1, prop2 order by value ASC) as value_rank,
        1.0*COUNT(0) over (partition by prop1, prop2) as part_value
  FROM tablehh
),
median_table AS (
SELECT prop1, prop2, AVG(value) as median_value
  FROM med_part_table
 WHERE fee_rank in (part_value/2+1, (part_value+1)/2)    
 GROUP BY prop1, prop2
 )
SELECT a.prop1, a.prop2, median_value, mean_value
  FROM median_table m
 INNER JOIN avg_table a 
    ON a.prop1=m.prop1
       AND a.prop2=m.prop2
ORDER BY a.prop1, a.prop2
