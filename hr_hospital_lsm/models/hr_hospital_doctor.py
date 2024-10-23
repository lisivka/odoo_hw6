import logging

from odoo import models, fields, api, exceptions, _

_logger = logging.getLogger(__name__)


class Doctor(models.Model):
    """
    Model representing a doctor.

    This model stores information about doctors,
    including whether they are interns,
    their mentor, and their specialty.
    It also includes functionality for linking
    doctors to their diagnoses and visits.
    """

    _inherit = 'hr.hospital.person'
    _name = 'hr.hospital.doctor'
    _description = 'Doctor'

    # Якщо не хочемо визначати компанію на звіті
    # company_id = fields.Many2one(
    #     comodel_name='res.company',
    #     required=True,
    #     readonly=True,
    #     default=lambda self: self.env.company,
    # )

    is_intern = fields.Boolean()
    intern_ids = fields.One2many('hr.hospital.doctor',
                                 'mentor_id', )
    diagnosis_ids = fields.One2many('hr.hospital.diagnosis',
                                    'doctor_id',
                                    )
    mentor_id = fields.Many2one('hr.hospital.doctor',
                                domain=[('is_intern', '=', False)], )
    mentor_specialty = fields.Char(compute='_compute_mentor_info')
    mentor_phone = fields.Char(compute='_compute_mentor_info')
    # Поле для зберігання many2one посилань на інтернів
    mentor_intern_ids = fields.One2many('hr.hospital.doctor',
                                        'mentor_id',
                                        string="Interns")
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
        """ Compute the mentor's specialty and phone number. """
        for doctor in self:
            if doctor.mentor_id:
                doctor.mentor_specialty = doctor.mentor_id.specialty
                doctor.mentor_phone = doctor.mentor_id.phone
            else:
                doctor.mentor_specialty = ''
                doctor.mentor_phone = ''

    @api.depends('intern_ids')
    def _compute_mentor_interns(self):
        """  Compute the list of interns for the mentor. """
        for doctor in self:
            # Отримуємо список інтернів
            doctor.mentor_intern_ids = doctor.intern_ids.mapped('user_id')

    @api.onchange('is_intern')
    def _onchange_is_intern(self):
        """ Clear the mentor field if the doctor is no longer an intern. """
        if not self.is_intern:
            self.mentor_id = False

    @api.constrains('mentor_id', 'is_intern')
    def _check_mentor(self):
        """ Validate the mentor field based on intern status."""

        for rec in self:
            # Перевіряємо, що інтерн не може бути ментором
            if rec.mentor_id and rec.mentor_id.is_intern:
                raise exceptions.ValidationError(
                    _("Intern cannot be a mentor."))

            # Забороняємо призначати ментора, якщо лікар не є інтерном
            if not rec.is_intern and rec.mentor_id:
                raise exceptions.ValidationError(
                    _("Person is not intern."))

    def action_open_report_wizard(self):
        """ Open the wizard for printing a diagnosis report. """
        return {
            'type': 'ir.actions.act_window',
            'name': 'Print Diagnosis Report',
            'res_model': 'report.diagnosis.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_doctor_ids': [self.id]},
        }

    def create_quick_visit(self):
        """ Create a new visit for the doctor. """
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
        """ Open the form for scheduling a visit with the doctor. """
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
