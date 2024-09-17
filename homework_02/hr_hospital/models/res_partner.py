import logging

from odoo import models, fields


_logger = logging.getLogger(__name__)


class Patient(models.Model):
    _inherit = 'res.partner'

    is_patient = fields.Boolean(string='Is a Patient', default=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ], string='Gender')
    visit_ids = fields.One2many('hr_hospital.visit',
                                'patient_id', string='Visits')
