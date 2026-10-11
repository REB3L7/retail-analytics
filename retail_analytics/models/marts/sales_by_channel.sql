with orders as (

    select *
    from {{ ref('stg_orders') }}

),

order_items as (

    select *
    from {{ ref('stg_order_items') }}

),

products as (

    select *
    from {{ ref('stg_products') }}

),

channel_sales as (

    select
        orders.sales_channel,

        count(distinct orders.order_id) as total_orders,

        sum(order_items.quantity) as units_sold,

        round(
            sum(order_items.quantity * products.price),
            2
        ) as revenue

    from orders

    inner join order_items
        on orders.order_id = order_items.order_id

    inner join products
        on order_items.product_id = products.product_id

    group by orders.sales_channel

)

select *
from channel_sales
order by revenue desc