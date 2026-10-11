with stores as (

    select *
    from {{ ref('stg_stores') }}

),

orders as (

    select *
    from {{ ref('stg_orders') }}
    where sales_channel = 'STORE'

),

order_items as (

    select *
    from {{ ref('stg_order_items') }}

),

products as (

    select *
    from {{ ref('stg_products') }}

),

store_sales as (

    select
        stores.store_id,
        stores.store_name,
        stores.city,
        stores.state,
        stores.opened_date,

        count(distinct orders.order_id) as total_orders,

        coalesce(
            sum(order_items.quantity),
            0
        ) as units_sold,

        round(
            coalesce(
                sum(order_items.quantity * products.price),
                0
            ),
            2
        ) as revenue

    from stores

    left join orders
        on stores.store_id = orders.store_id

    left join order_items
        on orders.order_id = order_items.order_id

    left join products
        on order_items.product_id = products.product_id

    group by
        stores.store_id,
        stores.store_name,
        stores.city,
        stores.state,
        stores.opened_date

)

select *
from store_sales