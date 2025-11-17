from odoo import models, fields


class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Library Book'

    name = fields.Char(string="Book Title", required=True)
    published_date = fields.Date(string="Published Date")
    author_id = fields.Many2one('library.author', string="Author")
