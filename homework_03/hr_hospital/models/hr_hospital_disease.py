import logging

from odoo import models, fields

_logger = logging.getLogger(__name__)


class Disease(models.Model):
    _name = 'hr.hospital.disease'
    _description = 'Disease'

    name = fields.Char(string='Disease Name', required=True)
    description = fields.Text(string='Description')
    parent_id = fields.Many2one('hr.hospital.disease', string='Parent Disease')
    child_ids = fields.One2many('hr.hospital.disease', 'parent_id', string='Sub-Diseases')
    sequence = fields.Integer(default=10)
