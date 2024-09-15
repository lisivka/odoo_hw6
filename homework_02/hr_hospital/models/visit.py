import logging

from odoo import models, fields

_logger = logging.getLogger(__name__)


class Visit(models.Model):
    _name = 'hr_hospital.visit'
    _description = 'Patient Visit'

    patient_id = fields.Many2one('hr_hospital.patient', string='Patient', required=True)
    date = fields.Datetime(string='Visit Date', default=fields.Datetime.now, required=True)
    notes = fields.Text(string='Notes')
    doctor_id = fields.Many2one('hr_hospital.doctor', string='Doctor', related='patient_id.doctor_id')

