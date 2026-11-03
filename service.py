from connection import *


async def create_product(owner_id, title, category, price, stock, photo_file_id):
    conn = await connection_db()
    try:
        product_id = await conn.fetchval("""
        insert into products(owner_id, title, category, price, stock, photo_file_id)
        values ($1, $2, $3, $4, $5, $6)
        returning id
        """, owner_id, title, category, price, stock, photo_file_id)
        return product_id
    except Exception as Error:
        print(f"❌ Create product Error: {Error}")
    finally:
        await conn.close()


async def get_other_products(user_id):
    conn = await connection_db()
    try:
        products = await conn.fetch("""
        select * from products
        where owner_id != $1
        order by id
        """, user_id)
        return products
    except Exception as Error:
        print(f"❌ Get other products Error: {Error}")

    finally:
        await conn.close()



async def get_my_products(user_id):
    conn = await connection_db()
    try:
        products = await conn.fetch("""
        select * from products
        where owner_id = $1
        order by id
        """, user_id)
        return products
    except Exception as Error:
        print(f"❌ Get my products Error: {Error}")
    finally:
        await conn.close()






async def get_product(product_id):
    conn = await connection_db()
    try:
        product = await conn.fetchrow("""
        select * from products where id = $1
        """, product_id)
        return product
    except Exception as Error:
        print(f"❌ Get product Error: {Error}")
        return None
    finally:
        await conn.close()







async def buy_product(product_id, user_id):
    conn = await connection_db()
    try:
        async with conn.transaction():
            product = await conn.fetchrow("""
            select * from products
            where id = $1 for update
            """, product_id)

            if not product:
                return "not_found",

            if product['owner_id'] == user_id:
                return "own_product", product

            if product['stock'] <= 0:
                return "out_of_stock", product

            product = await conn.fetchrow("""
            update products set stock = stock - 1
            where id = $1
            """, product_id)

            await conn.execute("""
            insert into orders(user_id, product_id, purchase_price)
            values ($1, $2, $3)
            """, user_id, product_id, product['price'])

            return "ok", product
    except Exception as Error:
        print(f"❌ Buy product Error: {Error}")
        return "error", 
    finally:
        await conn.close()








async def get_user_orders(user_id):
    conn = await connection_db()
    try:
        orders = await conn.fetch("""
        select products.id as product_id, products.title,
               orders.purchase_price, orders.purchased_at
        from orders
        join products on orders.product_id = products.id
        where orders.user_id = $1
        order by orders.purchased_at desc
        """, user_id)
        return orders
    except Exception as Error:
        print(f"❌ Get orders Error: {Error}")
    finally:
        await conn.close()









async def get_sales_count(product_id):
    conn = await connection_db()
    try:
        count = await conn.fetchval("""
        select count(*) from orders where product_id = $1
        """, product_id)
        return count
    except Exception as Error:
        print(f"❌ Get sales count Error: {Error}")
    finally:
        await conn.close()




async def get_user_spending(user_id):
    conn = await connection_db()
    try:
        total = await conn.fetchval("""
        select coalesce(sum(purchase_price))
        from orders where user_id = $1
        """, user_id)
        return total
    except Exception as Error:
        print(f"❌ Get spending Error: {Error}")
     
    finally:
        await conn.close()






async def get_all_products():
    conn = await connection_db()
    try:
        products = await conn.fetch("""
        select * from products order by id
        """)
        return products
    except Exception as Error:
        print(f"❌ Get  products Error: {Error}")
    finally:
        await conn.close()