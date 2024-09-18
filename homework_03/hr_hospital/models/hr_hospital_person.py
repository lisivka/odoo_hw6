# hr_hospital/models/hr_hospital_person.py
from odoo import models, fields


class Person(models.AbstractModel):
    _name = 'hr.hospital.person'
    _description = 'Person'

    first_name = fields.Char(string='First Name', required=True)
    last_name = fields.Char(string='Last Name', required=True)
    phone = fields.Char(string='Phone')
    photo = fields.Binary(string='Photo')
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ], string='Gender')
