# Product API Addon - Complete Guide

## 📚 What is This?

This addon creates a **REST API** to access your Odoo product data. It has:
- **Model** (`models/product_template.py`) - Extends product.template with custom methods
- **Controller** (`controllers/product_controller.py`) - Creates API endpoints (URLs)

## 🎯 Understanding Models vs Controllers

### Model (Database Layer)
**File:** `models/product_template.py`

The **model** extends Odoo's existing `product.template` model and adds custom methods to work with product data.

```python
class ProductTemplate(models.Model):
    _inherit = 'product.template'  # Extend existing product model
    
    @api.model
    def get_product_info(self, product_id):
        # This method gets product data from database
        product = self.browse(product_id)
        return {
            'id': product.id,
            'name': product.name,
            'price': product.list_price,
            # ... more fields
        }
```

**What it does:**
- Works directly with the database
- Gets product data
- Formats data for API responses
- Can be called from controllers or other models

### Controller (API Layer)
**File:** `controllers/product_controller.py`

The **controller** creates HTTP endpoints (URLs) that users can visit to get data.

```python
class ProductAPIController(http.Controller):
    
    @http.route('/api/products', type='http', auth='public')
    def get_all_products(self, **kwargs):
        # When user visits /api/products, this runs
        products = request.env['product.template'].sudo().get_all_products_simple()
        return self._json_response({'products': products})
```

**What it does:**
- Handles HTTP requests (GET, POST, etc.)
- Calls model methods to get data
- Returns JSON responses
- Like a waiter: takes orders (requests) and brings food (data)

## 🔄 How They Work Together

```
User makes request
       ↓
GET http://localhost:8069/api/products
       ↓
Controller receives request
       ↓
Controller calls Model method
       ↓
Model queries database
       ↓
Model returns data
       ↓
Controller formats as JSON
       ↓
User receives response
```

## 📁 File Structure

```
product_api/
├── __manifest__.py          # Addon configuration
├── __init__.py              # Imports models and controllers
│
├── models/                  # DATABASE LAYER
│   ├── __init__.py
│   └── product_template.py # Extends product.template
│       • get_product_info()
│       • search_products()
│       • get_all_products_simple()
│       • get_products_by_category()
│
├── controllers/             # API LAYER
│   ├── __init__.py
│   └── product_controller.py
│       • GET /api/products
│       • GET /api/products/{id}
│       • GET /api/products/search
│       • GET /api/products/category/{name}
│
└── security/
    └── ir.model.access.csv  # Access rights
```

## 🚀 Installation

### Step 1: Restart Odoo
```bash
# If Odoo is running, restart it
sudo systemctl restart odoo
# Or if running manually, stop and restart
```

### Step 2: Update Apps List
1. Go to **Apps** menu in Odoo
2. Click **Update Apps List**
3. Remove the **Apps** filter (click the X)

### Step 3: Install Module
1. Search for **"Product API"**
2. Click **Install**

## 🧪 Testing the API

### Test 1: Health Check
```bash
curl http://localhost:8069/api/products/health
```

**Expected Response:**
```json
{
  "status": "ok",
  "message": "Product API is running"
}
```

### Test 2: Get All Products
```bash
curl http://localhost:8069/api/products?limit=5
```

**Expected Response:**
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
    },
    {
      "id": 2,
      "name": "Casual Denim Short",
      "reference": "",
      "price": 35.0,
      "quantity": 56.0,
      "image_url": "/web/image/product.template/2/image_128"
    }
  ],
  "total": 2,
  "limit": 5,
  "offset": 0
}
```

### Test 3: Get Single Product
```bash
curl http://localhost:8069/api/products/1
```

### Test 4: Search Products
```bash
# Search by name
curl "http://localhost:8069/api/products/search?name=desk"

# Search by price range
curl "http://localhost:8069/api/products/search?min_price=10&max_price=50"

