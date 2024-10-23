# models/mass_update_doctor_wizard.py
import logging
from odoo import models, fields

_logger = logging.getLogger(__name__)


class MassUpdateDoctorWizard(models.TransientModel):
    _name = 'mass.update.doctor.wizard'
    _description = 'Wizard for Mass Update of Personal Doctor'

    doctor_id = fields.Many2one(
        'hr.hospital.doctor',
        string='New Personal Doctor',
        required=True)

    def action_update_doctor(self):
        """Метод для масового оновлення лікаря"""
        active_ids = self.env.context.get('active_ids')
        if active_ids:
            patients = self.env['hr.hospital.patient'].browse(active_ids)
            for patient in patients:
                patient.personal_doctor_id = self.doctor_id
        return {'type': 'ir.actions.act_window_close'}
