# -*- coding: utf-8 -*-

import json
import logging
from odoo import http
from odoo.http import request, Response

_logger = logging.getLogger(__name__)


class ProductAPIController(http.Controller):
    """
    REST API Controller for Product Data
    
    All endpoints return JSON responses
    """

    def _json_response(self, data, status=200):
        """Helper to create JSON response"""
        return Response(
            json.dumps(data, ensure_ascii=False, default=str),
            status=status,
            mimetype='application/json'
        )

    def _error_response(self, message, status=400):
        """Helper to create error response"""
        return self._json_response({
            'error': True,
            'message': message
        }, status=status)

    # ============================================
    # Public Endpoints (No Authentication)
    # ============================================

    @http.route('/api/products/health', type='http', auth='public', methods=['GET'], csrf=False)
    def health_check(self):
        """
        Health check endpoint
        
        GET /api/products/health
        
        Returns:
            {"status": "ok", "message": "Product API is running"}
        """
        return self._json_response({
            'status': 'ok',
            'message': 'Product API is running'
        })

    @http.route('/api/products', type='http', auth='public', methods=['GET'], csrf=False)
    def get_all_products(self, **kwargs):
        """
        Get all products (simple list)
        
        GET /api/products
        
        Query Parameters:
            limit (int): Number of products to return (default: 100)
            offset (int): Number of products to skip (default: 0)
        
        Example:
            GET /api/products?limit=10&offset=0
        
        Returns:
            {
                "products": [
                    {
                        "id": 1,
                        "name": "Product Name",
                        "reference": "REF001",
                        "price": 100.00,
                        "quantity": 50.0
                    },
                    ...
                ]
            }
        """
        try:
            limit = int(kwargs.get('limit', 100))
            offset = int(kwargs.get('offset', 0))
            
            products = request.env['product.template'].sudo().get_all_products_simple(
                limit=limit,
                offset=offset
            )
            
            return self._json_response({
                'products': products,
                'total': len(products),
                'limit': limit,
                'offset': offset
            })
        except Exception as e:
            _logger.error(f"Error in get_all_products: {str(e)}")
            return self._error_response(str(e), 500)

    @http.route('/api/products/<int:product_id>', type='http', auth='public', methods=['GET'], csrf=False)
    def get_product(self, product_id):
        """
        Get single product by ID
        
        GET /api/products/{product_id}
        
        Example:
            GET /api/products/1
        
        Returns:
            {
                "id": 1,
                "name": "Product Name",
                "default_code": "REF001",
                "list_price": 100.00,
                "standard_price": 80.00,
                "qty_available": 50.0,
                "type": "product",
                "categ_id": {"id": 1, "name": "Category"},
                "image_url": "/web/image/...",
                "description": "Product description",
                ...
            }
        """
        try:
            product_info = request.env['product.template'].sudo().get_product_info(product_id)
            
            if 'error' in product_info:
                return self._error_response(product_info['error'], 404)
            
            return self._json_response(product_info)
        except Exception as e:
            _logger.error(f"Error in get_product: {str(e)}")
            return self._error_response(str(e), 500)

    @http.route('/api/products/search', type='http', auth='public', methods=['GET'], csrf=False)
    def search_products(self, **kwargs):
        """
        Search products with filters
        
        GET /api/products/search
        
        Query Parameters:
            name (str): Product name (partial match)
            default_code (str): Product reference
            barcode (str): Product barcode (exact match)
            category (str): Category name
            min_price (float): Minimum price
            max_price (float): Maximum price
            type (str): Product type (consu, service, product)
            limit (int): Number of results (default: 10)
            offset (int): Skip results (default: 0)
        
        Examples:
            GET /api/products/search?name=shirt
            GET /api/products/search?barcode=1234567890123
            GET /api/products/search?category=clothing&min_price=10&max_price=50
            GET /api/products/search?type=product&limit=20
        
        Returns:
            {
                "products": [...],
                "total": 15,
                "limit": 10,
                "offset": 0
            }
        """
        try:
            filters = {}
            
            # Extract filter parameters
            if kwargs.get('name'):
                filters['name'] = kwargs['name']
            if kwargs.get('default_code'):
                filters['default_code'] = kwargs['default_code']
            if kwargs.get('barcode'):
                filters['barcode'] = kwargs['barcode']
            if kwargs.get('category'):
                filters['category'] = kwargs['category']
            if kwargs.get('min_price'):
                filters['min_price'] = kwargs['min_price']
            if kwargs.get('max_price'):
                filters['max_price'] = kwargs['max_price']
            if kwargs.get('type'):
                filters['type'] = kwargs['type']
            
            limit = int(kwargs.get('limit', 10))
            offset = int(kwargs.get('offset', 0))
            
            result = request.env['product.template'].sudo().search_products(
                filters=filters,
                limit=limit,
                offset=offset
            )
            
            return self._json_response(result)
        except Exception as e:
            _logger.error(f"Error in search_products: {str(e)}")
            return self._error_response(str(e), 500)

    @http.route('/api/products/category/<string:category_name>', type='http', auth='public', methods=['GET'], csrf=False)
    def get_by_category(self, category_name):
        """
        Get products by category
        
        GET /api/products/category/{category_name}
        
        Example:
            GET /api/products/category/clothing
        
        Returns:
            {
                "category": "Clothing",
                "products": [...]
            }
        """
        try:
            products = request.env['product.template'].sudo().get_products_by_category(category_name)
            
            return self._json_response({
                'category': category_name,
                'products': products,
                'count': len(products)
            })
        except Exception as e:
            _logger.error(f"Error in get_by_category: {str(e)}")
            return self._error_response(str(e), 500)

