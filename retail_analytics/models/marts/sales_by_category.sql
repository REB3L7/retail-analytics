with order_items as (

    select *
    from {{ ref('stg_order_items') }}

),

products as (

    select *
    from {{ ref('stg_products') }}

),

category_sales as (

    select
        products.category,
        sum(order_items.quantity) as units_sold,
        round(
            sum(order_items.quantity * products.price),
            2
        ) as revenue

    from order_items

    inner join products
        on order_items.product_id = products.product_id

    group by products.category

)

select *
from category_sales
order by revenue desc