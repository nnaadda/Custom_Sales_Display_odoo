{
    'name': 'Custom Sales Partner Display',
    'version': '18.0.1.0.0',
    'category': 'Sales',
    'summary': 'Enhance partner display in sales orders to show name and job position',
    'description': """
        This module extends the sales functionality to display partner information
        with both name and job position in the debug menu and other views.
    """,
    'author': 'Nada',
    'website': 'https://yourcompany.com',
    'depends': ['sale', 'base'],
    'data': [
        'views/partner_job_views.xml',
        'views/partner_job_menu.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
