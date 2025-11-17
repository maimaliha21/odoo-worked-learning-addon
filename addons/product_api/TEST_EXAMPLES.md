# 🧪 Test Examples - Product API

## ✅ Health Check (Working!)
You've already tested this:
```
GET http://localhost:8069/api/products/health
Response: {"status": "ok", "message": "Product API is running"}
```

## 🎯 Next Tests to Try

### Test 1: Get All Products
Open in browser:
```
http://localhost:8069/api/products?limit=5
```

Or use curl:
```bash
curl http://localhost:8069/api/products?limit=5
```

**Expected:** List of your products (Cable Management Box, Casual Denim Short, etc.)

### Test 2: Get Single Product
Replace `1` with an actual product ID from your Odoo:
```
http://localhost:8069/api/products/1
```

**Expected:** Detailed info about one product

### Test 3: Search Products
```
http://localhost:8069/api/products/search?name=desk
```

**Expected:** Products with "desk" in the name

### Test 4: Search by Price
```
http://localhost:8069/api/products/search?min_price=10&max_price=50
```

**Expected:** Products between $10 and $50

### Test 5: Get by Category
```
http://localhost:8069/api/products/category/all
```

**Expected:** Products in that category

## 💻 Python Test Script

Create a file `test_api.py`:

```python
import requests
import json

base_url = 'http://localhost:8069/api/products'

print("=" * 50)
print("Test 1: Health Check")
print("=" * 50)
response = requests.get(f'{base_url}/health')
print(json.dumps(response.json(), indent=2))

print("\n" + "=" * 50)
print("Test 2: Get All Products (limit 5)")
print("=" * 50)
response = requests.get(f'{base_url}?limit=5')
data = response.json()
print(f"Total: {data['total']} products")
for product in data['products']:
    print(f"  - {product['name']} (${product['price']})")

print("\n" + "=" * 50)
print("Test 3: Search Products")
print("=" * 50)
response = requests.get(f'{base_url}/search', params={'name': 'desk', 'limit': 3})
data = response.json()
print(f"Found {data['total']} products")
for product in data['products']:
    print(f"  - {product['name']} (${product['list_price']})")
```

Run it:
```bash
python test_api.py
```

## 🌐 Browser Tests

Just copy-paste these URLs in your browser:

1. **All Products:**
   ```
   http://localhost:8069/api/products?limit=10
   ```

2. **Search:**
   ```
   http://localhost:8069/api/products/search?name=chair
   ```

3. **Price Range:**
   ```
   http://localhost:8069/api/products/search?min_price=20&max_price=100
   ```

## 📊 Expected Response Format

### Get All Products Response:
```json
{
  "products": [
    {
      "id": 1,
      "name": "Cable Management Box",
      "reference": "FURN_5555",
      "price": 100.0,
      "quantity": 90.0,
      "image_url": "/web/image/product.template/1/image_128"
    }
  ],
  "total": 1,
  "limit": 5,
  "offset": 0
}
```

### Single Product Response:
```json
{
  "id": 1,
  "name": "Cable Management Box",
  "default_code": "FURN_5555",
  "list_price": 100.0,
  "standard_price": 70.0,
  "qty_available": 90.0,
  "type": "product",
  "categ_id": {
    "id": 1,
    "name": "All"
  }
}
```

## 🎉 You're All Set!

Your API is working! Now you can:
- Use it in your Flutter app
- Integrate with other systems
- Build a frontend that consumes the API
- Add more endpoints as needed

Happy testing! 🚀

