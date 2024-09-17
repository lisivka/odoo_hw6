{
    'name': 'HR Hospital',
    'author': 'Lisivka Sergii',
    'category': 'Customizations',
    'summary': 'Manage Hospital Operations',
    'description': """
        Module to manage hospital operations:
        - Doctors
        - Patients
        - Diseases
        - Visits
    """,
    'website': 'https://odoo.school/',
    'version': '17.0.0.0.3',
    'license': 'OPL-1',
    'depends': [
        'base',
    ],

    'external_dependencies': {
        'python': [],
    },

    'data': [
        'security/ir.model.access.csv',
        'views/hr_hospital_doctor_views.xml',
        'views/res_partner_views.xml',
        'views/hr_hospital_disease_views.xml',
        'views/hr_hospital_visit_views.xml',
        'views/hr_hospital_menu.xml',  # Завантажується останнім
    ],

    'demo': [
        'demo/hr_hospital_demo.xml',
        # 'demo/hr_hospital_disease.csv',
        # 'demo/hr_hospital_doctor.csv',
        # 'demo/res_partner.csv',
        # 'demo/hr_hospital_visit.csv',
    ],

    'installable': True,
    'auto_install': False,

    'images': [
        'static/description/icon.png'
    ],
}
