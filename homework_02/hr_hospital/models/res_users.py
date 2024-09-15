import logging

from odoo import models, fields

_logger = logging.getLogger(__name__)


class Doctor(models.Model):
    _inherit = 'res.users'

    is_doctor = fields.Boolean(string='Is a Doctor', default=True)
    specialty = fields.Char(string='Specialty')
    # patient_ids = fields.One2many('res.partner', 'doctor_id', string='Patients')
