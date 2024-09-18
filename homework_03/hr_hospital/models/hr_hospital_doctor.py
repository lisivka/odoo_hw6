import logging

from odoo import models, fields

_logger = logging.getLogger(__name__)


class Doctor(models.Model):
    _inherit = 'hr.hospital.person'
    _name = 'hr.hospital.doctor'
    _description = 'Doctor'

    specialty = fields.Char(string='Specialty')
    visit_ids = fields.One2many('hr.hospital.visit', 'doctor_id',
                                string='Visits')
