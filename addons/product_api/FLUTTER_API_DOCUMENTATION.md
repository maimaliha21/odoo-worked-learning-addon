# 📱 Flutter Integration - Complete API Documentation

## 🎯 What You Need to Build in Flutter

When RFID reader detects a barcode → Call Odoo API → Display product in basket

---

## 📡 API Endpoints Available

### Base URL
```
http://YOUR_ODOO_SERVER:8069
```
**Note:** Replace `YOUR_ODOO_SERVER` with your actual server IP (e.g., `192.168.1.100` or `localhost` for testing)

---

## 🔍 API 1: Search Product by Barcode (Main One You'll Use)

**Endpoint:**
```
GET /api/products/search?barcode={BARCODE}
```

**When to use:** When RFID reader detects a tag/barcode

**Example Request:**
```dart
// RFID reader detects: "ABC123XYZ"
final url = Uri.parse('http://YOUR_SERVER:8069/api/products/search?barcode=ABC123XYZ');
final response = await http.get(url);
```

**Response (Success):**
```json
{
  "products": [
    {
      "id": 1,
      "name": "Blue Denim Jeans",
      "default_code": "FURN_5555",
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

**Response (Not Found):**
```json
{
  "products": [],
  "total": 0,
  "limit": 10,
  "offset": 0
}
```

**Flutter Code:**
```dart
import 'dart:convert';
import 'package:http/http.dart' as http;

Future<Map<String, dynamic>?> getProductByBarcode(String barcode) async {
  try {
    final url = Uri.parse('http://YOUR_SERVER:8069/api/products/search?barcode=$barcode');
    final response = await http.get(url);
    
    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      
      if (data['products'] != null && data['products'].length > 0) {
        return data['products'][0];  // Return first product
      }
    }
    return null;  // Product not found
  } catch (e) {
    print('Error: $e');
    return null;
  }
}
```

---

## 📦 API 2: Get All Products (Optional - For Testing)

**Endpoint:**
```
GET /api/products?limit={LIMIT}&offset={OFFSET}
```

**Query Parameters:**
- `limit` (optional): Number of products (default: 100)
- `offset` (optional): Skip products (default: 0)

**Example Request:**
```dart
final url = Uri.parse('http://YOUR_SERVER:8069/api/products?limit=10');
final response = await http.get(url);
```

**Response:**
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
    },
    {
      "id": 2,
      "name": "Casual Denim Short",
      "reference": "",
      "barcode": "XYZ789",
      "price": 35.0,
      "quantity": 56.0,
      "image_url": "/web/image/product.template/2/image_128"
    }
  ],
  "total": 2,
  "limit": 10,
  "offset": 0
}
```

---

## 🔍 API 3: Get Single Product by ID

**Endpoint:**
```
GET /api/products/{PRODUCT_ID}
```

**Example Request:**
```dart
final url = Uri.parse('http://YOUR_SERVER:8069/api/products/1');
final response = await http.get(url);
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
  "uom_id": {
    "id": 1,
    "name": "Units"
  },
  "image_url": "/web/image/product.template/1/image_1920",
  "active": true,
  "description": "",
  "description_sale": ""
}
```

---

## ✅ API 4: Health Check

**Endpoint:**
```
GET /api/products/health
```

**Use for:** Testing if API is accessible

**Response:**
```json
{
  "status": "ok",
  "message": "Product API is running"
}
```

**Flutter Code:**
```dart
Future<bool> checkApiConnection() async {
  try {
    final url = Uri.parse('http://YOUR_SERVER:8069/api/products/health');
    final response = await http.get(url);
    return response.statusCode == 200;
  } catch (e) {
    return false;
  }
}
```

---

## 🎨 API 5: Get Product Image

**Endpoint:**
```
GET http://YOUR_SERVER:8069/web/image/product.template/{PRODUCT_ID}/image_128
```

**Note:** This is not an API endpoint, but how to build image URLs

**From API response, you get:**
```json
{
  "image_url": "/web/image/product.template/1/image_128"
}
```

