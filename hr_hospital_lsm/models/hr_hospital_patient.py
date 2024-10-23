import logging

from datetime import date
from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class Patient(models.Model):
    """
    Represents a patient in the hospital system.

    Inherits from the 'hr.hospital.person' model.
    Stores patient-specific information, including age, birth date,
    personal doctor, passport details, and contact person. It also
    tracks visits and diagnoses associated with the patient.
    """

    _inherit = 'hr.hospital.person'
    _name = 'hr.hospital.patient'
    _description = 'Patient'

    age = fields.Integer(compute='_compute_age', store=True)
    birth_date = fields.Date()
    personal_doctor_id = fields.Many2one('hr.hospital.doctor')
    passport_details = fields.Char()
    contact_person = fields.Char()
    visit_ids = fields.One2many('hr.hospital.visit', 'patient_id')
    diagnosis_ids = fields.One2many('hr.hospital.diagnosis', 'patient_id')

    # Додаємо поле, яке пов'язує особу з користувачем
    user_id = fields.Many2one('res.users',
                              help="The user linked to this person.")

    @api.depends('birth_date')
    def _compute_age(self):
        """ Computes the patient's age based on the birth date. """
        for record in self:
            record.age = 0
            if record.birth_date:
                today = date.today()
                birth_date = record.birth_date
                extra_year = ((today.month, today.day) < (
                    birth_date.month, birth_date.day))  # bool

                record.age = today.year - birth_date.year - extra_year
            if record.age < 0:
                record.age = 0

    def action_create_visit(self):
        """ Opens a window to create a new patient visit. """
        return {
            'type': 'ir.actions.act_window',
            'name': 'Create Visit',
            'res_model': 'hr.hospital.visit',
            'view_mode': 'form',
            'context': {
                'default_patient_id': self.id,
                'default_status': 'scheduled',
                'default_planned_date': fields.Datetime.now(),
            },
            'target': 'new',
        }

    def action_all_visits(self):
        """ Displays all visits associated with the current patient
        in a list view."""
        return {
            'type': 'ir.actions.act_window',
            'name': 'All visits',
            'res_model': 'hr.hospital.visit',
            'view_mode': 'tree',
            'domain': [('patient_id', '=', self.id)],
        }
