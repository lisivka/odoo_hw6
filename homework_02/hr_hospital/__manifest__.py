{
    'name': 'HR Hospital',
    'author': 'Lisivka Sergii',
    'category': 'Human Resources',
    'summary': 'Manage Hospital Operations',
    'description': """
        Module to manage hospital operations:
        - Doctors
        - Patients
        - Diseases
        - Visits
    """,
    'website': 'https://odoo.school/',
    'category': 'Customizations',
    'version': '17.0.0.0.2',
    'license': 'OPL-1',
    'depends': [
        'base',
    ],

    'external_dependencies': {
        'python': [],
    },

    'data': [
        'security/ir.model.access.csv',
        'views/doctor_views.xml',
        'views/patient_views.xml',
        'views/disease_views.xml',
        'views/visit_views.xml',
        'views/hr_hospital_menu.xml',  # Завантажується останнім
    ],

    'demo': [
         'demo/hr_hospital_demo.xml',
    ],

    'installable': True,
    'auto_install': False,

    'images': [
    'static/description/icon.png'
    ],

}