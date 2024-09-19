# hr_hospital/models/hr_hospital_person.py
from odoo import models, fields, api


class Person(models.AbstractModel):
    _name = 'hr.hospital.person'
    _description = 'Person'

    first_name = fields.Char(string='First Name', required=True)
    last_name = fields.Char(string='Last Name', required=True)
    phone = fields.Char(string='Phone')
    photo = fields.Binary(string='Photo')
    gender = fields.Selection(
        selection=[
            ('male', 'Male'),
            ('female', 'Female'),
            ('other', 'Other/Undefined'),
        ],
        default='other',
    )

    @api.depends('first_name', 'last_name')
    def _compute_display_name(self):
        for record in self:
            record.display_name = f"{record.first_name} {record.last_name} (id={record.id})"
