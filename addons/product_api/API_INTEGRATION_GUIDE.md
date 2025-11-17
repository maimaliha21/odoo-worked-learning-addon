# 🔗 Odoo API Integration Guide for Your Flutter Project

## 🎯 What You Need

When RFID reader detects a tag → Call Odoo API → Get product data → Display in basket

## 📡 API Endpoints You'll Use

### 1. Search Product by Barcode (RFID Tag)

**Endpoint:**
```
GET http://YOUR_ODOO_SERVER:8069/api/products/search?barcode=RFID_TAG_ID
```

**Example:**
```
GET http://localhost:8069/api/products/search?barcode=ABC123XYZ
```

**Response:**
```json
{
  "products": [
    {
      "id": 1,
      "name": "Blue Denim Jeans",
      "reference": "FURN_5555",
      "barcode": "ABC123XYZ",
      "list_price": 80.0,
      "qty_available": 50.0,
      "type": "product",
      "categ_id": "All",
      "image_url": "/web/image/product.template/1/image_128"
    }
  ],
  "total": 1,
  "limit": 10,
  "offset": 0
}
```

**Usage in Flutter:**
```dart
// When RFID tag is detected
String rfidTag = "ABC123XYZ";  // From your RFID reader

// Call Odoo API
final url = Uri.parse('http://YOUR_SERVER:8069/api/products/search?barcode=$rfidTag');
final response = await http.get(url);

if (response.statusCode == 200) {
  final data = json.decode(response.body);
  if (data['products'].length > 0) {
    final product = data['products'][0];
    // Use product data:
    // - product['name']
    // - product['list_price']
    // - product['image_url']
    // - product['barcode']
  }
}
```

### 2. Get Product Image

**Endpoint:**
```
GET http://YOUR_ODOO_SERVER:8069/web/image/product.template/{PRODUCT_ID}/image_128
```

**Example:**
```
GET http://localhost:8069/web/image/product.template/1/image_128
```

**Usage:**
```dart
// From API response, you get: "/web/image/product.template/1/image_128"
String imagePath = product['image_url'];
String fullImageUrl = 'http://YOUR_SERVER:8069$imagePath';
// Use fullImageUrl in Image.network() or CachedNetworkImage
```

### 3. Get Single Product by ID (Optional)

**Endpoint:**
```
GET http://YOUR_ODOO_SERVER:8069/api/products/{PRODUCT_ID}
```

**Example:**
```
GET http://localhost:8069/api/products/1
```

**Response:**
```json
{
  "id": 1,
  "name": "Blue Denim Jeans",
  "default_code": "FURN_5555",
  "barcode": "ABC123XYZ",
  "list_price": 80.0,
  "standard_price": 72.0,
  "qty_available": 50.0,
  "virtual_available": 50.0,
  "type": "product",
  "categ_id": {
    "id": 1,
    "name": "All"
  },
  "image_url": "/web/image/product.template/1/image_1920",
  "active": true,
  "description": "",
  "description_sale": ""
}
```

## 🔄 Complete Integration Flow

### Step 1: RFID Tag Detected

Your RFID reader API detects a tag and gives you the tag ID:
```dart
// Your RFID service callback
void onRfidTagDetected(String rfidTag) {
  // rfidTag = "ABC123XYZ" (example)
  _fetchProductFromOdoo(rfidTag);
}
```

### Step 2: Call Odoo API

```dart
Future<void> _fetchProductFromOdoo(String rfidTag) async {
  try {
    final url = Uri.parse(
      'http://YOUR_ODOO_SERVER:8069/api/products/search?barcode=$rfidTag'
    );
    
    final response = await http.get(url);
    
    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      
      if (data['products'] != null && data['products'].length > 0) {
        final productData = data['products'][0];
        
        // Add to your basket
        _addToBasket(productData);
      } else {
        // Product not found
        _showError('Product not found for RFID: $rfidTag');
      }
    }
  } catch (e) {
    _showError('Error: $e');
  }
}
```

### Step 3: Add to Basket

```dart
void _addToBasket(Map<String, dynamic> productData) {
  // Create product object (adjust to your model)
  final product = {
    'id': productData['id'],
    'name': productData['name'],
    'price': productData['list_price'],
    'barcode': productData['barcode'],
    'imageUrl': 'http://YOUR_SERVER:8069${productData['image_url']}',
    'quantity': productData['qty_available'],
  };
  
  // Add to your existing basket
  basketService.addProduct(product);
  
  // Update UI
  setState(() {});
}
```

## 📋 Data Mapping

| Odoo API Field | Use In Flutter |
|----------------|----------------|
| `id` | Product ID |
| `name` | Product name |
| `list_price` | Price |
| `barcode` | RFID tag / Barcode |
| `image_url` | Image path (add server URL) |
| `qty_available` | Stock quantity |
| `reference` or `default_code` | Product reference |

## 🎨 Display Product in Basket

Based on your basket UI, use the data like this:

```dart
// Product name
Text(product['name'])

// Price
Text('\$${product['price']}')

// Image
Image.network(product['imageUrl'])

// RFID/Barcode
Text('RFID: ${product['barcode']}')
```

## 🔧 Configuration

### Change Odoo Server URL

In your Flutter project, create a config file:

```dart
class ApiConfig {
  static const String odooBaseUrl = 'http://YOUR_SERVER_IP:8069';
  // For local testing: 'http://localhost:8069'
  // For device: 'http://192.168.1.100:8069' (your computer's IP)
}
```

### Build Image URL

```dart
String getImageUrl(String? imagePath) {
  if (imagePath == null || imagePath.isEmpty) return '';
  if (imagePath.startsWith('http')) return imagePath;
  return '${ApiConfig.odooBaseUrl}$imagePath';
}
```

## ✅ Checklist

- [ ] Odoo server is running and accessible
- [ ] Products in Odoo have barcode field = RFID tag ID
- [ ] Test API in browser: `http://YOUR_SERVER:8069/api/products/search?barcode=TEST_TAG`
- [ ] RFID reader is detecting tags
- [ ] Flutter app can make HTTP requests to Odoo server
- [ ] Basket UI is ready to display products

## 🐛 Troubleshooting

### Product Not Found
- **Check:** RFID tag matches barcode in Odoo exactly
- **Test:** `curl "http://YOUR_SERVER:8069/api/products/search?barcode=YOUR_TAG"`
- **Fix:** Make sure barcode field in Odoo product = RFID tag ID

### Can't Connect to Odoo
- **Check:** Odoo server is running
- **Check:** Server IP is correct
- **Test:** `curl http://YOUR_SERVER:8069/api/products/health`
- **Fix:** Use computer's IP address, not localhost (for device testing)

### Images Not Loading
- **Check:** Image URL is full URL: `http://SERVER:8069/web/image/...`
- **Check:** Odoo server is accessible from device
- **Fix:** Use `getImageUrl()` helper to build full URL

## 📝 Summary

**Simple Integration:**
1. RFID detects tag → Get tag ID
2. Call: `GET /api/products/search?barcode={TAG_ID}`
3. Get product data from response
4. Display in your existing basket UI

**That's it!** Just use the API endpoints in your existing Flutter code. 🎉

