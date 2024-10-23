import logging
from datetime import timedelta
from odoo import fields
from odoo.exceptions import ValidationError, UserError
from .common import TestHospitalCommon

_logger = logging.getLogger(__name__)


class TestVisitConstraints(TestHospitalCommon):
    """ Tests for visit constraints in the hospital module. """

    def test_01_no_change_to_past_visit(self):
        """
        Test that a user cannot change doctor/date
        of a visit marked as 'done'.
        """
        visit = self.visit_model.create({
            'patient_id': self.patient.id,
            'doctor_id': self.doctor.id,
            'planned_date': fields.Datetime.now(),
            'status': 'done',
        })

        # Check that we cannot change the doctor after the visit
        with self.assertRaises(ValidationError):
            visit.write({'doctor_id': self.env['hr.hospital.doctor'].create(
                {'first_name': 'New', 'last_name': 'Doctor'}).id})

    def test_02_no_delete_visit_with_diagnosis(self):
        """
        Test that a visit with an associated diagnosis cannot be deleted.
        """

        # Create a visit
        visit = self.visit_model.create({
            'patient_id': self.patient.id,
            'doctor_id': self.doctor.id,
            'planned_date': fields.Datetime.now(),
            'status': 'scheduled',
        })

        # Create a diagnosis for the visit
        _ = self.diagnosis_model.create({
            'visit_id': visit.id,
            'disease_id': self.disease.id,
        })

        # Try to delete the visit that has a diagnosis
        with self.assertRaises(UserError):
            visit.unlink()

    def test_03_no_duplicate_visit_same_day(self):
        """ Test that a patient cannot have multiple visits
        with the same doctor on the same day. """
        today = fields.Datetime.now()

        # Create a visit
        _ = self.visit_model.create({
            'patient_id': self.patient.id,
            'doctor_id': self.doctor.id,
            'planned_date': today,
        })

        # Try to create another visit
        # with the same patient and doctor on the same day
        with self.assertRaises(ValidationError):
            self.visit_model.create({
                'patient_id': self.patient.id,
                'doctor_id': self.doctor.id,
                'planned_date': today + timedelta(hours=1),
            })
