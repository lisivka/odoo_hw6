import logging

from odoo import models, fields

_logger = logging.getLogger(__name__)


class Patient(models.Model):
    _inherit = 'res.partner'

    is_patient = fields.Boolean(string='Is a Patient', default=True)
    # age = fields.Integer(string='Age')
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ], string='Gender')
    visit_ids = fields.One2many('hr_hospital.visit', 'patient_id', string='Visits')
    # doctor_id = fields.Many2one('hr_hospital.doctor', string='Doctor')
    # disease_id = fields.Many2one('hr_hospital.disease', string='Disease')
