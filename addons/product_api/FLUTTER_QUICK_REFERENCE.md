# 🚀 Flutter Quick Reference Card

## Main API Endpoint (Use This One!)

```
GET http://YOUR_SERVER:8069/api/products/search?barcode={RFID_TAG}
```

## Quick Code

```dart
import 'package:http/http.dart' as http;
import 'dart:convert';

// When RFID detects tag
Future<void> handleRfidTag(String rfidTag) async {
  final url = Uri.parse('http://YOUR_SERVER:8069/api/products/search?barcode=$rfidTag');
  final response = await http.get(url);
  final data = json.decode(response.body);
  
  if (data['products'].length > 0) {
    final product = data['products'][0];
    // product['name'] - Product name
    // product['list_price'] - Price
    // product['image_url'] - Image path
    // product['barcode'] - Barcode/RFID
  }
}
```

## Response Format

```json
{
  "products": [{
    "id": 1,
    "name": "Product Name",
    "barcode": "ABC123",
    "list_price": 80.0,
    "image_url": "/web/image/product.template/1/image_128"
  }]
}
```

## Image URL

```dart
String imageUrl = 'http://YOUR_SERVER:8069${product['image_url']}';
```

## All Available Endpoints

1. **Search by barcode:** `GET /api/products/search?barcode={TAG}`
2. **Get all products:** `GET /api/products?limit=10`
3. **Get single product:** `GET /api/products/{id}`
4. **Health check:** `GET /api/products/health`

## Setup

1. Add to `pubspec.yaml`:
   ```yaml
   dependencies:
     http: ^1.1.0
   ```

2. Set server URL:
   ```dart
   const baseUrl = 'http://YOUR_SERVER_IP:8069';
   ```

3. Call API when RFID detects tag

**That's it!** See `FLUTTER_API_DOCUMENTATION.md` for complete guide.