**Build full URL:**
```dart
String getImageUrl(String? imagePath) {
  if (imagePath == null || imagePath.isEmpty) return '';
  const baseUrl = 'http://YOUR_SERVER:8069';
  return '$baseUrl$imagePath';
}

// Usage:
final imageUrl = getImageUrl(productData['image_url']);
// Result: "http://YOUR_SERVER:8069/web/image/product.template/1/image_128"
```

---

## 🔄 Complete Integration Example

### Step 1: Create API Service Class

**File: `lib/services/odoo_api_service.dart`**

```dart
import 'dart:convert';
import 'package:http/http.dart' as http;

class OdooApiService {
  // ⚠️ CHANGE THIS TO YOUR ODOO SERVER URL
  static const String baseUrl = 'http://YOUR_SERVER_IP:8069';
  
  /// Search product by barcode (RFID tag)
  /// This is the main method you'll use
  static Future<Map<String, dynamic>?> searchProductByBarcode(String barcode) async {
    try {
      final url = Uri.parse('$baseUrl/api/products/search?barcode=$barcode');
      print('🔍 Searching for barcode: $barcode');
      
      final response = await http.get(url);
      
      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        
        if (data['products'] != null && data['products'].length > 0) {
          print('✅ Product found');
          return data['products'][0];
        } else {
          print('❌ Product not found');
          return null;
        }
      } else {
        print('❌ HTTP Error: ${response.statusCode}');
        return null;
      }
    } catch (e) {
      print('❌ Exception: $e');
      return null;
    }
  }
  
  /// Build full image URL
  static String getImageUrl(String? imagePath) {
    if (imagePath == null || imagePath.isEmpty) return '';
    if (imagePath.startsWith('http')) return imagePath;
    return '$baseUrl$imagePath';
  }
  
  /// Health check
  static Future<bool> checkConnection() async {
    try {
      final url = Uri.parse('$baseUrl/api/products/health');
      final response = await http.get(url);
      return response.statusCode == 200;
    } catch (e) {
      return false;
    }
  }
}
```

### Step 2: Create Product Model (Optional but Recommended)

**File: `lib/models/product.dart`**

```dart
class Product {
  final int id;
  final String name;
  final String reference;
  final String barcode;
  final double price;
  final double quantity;
  final String? imageUrl;
  
  Product({
    required this.id,
    required this.name,
    required this.reference,
    required this.barcode,
    required this.price,
    required this.quantity,
    this.imageUrl,
  });
  
  factory Product.fromJson(Map<String, dynamic> json) {
    return Product(
      id: json['id'] ?? 0,
      name: json['name'] ?? 'Unknown Product',
      reference: json['reference'] ?? json['default_code'] ?? '',
      barcode: json['barcode'] ?? '',
      price: (json['price'] ?? json['list_price'] ?? 0.0).toDouble(),
      quantity: (json['quantity'] ?? json['qty_available'] ?? 0.0).toDouble(),
      imageUrl: json['image_url'],
    );
  }
}
```

### Step 3: Integrate with RFID Reader

**In your RFID service/widget:**

```dart
import 'services/odoo_api_service.dart';
import 'models/product.dart';

// When RFID reader detects a tag
void onRfidTagDetected(String rfidTag) async {
  print('📡 RFID tag detected: $rfidTag');
  
  // Call Odoo API
  final productData = await OdooApiService.searchProductByBarcode(rfidTag);
  
  if (productData != null) {
    // Product found - convert to Product object
    final product = Product.fromJson(productData);
    
    // Add to basket (your existing basket service)
    basketService.addProduct(product);
    
    // Update UI
    setState(() {});
    
    // Show success message
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text('${product.name} added to basket')),
    );
  } else {
    // Product not found
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text('Product not found for RFID: $rfidTag'),
        backgroundColor: Colors.red,
      ),
    );
  }
}
```

### Step 4: Display Product in Basket

**In your basket item widget:**

