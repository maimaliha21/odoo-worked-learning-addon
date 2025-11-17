{
    'name': "Mai's Try",
    'version': '18.0.1.0.0',
    'license': 'LGPL-3',
    'depends': ['base', 'web'],
    'application': True,
    'author':'Mai Maliha',
    'installable': True,
    'demo': ['demo/demo.xml'],
       'data': [
        'security/ir.model.access.csv',
        'views/library_author_views.xml',
        'views/library_book_views.xml',
        'views/templates.xml',
    ],
}