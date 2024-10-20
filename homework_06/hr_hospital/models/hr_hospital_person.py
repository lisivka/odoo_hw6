import logging

from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class Person(models.AbstractModel):
    """
    Abstract base model for persons in the hospital system.

    Represents common personal information for different types
    of individuals in the hospital system (e.g., patients, doctors).
    Stores the first and last name, phone, gender, and profile photo.
    """
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
    user_id = fields.Many2one('res.users',
                              help="The user linked to this person.")

    @api.depends('first_name', 'last_name')
    def _compute_name(self):
        """
        Computes the full name of the person by concatenating the first
        and last name.
        """
        for record in self:
            record.name = f"{record.first_name} {record.last_name}"
