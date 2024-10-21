import logging

from odoo import models, fields

_logger = logging.getLogger(__name__)


class Disease(models.Model):
    """
    Model representing a disease.

    This model stores information about diseases, including their names, descriptions,
    and any parent-child relationships for sub-diseases.
    """

    _name = 'hr.hospital.disease'
    _description = 'Disease'
    _parent_name = 'parent_id'
    _parent_store = True
    _parent_order = 'sequence, name'
    _order = 'parent_left, name'

    name = fields.Char(required=True)
    description = fields.Text()
    parent_id = fields.Many2one('hr.hospital.disease',
                                ondelete='cascade',
                                index=True)
    child_ids = fields.One2many('hr.hospital.disease',
                                'parent_id',
                                string='Sub-Diseases')
    sequence = fields.Integer(default=10)
    parent_left = fields.Integer(index=True)
    parent_right = fields.Integer(index=True)
    parent_path = fields.Char(index=True, unaccent=False)
