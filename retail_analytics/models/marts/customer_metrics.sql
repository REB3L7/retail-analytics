with customers as (

    select *
    from {{ ref('stg_customers') }}

),

orders as (

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

order_totals as (

    select
        orders.order_id,
        orders.customer_id,
        orders.order_timestamp,

        sum(order_items.quantity) as units_purchased,

        round(
            sum(order_items.quantity * products.price),
            2
        ) as order_revenue

    from orders

    inner join order_items
        on orders.order_id = order_items.order_id

    inner join products
        on order_items.product_id = products.product_id

    group by
        orders.order_id,
        orders.customer_id,
        orders.order_timestamp

),

customer_summary as (

    select
        customers.customer_id,
        customers.name,
        customers.state,
        customers.loyalty_member,

        count(order_totals.order_id) as total_orders,

        coalesce(
            sum(order_totals.units_purchased),
            0
        ) as total_units,

        round(
            coalesce(sum(order_totals.order_revenue), 0),
            2
        ) as total_spend,

        round(
            coalesce(avg(order_totals.order_revenue), 0),
            2
        ) as average_order_value,

        min(order_totals.order_timestamp) as first_order,

        max(order_totals.order_timestamp) as latest_order

    from customers

    left join order_totals
        on customers.customer_id = order_totals.customer_id

    group by
        customers.customer_id,
        customers.name,
        customers.state,
        customers.loyalty_member

)

select *
from customer_summary