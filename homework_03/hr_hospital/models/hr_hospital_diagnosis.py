from odoo import models, fields, api

class Diagnosis(models.Model):
    _name = 'hr.hospital.diagnosis'
    _description = 'Diagnosis'

    visit_id = fields.Many2one('hr.hospital.visit', string='Visit', required=True)
    disease_id = fields.Many2one('hr.hospital.disease', string='Disease', required=True)
    description = fields.Text(string='Description')
    approved = fields.Boolean(string='Approved')
