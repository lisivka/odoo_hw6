from datetime import datetime, timedelta
from odoo import fields
from odoo.tests.common import Form
from odoo.exceptions import ValidationError, UserError
from .common import TestHospitalCommon


class TestVisitConstraints(TestHospitalCommon):
    """ Tests for visit constraints in the hospital module. """

    def test_01_no_change_to_past_visit(self):
        """ Test that a user cannot change doctor/date of a visit marked as 'done'. """
        visit = self.visit_model.create({
            'patient_id': self.patient.id,
            'doctor_id': self.doctor.id,
            'planned_date': fields.Datetime.now(),
            'status': 'done',
        })

        # Перевіримо, чи не можна змінити лікаря після візиту
        with self.assertRaises(ValidationError):
            visit.write({'doctor_id': self.env['hr.hospital.doctor'].create({'name': 'New Doctor'}).id})

    def test_02_no_delete_visit_with_diagnosis(self):
        """ Test that a visit with an associated diagnosis cannot be deleted. """
        # Створюємо візит
        visit = self.visit_model.create({
            'patient_id': self.patient.id,
            'doctor_id': self.doctor.id,
            'planned_date': fields.Datetime.now(),
            'status': 'scheduled',
        })

        # Створюємо діагноз для візиту
        diagnosis = self.env['hr.hospital.diagnosis'].create({
            'visit_id': visit.id,
            'disease_id': self.env['hr.hospital.disease'].create({'name': 'Test Disease'}).id,
        })

        # Спробуємо видалити візит, що має діагноз
        with self.assertRaises(UserError):
            visit.unlink()

    def test_03_no_duplicate_visit_same_day(self):
        """ Test that a patient cannot have multiple visits with the same doctor on the same day. """
        today = fields.Datetime.now()

        # Створимо перший візит
        visit_1 = self.visit_model.create({
            'patient_id': self.patient.id,
            'doctor_id': self.doctor.id,
            'planned_date': today,
        })

        # Спробуємо створити другий візит для того ж пацієнта і лікаря на той самий день
        with self.assertRaises(ValidationError):
            self.visit_model.create({
                'patient_id': self.patient.id,
                'doctor_id': self.doctor.id,
                'planned_date': today + timedelta(hours=1),
            })
