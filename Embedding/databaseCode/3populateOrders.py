from connection import connectToMongoDB, closeConnection
from bson import ObjectId, Decimal128 
from decimal import Decimal
from datetime import datetime
import random
from faker import Faker

mongoClient, db = connectToMongoDB()

usersCollection = db['users']
productsCollection = db['products']
ordersCollection = db['orders']

fake = Faker('en_GB')


def getRandomUser():
    pipeline = [{ "$sample": { "size": 1 } }]
    result = list(usersCollection.aggregate(pipeline))
    return result[0] if result else None


def createShoppingCart(minItems, maxItems):
    cartItems = []
    
    count = random.randint(minItems, maxItems)
    pipeline = [
        { "$match": { "stock": { "$gt": 0 } } },
        { "$sample": { "size": count } }
    ]
    
    products = list(productsCollection.aggregate(pipeline))
    
    for product in products:
        quantity = random.randint(1, max(1, product['stock']//2))
        
        cartItems.append({
            "productName": product['name'],
            "sku": product['sku'],
            "unitPrice": product['price'], 
            "quantity": quantity,
            "vendor": product['vendor']
        })
        
    return cartItems


def createOrder():
    customer = getRandomUser()
    if not customer:
        raise Exception("Error: No users in database")

    orderItems = createShoppingCart(1, 10)
    if not orderItems:
        raise Exception("Error: No items generated") 

    totalAmount = Decimal("0.00")
    for item in orderItems:
        price = item['unitPrice'].to_decimal() # converting from BSON to python value
        quantity = Decimal(item['quantity'])
        totalAmount += price * quantity

    userAddress = {}
    if "addresses" in customer and isinstance(customer["addresses"], list):
        userAddress = random.choice(customer["addresses"])
    else:
        userAddress = {}

    order = {
        "_id": ObjectId(),
        "orderDate": fake.date_time_between(start_date='-7y', end_date='now'),
        "total": Decimal128(totalAmount),
        "status": random.choice(["Pending", "Processing", "Shipped", "Delivered", "Cancelled"]),
        "customerSnapshot": customer, 
        "shippingDetails": {
            "address": userAddress,
            "method": random.choice(["DHL Express", "FedEx", "UPS Standard", "USPS Priority"]),
            "trackingCode": fake.bothify(text='??#########??').upper() # Ex: US123456789GB
        },
        "items": orderItems
    }
    
    return order


nOrders = 5000
orders = []

for _ in range(nOrders):
    order = createOrder()
    orders.append(order)

result = ordersCollection.insert_many(orders)
print(f"✓ {len(result.inserted_ids)} unique orders added successfully")

closeConnection(mongoClient)
