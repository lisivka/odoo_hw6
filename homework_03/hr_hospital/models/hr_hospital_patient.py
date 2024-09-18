import logging

from datetime import date
from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class Patient(models.Model):
    _inherit = 'hr.hospital.person'
    _name = 'hr.hospital.patient'
    _description = 'Patient'

    age = fields.Integer(string='Age', compute='_compute_age', store=True)
    birth_date = fields.Date(string='Birth Date')
    personal_doctor_id = fields.Many2one('hr.hospital.doctor',
                                         string='Personal Doctor')
    passport_details = fields.Char(string='Passport Details')
    contact_person = fields.Char(string='Contact Person')
    visit_ids = fields.One2many('hr.hospital.visit', 'patient_id',
                                string='Visits')

    @api.depends('birth_date')
    def _compute_age(self):
        for record in self:
            if record.birth_date:
                today = date.today()
                record.age = today.year - record.birth_date.year - (
                            (today.month, today.day) < (
                    record.birth_date.month, record.birth_date.day))
            else:
                record.age = 0