```dart
import 'services/odoo_api_service.dart';

Widget buildBasketItem(Product product) {
  final imageUrl = OdooApiService.getImageUrl(product.imageUrl);
  
  return ListTile(
    leading: imageUrl.isNotEmpty
        ? Image.network(
            imageUrl,
            width: 60,
            height: 60,
            fit: BoxFit.cover,
            errorBuilder: (context, error, stackTrace) => 
                Icon(Icons.image, size: 60),
          )
        : Icon(Icons.image, size: 60),
    title: Text(product.name),
    subtitle: Text('RFID: ${product.barcode}'),
    trailing: Text(
      '\$${product.price.toStringAsFixed(2)}',
      style: TextStyle(
        fontSize: 18,
        fontWeight: FontWeight.bold,
        color: Colors.green[700],
      ),
    ),
  );
}
```

---

## 📋 Data Fields Mapping

| Odoo API Field | Flutter Usage | Description |
|----------------|---------------|-------------|
| `id` | `product.id` | Product ID |
| `name` | `product.name` | Product name |
| `barcode` | `product.barcode` | RFID tag / Barcode |
| `list_price` or `price` | `product.price` | Product price |
| `image_url` | `product.imageUrl` | Image path (add server URL) |
| `qty_available` or `quantity` | `product.quantity` | Stock quantity |
| `reference` or `default_code` | `product.reference` | Product reference |

---

## 🔧 Configuration

### 1. Add HTTP Package

**In `pubspec.yaml`:**
```yaml
dependencies:
  flutter:
    sdk: flutter
  http: ^1.1.0
```

**Run:**
```bash
flutter pub get
```

### 2. Set Server URL

**In `lib/services/odoo_api_service.dart`:**
```dart
static const String baseUrl = 'http://192.168.1.100:8069';  // Your server IP
```

**For testing on same machine:**
```dart
static const String baseUrl = 'http://localhost:8069';
```

**For device testing:**
```dart
static const String baseUrl = 'http://YOUR_COMPUTER_IP:8069';
// Find your IP: ipconfig (Windows) or ifconfig (Mac/Linux)
```

---

## 🎯 Complete Flow Summary

```
1. RFID Reader detects tag: "ABC123"
   ↓
2. Call: GET /api/products/search?barcode=ABC123
   ↓
3. Odoo returns product data (if found)
   ↓
4. Parse JSON response
   ↓
5. Create Product object
   ↓
6. Add to basket
   ↓
7. Display in UI
```

---

## 🐛 Error Handling

```dart
Future<Map<String, dynamic>?> searchProductByBarcode(String barcode) async {
  try {
    final url = Uri.parse('$baseUrl/api/products/search?barcode=$barcode');
    final response = await http.get(url);
    
    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      if (data['products'] != null && data['products'].length > 0) {
        return data['products'][0];
      }
      return null;  // Product not found
    } else if (response.statusCode == 404) {
      print('API endpoint not found');
      return null;
    } else {
      print('Server error: ${response.statusCode}');
      return null;
    }
  } on SocketException {
    print('Cannot connect to server');
    return null;
  } on TimeoutException {
    print('Request timeout');
    return null;
  } catch (e) {
    print('Error: $e');
    return null;
  }
}
```

---

## ✅ Checklist for Flutter Integration

- [ ] Add `http` package to `pubspec.yaml`
- [ ] Create `OdooApiService` class
- [ ] Set correct server URL
- [ ] Connect RFID reader callback to API call
- [ ] Handle product found/not found cases
- [ ] Display product in basket UI
- [ ] Build image URLs correctly
- [ ] Test with real RFID tags

---

## 🚀 Quick Start Code

**Minimal example:**

```dart
// When RFID detects tag
void handleRfidTag(String tag) async {
  final url = Uri.parse('http://YOUR_SERVER:8069/api/products/search?barcode=$tag');
  final response = await http.get(url);
  final data = json.decode(response.body);
  
  if (data['products'].length > 0) {
    final product = data['products'][0];
    // Use product data:
    // product['name']
    // product['list_price']
    // product['image_url']
    // product['barcode']
  }
}
```

---

## 📞 Summary

**Main API to use:**
```
GET /api/products/search?barcode={RFID_TAG}
```

**What to do:**
1. Call this API when RFID detects a tag
2. Get product data from response
3. Display in your basket UI

**That's it!** 🎉

