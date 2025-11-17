# 🚀 Quick Start Guide - Product API

## What You Have

✅ **Model** (`models/product_template.py`) - Extends product.template with methods to get product data  
✅ **Controller** (`controllers/product_controller.py`) - Creates API endpoints  
✅ **5 API Endpoints** - Ready to use!

## 📝 Simple Explanation

### Model = Database Worker
- **File:** `models/product_template.py`
- **What it does:** Gets product data from database
- **Example method:** `get_product_info(product_id)` - Gets one product's data

### Controller = API Server
- **File:** `controllers/product_controller.py`
- **What it does:** Creates URLs that return product data
- **Example:** When you visit `/api/products`, it returns all products as JSON

## 🔄 How It Works

```
You request: GET /api/products
     ↓
Controller receives request
     ↓
Controller calls: Model.get_all_products_simple()
     ↓
Model gets data from database
     ↓
Controller returns JSON: {"products": [...]}
```

## ⚡ 3-Minute Setup

### 1. Restart Odoo
```bash
# Stop Odoo (Ctrl+C if running manually)
# Then start it again
```

### 2. Install Module
1. Open Odoo
2. Go to **Apps**
3. Click **Update Apps List**
4. Search **"Product API"**
5. Click **Install**

### 3. Test It!
```bash
# Test health check
curl http://localhost:8069/api/products/health

# Get your products
curl http://localhost:8069/api/products?limit=5
```

## 📡 5 API Endpoints

### 1. Health Check
```bash
GET /api/products/health
```

### 2. Get All Products
```bash
GET /api/products?limit=10
```

### 3. Get One Product
```bash
GET /api/products/1
```

### 4. Search Products
```bash
GET /api/products/search?name=desk&min_price=50
```

### 5. Get by Category
```bash
GET /api/products/category/furniture
```

## 💡 Example: Get Your Products

```python
import requests

# Get all products
response = requests.get('http://localhost:8069/api/products?limit=10')
data = response.json()

for product in data['products']:
    print(f"{product['name']} - ${product['price']}")
```

**Output:**
```
Cable Management Box - $100.0
Casual Denim Short - $35.0
Cheese Croissant - $1.65
...
```

## 🎯 Key Files

1. **`models/product_template.py`** - Model with methods to get data
2. **`controllers/product_controller.py`** - Controller with API endpoints
3. **`README.md`** - Complete documentation

## ❓ Common Questions

**Q: Where is the database?**  
A: Odoo uses PostgreSQL. The model accesses it via `self.search()`.

**Q: How do I add a new endpoint?**  
A: Add a new method in `controllers/product_controller.py` with `@http.route()`.

**Q: How do I add a new filter?**  
A: Edit `search_products()` method in `models/product_template.py`.

**Q: Why use `.sudo()`?**  
A: It bypasses permissions so the API works without login.

## 🐛 Troubleshooting

**Module not found?**
- Restart Odoo
- Update Apps List
- Check addon is in `addons/product_api/`

**404 Error?**
- Check module is installed
- Verify URL: `/api/products/health`

**No products?**
- Make sure you have products in Odoo
- Go to: Inventory → Products

## 📚 Next Steps

1. ✅ Install the module
2. ✅ Test with curl
3. ✅ Read `README.md` for details
4. ✅ Use in your app!

**That's it! You're ready to use the Product API!** 🎉

