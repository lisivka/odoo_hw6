import logging

from odoo import models, fields, api

_logger = logging.getLogger(__name__)

class Diagnosis(models.Model):
    _name = 'hr.hospital.diagnosis'
    _inherit = ['mail.thread']
    _description = 'Diagnosis'

    visit_id = fields.Many2one('hr.hospital.visit', string='Visit', required=True)
    disease_id = fields.Many2one('hr.hospital.disease', string='Disease', required=True)
    description = fields.Text(string='Description', tracking = True)
    approved = fields.Boolean(string='Approved', tracking = True)

    patient_name = fields.Char(string="Patient Name",
                               compute='_compute_person_names', store=True)
    doctor_name = fields.Char(string="Doctor Name",
                              compute='_compute_person_names', store=True)

    @api.depends('visit_id')
    def _compute_person_names(self):
        """Обчислює ім'я та прізвище пацієнта і лікаря"""
        for rec in self:
            if rec.visit_id:
                # Отримуємо дані пацієнта
                patient = rec.visit_id.patient_id
                rec.patient_name = f"{patient.first_name} {patient.last_name}" if patient else ""

                # Отримуємо дані лікаря
                doctor = rec.visit_id.doctor_id
                rec.doctor_name = f"{doctor.first_name} {doctor.last_name}" if doctor else ""