with order_details as (

    select
        o.order_id,
        o.order_timestamp,
        oi.quantity,
        p.price

    from {{ ref('stg_orders') }} o

    join {{ ref('stg_order_items') }} oi
        on o.order_id = oi.order_id

    join {{ ref('stg_products') }} p
        on oi.product_id = p.product_id

)

select
    date_trunc('month', order_timestamp) as month,
    count(distinct order_id) as total_orders,
    sum(quantity) as units_sold,
    round(sum(quantity * price), 2) as revenue

from order_details

group by 1
order by 1