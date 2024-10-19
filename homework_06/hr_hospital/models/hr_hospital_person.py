# hr_hospital/models/hr_hospital_person.py
import logging

from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class Person(models.AbstractModel):
    _name = 'hr.hospital.person'
    _description = 'Person'

    name = fields.Char(compute='_compute_name', store=True)
    first_name = fields.Char(required=True)
    last_name = fields.Char(required=True)
    phone = fields.Char()
    photo = fields.Binary()
    gender = fields.Selection(
        selection=[
            ('male', 'Male'),
            ('female', 'Female'),
            ('other', 'Other/Undefined'),
        ],
        default='other',
    )
    # Додаємо поле, яке пов'язує особу з користувачем
    user_id = fields.Many2one('res.users', help="The user linked to this person.")

    @api.depends('first_name', 'last_name')
    def _compute_name(self):
        """Обчислює значення для збереженого поля name"""
        for record in self:
            record.name = f"{record.first_name} {record.last_name}"
