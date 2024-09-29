import logging

from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class Diagnosis(models.Model):
    _name = 'hr.hospital.diagnosis'
    _inherit = ['mail.thread']
    _description = 'Diagnosis'

    name = fields.Char(compute='_compute_name',
                       store=True)
    visit_id = fields.Many2one('hr.hospital.visit',
                               ondelete='cascade')
    disease_id = fields.Many2one('hr.hospital.disease',
                                 required=True)
    description = fields.Text(tracking=True)
    approved = fields.Boolean(tracking=True)

    patient_name = fields.Char(compute='_compute_person_names',
                               store=True)
    doctor_name = fields.Char(compute='_compute_person_names',
                              store=True)

    @api.depends('patient_name', 'doctor_name')
    def _compute_name(self):
        """Обчислює значення для збереженого поля name"""
        for record in self:
            record.name = (f"{record.patient_name}" +
                           f" | {record.doctor_name}" +
                           f" | {record.disease_id.name}" +
                           f" | {record.description}")

    @api.depends('visit_id')
    def _compute_person_names(self):
        """Обчислює ім'я та прізвище пацієнта і лікаря"""
        for rec in self:
            if rec.visit_id:
                # Отримуємо дані пацієнта
                patient = rec.visit_id.patient_id
                rec.patient_name = (f"{patient.first_name} {patient.last_name}"
                                    if patient else "")

                # Отримуємо дані лікаря
                doctor = rec.visit_id.doctor_id
                rec.doctor_name = (f"{doctor.first_name} {doctor.last_name}"
                                   if doctor else "")
