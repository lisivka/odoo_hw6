import logging

from odoo import models, fields

_logger = logging.getLogger(__name__)


class Patient(models.Model):
    _inherit = 'res.partner'

    is_patient = fields.Boolean('Patient', default=False)
    gender = fields.Selection(
        selection=[
            ('male', 'Male'),
            ('female', 'Female'),
            ('other', 'Other'),
        ],
        )
    visit_ids = fields.One2many('hr_hospital.visit',
                                'patient_id', string='Visits')
