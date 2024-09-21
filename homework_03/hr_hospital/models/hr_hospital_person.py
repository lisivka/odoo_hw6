# hr_hospital/models/hr_hospital_person.py
import logging

from odoo import models, fields, api

_logger = logging.getLogger(__name__)

class Person(models.AbstractModel):
    _name = 'hr.hospital.person'
    _description = 'Person'

    name = fields.Char(string='Name', compute='_compute_name', store=True)
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

    # display_name = fields.Char(string='Display Name', compute='_compute_display_name')

    @api.depends('first_name', 'last_name')
    def _compute_name(self):
        """Обчислює значення для збереженого поля name"""
        for record in self:
            record.name = f"{record.first_name} {record.last_name}"

    # @api.depends('first_name', 'last_name')
    # def _compute_display_name(self):
    #     """Обчислює значення для незбереженого поля display_name"""
    #     for record in self:
    #         record.display_name = f"{record.first_name} {record.last_name}"
