SELECT
    category,
    COUNT(*) AS product_count,
    ROUND(AVG(price), 2) AS average_price,
    ROUND(MIN(price), 2) AS cheapest_product,
    ROUND(MAX(price), 2) AS most_expensive_product
FROM read_parquet('data/raw/products.parquet')
GROUP BY category
ORDER BY average_price DESC;