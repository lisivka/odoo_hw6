import logging

from odoo import models, fields

_logger = logging.getLogger(__name__)


class Patient(models.Model):
    _inherit = 'hr.hospital.person'
    _name = 'hr.hospital.patient'
    _description = 'Patient'

    visit_ids = fields.One2many('hr.hospital.visit', 'patient_id',
                                string='Visits')
