import logging

from odoo import models, fields


_logger = logging.getLogger(__name__)
from odoo import models, fields


class Visit(models.Model):
    _name = 'hr.hospital.visit'
    _description = 'Patient Visit'

    patient_id = fields.Many2one('hr.hospital.patient', string='Patient',
                                 required=True)
    doctor_id = fields.Many2one('hr.hospital.doctor', string='Doctor',
                                required=True)
    disease_id = fields.Many2one('hr.hospital.disease', string='Main Disease')
    disease_ids = fields.Many2many('hr.hospital.disease',
                                   string='Other Diseases')
    date = fields.Datetime(string='Visit Date', default=fields.Datetime.now,
                           required=True)
    notes = fields.Text(string='Notes')
    status = fields.Selection(
        selection= [
        ('draft', 'Draft'),
        ('done', 'Done'),
        ('canceled', 'Canceled'),
        ('expired', 'Expired'),
        ('sheduled', 'Scheduled'),
        ('processed', 'Processed'),
    ], string='Status', default='sheduled')
