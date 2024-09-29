import logging

from odoo import models, fields

_logger = logging.getLogger(__name__)


class Disease(models.Model):
    _name = 'hr.hospital.disease'
    _description = 'Disease'
    _parent_name = 'parent_id'
    _parent_store = True
    _child_order = 'sequence, name'

    name = fields.Char(required=True)
    description = fields.Text()
    parent_id = fields.Many2one('hr.hospital.disease',
                                ondelete='cascade',
                                index=True)
    child_ids = fields.One2many('hr.hospital.disease',
                                'parent_id',
                                string='Sub-Diseases')
    sequence = fields.Integer(default=10)
    parent_path = fields.Char(index=True)
