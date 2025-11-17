# -*- coding: utf-8 -*-
{
    'name': 'Product API',
    'version': '18.0.1.0.0',
    'category': 'API',
    'summary': 'REST API for Product Data',
    'description': """
        Product API Addon
        =================
        
        This addon provides REST API endpoints to access product data.
        
        Features:
        - Get all products
        - Get single product by ID
        - Search products with filters
        - Get products by category
        
        Usage:
        - GET /api/products - Get all products
        - GET /api/products/{id} - Get single product
        - GET /api/products/search?name=desk - Search products
    """,
    'author': 'Your Name',
    'website': 'https://www.odoo.com',
    'license': 'LGPL-3',
    'depends': ['base', 'product', 'stock'],
    'data': [
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}

