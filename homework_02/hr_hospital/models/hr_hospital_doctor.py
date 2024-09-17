import logging

from odoo import models, fields

_logger = logging.getLogger(__name__)


class Doctor(models.Model):
    _name = 'hr_hospital.doctor'
    _description = 'Doctor'

    name = fields.Char(string='Name and Surname', required=True)
    specialty = fields.Char(string='Specialty ')
    visit_ids = fields.One2many('hr_hospital.visit', 'doctor_id',
                                string='Visits')
