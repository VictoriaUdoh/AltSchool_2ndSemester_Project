from pymongo import MongoClient
from faker import Faker

client = MongoClient("mongodb://localhost:27017/")
db = client['ecommerce_db']
orders = db['orders']
products = db['products']

fake = Faker()

# Insert order
orders.insert_one({
    "order_id": 5021,
    "customer_id": 1,
    "order_date": fake.date_time_this_year().isoformat(),
    "status": "Pending"
})

# Update inventory
products.update_one(
    {"product_id": 101},
    {"$inc": {"stock": -1}}
)

# Change Streams (Only works on replica sets)
# Commented out if you are not using a replica set
# with db.orders.watch() as stream:
#     for change in stream:
#         print("Change detected:", change)

# Schema Validation
db.command("collMod", "products", validator={
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["price"],
        "properties": {
            "price": {"bsonType": "number", "minimum": 0}
        }
    }
})
print("Schema validation applied.")