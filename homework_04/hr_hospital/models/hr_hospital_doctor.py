import logging

from odoo import models, fields, api, exceptions, _

_logger = logging.getLogger(__name__)


class Doctor(models.Model):
    _inherit = 'hr.hospital.person'
    _name = 'hr.hospital.doctor'
    _description = 'Doctor'

    is_intern = fields.Boolean(string="Intern")
    intern_ids = fields.One2many('hr.hospital.doctor',
                                 'mentor_id', )
    diagnosis_ids = fields.One2many('hr.hospital.diagnosis',
                                    'doctor_id',
                                    )
    mentor_id = fields.Many2one('hr.hospital.doctor', )
    mentor_specialty = fields.Char(string="Mentor Specialty",
                                   compute='_compute_mentor_info')
    mentor_phone = fields.Char(string="Mentor Phone",
                               compute='_compute_mentor_info')
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

    visit_ids = fields.One2many('hr.hospital.visit',
                                'doctor_id',
                                )

    @api.depends('mentor_id')
    def _compute_mentor_info(self):
        for doctor in self:
            if doctor.mentor_id:
                doctor.mentor_specialty = doctor.mentor_id.specialty
                doctor.mentor_phone = doctor.mentor_id.phone
            else:
                doctor.mentor_specialty = ''
                doctor.mentor_phone = ''

    @api.onchange('is_intern')
    def _onchange_is_intern(self):
        """Обнуляємо поле 'mentor_id', якщо лікар більше не інтерн"""
        if not self.is_intern:
            self.mentor_id = False

    @api.constrains('mentor_id', 'is_intern')
    def _check_mentor(self):
        """Забороняємо вибирати інтерна як ментора
        та забороняємо призначати ментора, якщо лікар не інтерн."""
        for rec in self:
            # Перевіряємо, що інтерн не може бути ментором
            if rec.mentor_id and rec.mentor_id.is_intern:
                raise exceptions.ValidationError(
                    _("Інтерн не може бути лікарем-ментором."))

            # Забороняємо призначати ментора, якщо лікар не є інтерном
            if not rec.is_intern and rec.mentor_id:
                raise exceptions.ValidationError(
                    _("Не вибирайте ментора для лікаря, який не є інтерном."))

    # @api.model
    # def fields_view_get(self, view_id=None, view_type='form', toolbar=False,
    #                     submenu=False):
    #     """Налаштовуємо форму, щоб поле 'mentor_id'
    #     відображалося лише якщо лікар інтерн - устаріло (("""
    #     res = super(Doctor, self).fields_view_get(view_id=view_id,
    #                                               view_type=view_type,
    #                                               toolbar=toolbar,
    #                                               submenu=submenu)
    #     if view_type == 'form':
    #         doc = res['arch']
    #         if 'is_intern' in doc:
    #             doc = doc.replace(
    #                 '<field name="mentor_id"/>',
    #                 '''<field name="mentor_id" attrs="{'invisible':
    #                 [('is_intern', '=', False)]}"/>'''
    #             )
    #
    #     return res

    def action_open_report_wizard(self):
        print(f"{self.env.context.get('active_ids')=}")
        print(f"{self.env.context.get('default_doctor_ids')=}")
        print(f"{self.id=}")
        return {
            'type': 'ir.actions.act_window',
            'name': 'Print Diagnosis Report',
            'res_model': 'report.diagnosis.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_doctor_ids': [self.id]},
        }

    def create_quick_visit(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Create Visit',
            'res_model': 'hr.hospital.visit',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_doctor_id': self.id, },
        }

    # Відкриття форми запису до лікаря
    def open_visit_form(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Запис до лікаря',
            'res_model': 'hr.hospital.visit',
            'view_mode': 'form',
            'context': {
                'default_doctor_id': self.id,
            },
            'target': 'new',
        }
