# 🌐 Web Testing - API Endpoints

## 🎯 Test APIs in Your Browser

Copy and paste these URLs into your browser to test the APIs.

**Base URL:** `http://localhost:8069` (or your server IP)

---

## ✅ 1. Health Check

**URL:**
```
http://localhost:8069/api/products/health
```

**Expected Response:**
```json
{
  "status": "ok",
  "message": "Product API is running"
}
```

**Test it:** Just paste the URL in your browser!

---

## 📦 2. Get All Products

**URL:**
```
http://localhost:8069/api/products?limit=5
```

**With more products:**
```
http://localhost:8069/api/products?limit=10&offset=0
```

**Expected Response:**
```json
{
  "products": [
    {
      "id": 1,
      "name": "Cable Management Box",
      "reference": "FURN_5555",
      "barcode": "ABC123",
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

---

## 🔍 3. Get Single Product by ID

**URL (replace 1 with actual product ID):**
```
http://localhost:8069/api/products/1
```

**Try different IDs:**
```
http://localhost:8069/api/products/2
http://localhost:8069/api/products/3
```

**Expected Response:**
```json
{
  "id": 1,
  "name": "Blue Denim Jeans",
  "default_code": "FURN_5555",
  "barcode": "ABC123XYZ",
  "list_price": 80.0,
  "standard_price": 72.0,
  "qty_available": 50.0,
  "type": "product",
  "categ_id": {
    "id": 1,
    "name": "All"
  },
  "image_url": "/web/image/product.template/1/image_1920"
}
```

---

## 🔎 4. Search Products by Barcode (Main One for RFID!)

**URL (replace ABC123 with actual barcode from your products):**
```
http://localhost:8069/api/products/search?barcode=ABC123
```

**Try with different barcodes:**
```
http://localhost:8069/api/products/search?barcode=XYZ789
http://localhost:8069/api/products/search?barcode=123456
```

**Expected Response (Found):**
```json
{
  "products": [
    {
      "id": 1,
      "name": "Blue Denim Jeans",
      "barcode": "ABC123",
      "list_price": 80.0,
      "qty_available": 50.0,
      "image_url": "/web/image/product.template/1/image_128"
    }
  ],
  "total": 1
}
```

**Expected Response (Not Found):**
```json
{
  "products": [],
  "total": 0,
  "limit": 10,
  "offset": 0
}
```

---

## 🔎 5. Search Products by Name

**URL:**
```
http://localhost:8069/api/products/search?name=desk
```

**Try different searches:**
```
http://localhost:8069/api/products/search?name=chair
http://localhost:8069/api/products/search?name=jeans
http://localhost:8069/api/products/search?name=shirt
```

---

## 🔎 6. Search Products by Price Range

**URL:**
```
http://localhost:8069/api/products/search?min_price=10&max_price=50
```

**Try different ranges:**
```
http://localhost:8069/api/products/search?min_price=50&max_price=100
http://localhost:8069/api/products/search?min_price=0&max_price=20
```

---

## 🔎 7. Search Products by Category

**URL:**
```
http://localhost:8069/api/products/search?category=furniture
```

**Try different categories:**
```
http://localhost:8069/api/products/search?category=clothing
http://localhost:8069/api/products/search?category=all
```

---

## 📂 8. Get Products by Category

**URL:**
```
http://localhost:8069/api/products/category/all
```

**Try different categories:**
```
http://localhost:8069/api/products/category/furniture
http://localhost:8069/api/products/category/clothing
```

---

## 🧪 Testing Steps

### Step 1: Test Health Check
1. Open browser
2. Go to: `http://localhost:8069/api/products/health`
3. Should see: `{"status": "ok", "message": "Product API is running"}`

### Step 2: Get All Products
1. Go to: `http://localhost:8069/api/products?limit=5`
2. Should see list of products

### Step 3: Find a Product Barcode
1. Look at the products list
2. Note a barcode value (e.g., "ABC123")
3. Or check in Odoo: Inventory → Products → Open a product → Check "Barcode" field

### Step 4: Test Barcode Search
1. Go to: `http://localhost:8069/api/products/search?barcode=YOUR_BARCODE`
2. Replace `YOUR_BARCODE` with actual barcode from Step 3
3. Should see the product if barcode exists

### Step 5: Test Single Product
1. Get a product ID from the products list
2. Go to: `http://localhost:8069/api/products/1` (replace 1 with actual ID)
3. Should see detailed product info

---

## 🔧 If Using Different Server

**Replace `localhost` with your server IP:**

```
http://192.168.1.100:8069/api/products/health
http://192.168.1.100:8069/api/products?limit=5
http://192.168.1.100:8069/api/products/search?barcode=ABC123
```

---

## 📝 Quick Test Checklist

- [ ] Health check works: `/api/products/health`
- [ ] Get all products works: `/api/products?limit=5`
- [ ] Get single product works: `/api/products/1`
- [ ] Search by barcode works: `/api/products/search?barcode=XXX`
- [ ] Search by name works: `/api/products/search?name=desk`
- [ ] Images load: Check `image_url` in response

---

## 🎯 Most Important for RFID Integration

**This is the one you'll use in Flutter:**
```
http://localhost:8069/api/products/search?barcode={RFID_TAG}
```

**Test it:**
1. Get a barcode from one of your products
2. Replace `{RFID_TAG}` with that barcode
3. Paste in browser
4. Should return the product!

---

## 🐛 Troubleshooting

### "404 Not Found"
- Check module is installed in Odoo
- Verify URL is correct
- Try health check first

### "Empty products list"
- Make sure you have products in Odoo
- Check products have barcodes (if searching by barcode)
- Try getting all products first

### "Connection refused"
- Check Odoo server is running
- Verify port 8069 is correct
- Check firewall settings

---

## ✅ Ready to Test!

Just copy the URLs above and paste them in your browser! 🚀

