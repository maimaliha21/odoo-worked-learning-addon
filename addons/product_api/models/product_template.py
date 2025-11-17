# -*- coding: utf-8 -*-

from odoo import models, api
import logging

_logger = logging.getLogger(__name__)


class ProductTemplate(models.Model):
    """
    Extend product.template model with custom API methods
    """
    _inherit = 'product.template'

    @api.model
    def get_product_info(self, product_id):
        """
        Get detailed information about a single product
        
        Args:
            product_id (int): ID of the product
            
        Returns:
            dict: Product information or error message
        """
        try:
            product = self.browse(product_id)
            
            if not product.exists():
                return {'error': f'Product with ID {product_id} not found'}
            
            # Get product data
            product_data = {
                'id': product.id,
                'name': product.name,
                'default_code': product.default_code or '',
                'barcode': product.barcode or '',
                'list_price': product.list_price,
                'standard_price': product.standard_price,
                'qty_available': product.qty_available,
                'virtual_available': product.virtual_available,
                'type': product.type,
                'categ_id': {
                    'id': product.categ_id.id if product.categ_id else None,
                    'name': product.categ_id.name if product.categ_id else 'All'
                },
                'uom_id': {
                    'id': product.uom_id.id if product.uom_id else None,
                    'name': product.uom_id.name if product.uom_id else 'Units'
                },
                'image_url': f'/web/image/product.template/{product.id}/image_1920' if product.image_1920 else None,
                'active': product.active,
                'description': product.description or '',
                'description_sale': product.description_sale or '',
            }
            
            return product_data
            
        except Exception as e:
            _logger.error(f"Error getting product info: {str(e)}")
            return {'error': str(e)}

    @api.model
    def search_products(self, filters=None, limit=10, offset=0):
        """
        Search products with various filters
        
        Args:
            filters (dict): Dictionary of filters
                - name: Product name (partial match)
                - default_code: Product reference
                - barcode: Product barcode (exact match)
                - category: Category name
                - min_price: Minimum price
                - max_price: Maximum price
                - type: Product type (consu, service, product)
            limit (int): Number of results to return
            offset (int): Number of results to skip
            
        Returns:
            dict: Dictionary with products list and metadata
        """
        try:
            filters = filters or {}
            domain = []
            
            # Build search domain based on filters
            if filters.get('name'):
                domain.append(('name', 'ilike', filters['name']))
            
            if filters.get('default_code'):
                domain.append(('default_code', '=', filters['default_code']))
            
            if filters.get('barcode'):
                domain.append(('barcode', '=', filters['barcode']))
            
            if filters.get('category'):
                domain.append(('categ_id.name', 'ilike', filters['category']))
            
            if filters.get('min_price'):
                domain.append(('list_price', '>=', float(filters['min_price'])))
            
            if filters.get('max_price'):
                domain.append(('list_price', '<=', float(filters['max_price'])))
            
            if filters.get('type'):
                domain.append(('type', '=', filters['type']))
            
            # Search products
            products = self.search(domain, limit=limit, offset=offset, order='name')
            
            # Format results
            result = []
            for product in products:
                result.append({
                    'id': product.id,
                    'name': product.name,
                    'default_code': product.default_code or '',
                    'barcode': product.barcode or '',
                    'list_price': product.list_price,
                    'qty_available': product.qty_available,
                    'type': product.type,
                    'categ_id': product.categ_id.name if product.categ_id else 'All',
                    'image_url': f'/web/image/product.template/{product.id}/image_128' if product.image_128 else None,
                })
            
            # Get total count (without limit)
            total_count = self.search_count(domain)
            
            return {
                'products': result,
                'total': total_count,
                'limit': limit,
                'offset': offset
            }
            
        except Exception as e:
            _logger.error(f"Error searching products: {str(e)}")
            return {
                'products': [],
                'total': 0,
                'error': str(e)
            }

    @api.model
    def get_all_products_simple(self, limit=100, offset=0):
        """
        Get all products in simple format
        
        Args:
            limit (int): Number of products to return
            offset (int): Number of products to skip
            
        Returns:
            list: List of product dictionaries
        """
        try:
            products = self.search([], limit=limit, offset=offset, order='name')
            
            result = []
            for product in products:
                result.append({
                    'id': product.id,
                    'name': product.name,
                    'reference': product.default_code or '',
                    'barcode': product.barcode or '',
                    'price': product.list_price,
                    'quantity': product.qty_available,
                    'image_url': f'/web/image/product.template/{product.id}/image_128' if product.image_128 else None,
                })
            
            return result
            
        except Exception as e:
            _logger.error(f"Error getting all products: {str(e)}")
            return []

    @api.model
    def get_products_by_category(self, category_name):
        """
        Get all products in a specific category
        
        Args:
            category_name (str): Name of the category
            
        Returns:
            list: List of product dictionaries
        """
        try:
            # Search for category
            category = self.env['product.category'].search([
                ('name', 'ilike', category_name)
            ], limit=1)
            
            if not category:
                return []
            
            # Get products in this category
            products = self.search([
                ('categ_id', '=', category.id)
            ], order='name')
            
            result = []
            for product in products:
                result.append({
                    'id': product.id,
                    'name': product.name,
                    'default_code': product.default_code or '',
                    'barcode': product.barcode or '',
                    'list_price': product.list_price,
                    'qty_available': product.qty_available,
                    'category': category.name,
                    'image_url': f'/web/image/product.template/{product.id}/image_128' if product.image_128 else None,
                })
            
            return result
            
        except Exception as e:
            _logger.error(f"Error getting products by category: {str(e)}")
            return []

