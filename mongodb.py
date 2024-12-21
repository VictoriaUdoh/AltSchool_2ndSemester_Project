import faker
import names_generator
from names_generator import generate_name
import pymongo
from pymongo import MongoClient
from datetime import timedelta, datetime
import random

from faker import Faker

fake = Faker()

try:
    uri = "mongodb://localhost:27017/"
    client = MongoClient(uri)
    db = client["ecommerce_db"]
except Exception as e:
    raise Exception(
        "The following error occurred: ",e)

customers = db["customers"]
products = db["products"]
orders = db["orders"]
order_items = db["order_items"]


# Insert customers
customer_data = [
    {
        "customer_id": i,
        "name": fake.name(),
        "email": fake.email(),
        "address": {
            "street": fake.street_address(),
            "city": fake.city(),
            "state": fake.state()
        }
    }
    for i in range(1, 21)  
]

customers.insert_many(customer_data)
print("Inserted customers.")


# Insert products
product_data = [
    {
        "product_id": i,
        "product_name": f"Product_{i}",
        "category": random.choice(["Electronics", "Books", "Clothing", "Toys"]),
        "price": random.randint(10, 5000)
    }
    for i in range(1, 21) 
]

products.insert_many(product_data)
print("Inserted products.")


# Insert orders
order_data = [
    {
        "order_id": i,
        "customer_id": random.randint(1, 20),
        "order_date": fake.date_time_this_year(),
        "delivery_date": fake.date_time_this_year() + timedelta(days=random.randint(1, 10)),
        "status": random.choice(["Delivered", "Pending", "Cancelled"])
    }
    for i in range(1, 21)
]

orders.insert_many(order_data)
print("Inserted orders with valid datetime objects.")


#insert order items
order_item_data = [
    {
        "order_item_id": i,
        "order_id": random.randint(1, 20),
        "product_id": random.randint(1, 20),
        "quantity": random.randint(1, 10),
        "price": random.randint(10, 5000)  
    }
    for i in range(1, 21)  
]

order_items.insert_many(order_item_data)
print("Inserted order items.")



#Perform Analytical Queries
#Revenue by Product Category
pipeline = [
    {"$lookup": {
        "from": "order_items",
        "localField": "product_id",
        "foreignField": "product_id",
        "as": "order_details"
    }},
    {"$unwind": "$order_details"},
    {"$group": {
        "_id": "$category",
        "total_revenue": {"$sum": {"$multiply": ["$order_details.quantity", "$order_details.price"]}}
    }},
    {"$sort": {"total_revenue": -1}}
]

result = list(products.aggregate(pipeline))
print("Revenue by Category:", result)


#What is the average delivery time for orders?
pipeline = [
    {
        "$project": {
            "delivery_time": {
                "$subtract": ["$delivery_date", "$order_date"] 
            }
        }
    },
    {
        "$group": {
            "_id": None,
            "avg_delivery_time_in_days": {
                "$avg": {"$divide": ["$delivery_time", 86400000]}  # Convert ms to days
            }
        }
    }
]

result = list(orders.aggregate(pipeline))

if result:
    print("Average Delivery Time (in days):", result[0]["avg_delivery_time_in_days"])
else:
    print("No data found.")

#Which states have the highest number of customers?
pipeline = [
    {
        "$group": {
            "_id": "$address.state",
            "num_customers": {"$sum": 1}
        }
    },
    {
        "$sort": {"num_customers": -1}  # Sort in descending order
    },
    {
        "$limit": 1  # Get only the top result
    }
]

result = list(customers.aggregate(pipeline))

if result:
    print("State with the Highest Number of Customers:", result[0])
else:
    print("No data found.")


#What are the top 3 most expensive products sold in each order?
pipeline = [
    {"$lookup": {
        "from": "products",
        "localField": "product_id",
        "foreignField": "product_id",
        "as": "product_details"
    }},
    {"$unwind": "$product_details"},
    {"$sort": {"product_details.price": -1}},
    {"$group": {
        "_id": "$order_id",
        "top_products": {"$push": "$product_details"}
    }},
    {"$project": {
        "_id": 1,
        "top_products": {"$slice": ["$top_products", 3]}
    }},
    {"$limit": 3} 
]

result = list(order_items.aggregate(pipeline))
print("Top 3 Orders with Products:", result)


#Schema Optimization
#Indexing
customers.create_index([("customer_id", 1)])
products.create_index([("product_id", 1)])
orders.create_index([("order_id", 1)])
order_items.create_index([("order_id", 1), ("product_id", 1)])
print("Indexes created.")