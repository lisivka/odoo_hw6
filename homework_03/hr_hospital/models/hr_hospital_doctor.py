import logging

from odoo import models, fields, api, exceptions

_logger = logging.getLogger(__name__)


class Doctor(models.Model):
    _inherit = 'hr.hospital.person'
    _name = 'hr.hospital.doctor'
    _description = 'Doctor'

    specialty = fields.Selection(
        selection=[
            ("cardiologist", "Cardiologist"),
            ("neurologist", "Neurologist"),
            ("dermatologist", "Dermatologist"),
            ("oncologist", "Oncologist"),
            ("pediatrician", "Pediatrician"),
            ("radiologist", "Radiologist"),
            ("ophthalmologist", "Ophthalmologist"),
            ("psychiatrist", "Psychiatrist"),
            ("endocrinologist", "Endocrinologist"),
            ("surgeon", "Surgeon"),
            ('other', "other")
        ], default='other')

    visit_ids = fields.One2many('hr.hospital.visit', 'doctor_id',
                                string='Visits')

    is_intern = fields.Boolean(string="Intern")
    mentor_id = fields.Many2one('hr.hospital.doctor', string="Mentor")

    @api.onchange('is_intern')
    def _onchange_is_intern(self):
        """Обнуляємо поле 'mentor_id', якщо лікар більше не інтерн"""
        if not self.is_intern:
            self.mentor_id = False

    @api.constrains('mentor_id')
    def _check_mentor(self):
        """Забороняємо вибирати інтерна як ментора"""
        for rec in self:
            if rec.mentor_id and rec.mentor_id.is_intern:
                raise exceptions.ValidationError(
                    "Інтерн не може бути лікарем-ментором.")

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False,
                        submenu=False):
        """Налаштовуємо форму, щоб поле 'mentor_id' відображалося лише якщо лікар інтерн"""
        res = super(Doctor, self).fields_view_get(view_id=view_id,
                                                  view_type=view_type,
                                                  toolbar=toolbar,
                                                  submenu=submenu)
        if view_type == 'form':
            doc = res['arch']
            if 'is_intern' in doc:
                doc = doc.replace(
                    '<field name="mentor_id"/>',
                    '''<field name="mentor_id" attrs="{'invisible': [('is_intern', '=', False)]}"/>'''
                )
        return res
