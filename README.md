# AltSchool_2ndSemester_Project
MongoDB Project: E-Commerce Database setup and Data Analysis
This project sets up an eCommerce database with collections for customers, products, orders, and order_items. It includes Python scripts for inserting sample data, performing analytical queries, and applying schema optimization techniques like indexing and validation.

Schema Design Decisions
The schema design reflects an eCommerce business structure with four main collections:

Customers
customer_id: A unique identifier for each customer (integer).
name: Customer's full name (string).
email: Customer's email address (string).
address: A nested object containing: street, city, and state (string).

Products
product_id: A unique identifier for each product (integer).
product_name: Name of the product (string).
category: Category to which the product belongs (string).
price: Price of the product (integer).
 
Orders
order_id: A unique identifier for each order (integer).
customer_id: A reference to the customer placing the order (integer).
order_date: Date when the order was placed (datetime).
delivery_date: Date when the order is expected or was delivered (datetime).
status: Current status of the order (Pending, Delivered, Cancelled) (string).
 
Order Items
order_item_id: A unique identifier for each order item (integer).
order_id: A reference to the order to which the item belongs (integer).
product_id: A reference to the product being sold (integer).
quantity: Quantity of the product in the order (integer).
price: Price of the product at the time of order (integer).
