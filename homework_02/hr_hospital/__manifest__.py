{
    'name': 'HR Hospital',
    'author': 'Lisivka Sergii',
    'summary': '',
    'website': 'https://odoo.school/',
    'category': 'Customizations',
    'version': '17.0.0.0.0',
    'license': 'OPL-1',
    'depends': [
        'base',
    ],

    'external_dependencies': {
        'python': [],
    },

    'data': [
        'security/ir.model.access.csv',
        'views/hr_hospital_menu.xml',
        'views/disease_views.xml',
        'views/doctor_views.xml',
        'views/patient_views.xml',
        'views/visit_views.xml',
    ],
    'demo': [],

    'installable': True,
    'auto_install': False,

    'images': [
    'static/description/icon.png'
    ],

}