# Search by category
curl "http://localhost:8069/api/products/search?category=furniture"
```

### Test 5: Get by Category
```bash
curl http://localhost:8069/api/products/category/furniture
```

## 📡 Available API Endpoints

### 1. Health Check
```
GET /api/products/health
```
Returns API status

### 2. Get All Products
```
GET /api/products?limit=100&offset=0
```
- `limit`: Number of products (default: 100)
- `offset`: Skip products (default: 0)

### 3. Get Single Product
```
GET /api/products/{id}
```
Get detailed info about one product

### 4. Search Products
```
GET /api/products/search?name=desk&min_price=50&max_price=100
```
**Filters:**
- `name`: Product name (partial match)
- `default_code`: Product reference
- `category`: Category name
- `min_price`: Minimum price
- `max_price`: Maximum price
- `type`: Product type (consu, service, product)
- `limit`: Results limit (default: 10)
- `offset`: Skip results (default: 0)

### 5. Get by Category
```
GET /api/products/category/{category_name}
```
Get all products in a category

## 💻 Using from Python

```python
import requests

# Get all products
response = requests.get('http://localhost:8069/api/products?limit=10')
products = response.json()
print(f"Found {products['total']} products")

# Get single product
response = requests.get('http://localhost:8069/api/products/1')
product = response.json()
print(f"Product: {product['name']} - ${product['list_price']}")

# Search products
response = requests.get('http://localhost:8069/api/products/search', params={
    'name': 'desk',
    'min_price': 50,
    'limit': 5
})
results = response.json()
print(f"Found {results['total']} products")
```

## 🌐 Using from JavaScript

```javascript
// Get all products
fetch('http://localhost:8069/api/products?limit=10')
  .then(response => response.json())
  .then(data => {
    console.log('Products:', data.products);
    data.products.forEach(product => {
      console.log(`${product.name} - $${product.price}`);
    });
  });

// Search products
fetch('http://localhost:8069/api/products/search?name=desk&min_price=50')
  .then(response => response.json())
  .then(data => {
    console.log('Search results:', data);
  });
```

## 🔑 Key Concepts Explained

### `_inherit = 'product.template'`
This means we're **extending** the existing product model, not creating a new one. We add new methods but keep all existing functionality.

### `@api.model`
This decorator means the method works at the **model level** (not on a specific record). Use it for:
- Searching/filtering
- Getting multiple records
- Creating new records

### `request.env['product.template']`
This is how you access models from a controller:
- `request.env` = Access to Odoo database
- `['product.template']` = Access the product model
- `.sudo()` = Bypass permissions (admin access)

### `.search([])`
Searches for records:
- `[]` = Get all records
- `[('name', 'ilike', 'desk')]` = Search with filter
- `limit=10` = Maximum results
- `offset=0` = Skip first N results

### `@http.route()`
Defines an API endpoint:
- `/api/products` = URL path
- `type='http'` = REST endpoint
- `auth='public'` = No login required
- `methods=['GET']` = Only GET requests
- `csrf=False` = Disable CSRF protection (needed for API)

## 🛠️ Customization Examples

### Add New Filter
Edit `models/product_template.py`:

```python
# In search_products method, add:
if filters.get('barcode'):
    domain.append(('barcode', '=', filters['barcode']))
```

### Add New Endpoint
Edit `controllers/product_controller.py`:

```python
@http.route('/api/products/my_endpoint', type='http', auth='public', methods=['GET'], csrf=False)
def my_endpoint(self, **kwargs):
    # Your code here
    products = request.env['product.template'].sudo().search([])
    return self._json_response({'count': len(products)})
```

### Add New Field to Response
Edit `models/product_template.py`:

```python
# In get_product_info method, add:
product_data['my_custom_field'] = product.my_custom_field or ''
```

## 🐛 Troubleshooting

### Module doesn't appear
1. Restart Odoo: `sudo systemctl restart odoo`
2. Go to Apps → Update Apps List
3. Remove filters and search again

### API returns 404
- Check module is installed
- Verify Odoo is running
- Test health endpoint first: `/api/products/health`

### Empty products list
- Make sure you have products in Odoo
- Go to: Inventory → Products
- Create some test products if needed

### Permission errors
- The API uses `.sudo()` which bypasses permissions
- If you still get errors, check `security/ir.model.access.csv`

## 📖 Summary

**Model (`models/product_template.py`):**
- Extends `product.template`
- Adds methods: `get_product_info()`, `search_products()`, etc.
- Works with database
- Returns formatted data

**Controller (`controllers/product_controller.py`):**
- Creates API endpoints
- Handles HTTP requests
- Calls model methods
- Returns JSON responses

**Together:**
1. User requests → Controller
2. Controller → Model
3. Model → Database
4. Database → Model
5. Model → Controller
6. Controller → User (JSON response)

That's it! You now have a working Product API! 🎉

