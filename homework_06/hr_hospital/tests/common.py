from odoo.tests.common import TransactionCase


class TestHospitalCommon(TransactionCase):
    """ Common setup for all tests in the hospital module. """

    def setUp(self):
        super(TestHospitalCommon, self).setUp()

        self.patient = self.env['hr.hospital.patient'].create({
            'first_name': 'Test',
            'last_name': 'Patient',
            'birth_date': '1990-01-01'
        })

        self.doctor = self.env['hr.hospital.doctor'].create({
            'first_name': 'Test',
            'last_name': 'Doctor',
            'specialty': 'cardiologist',
        })

        self.disease = self.env['hr.hospital.disease'].create({
            'name': 'Test Disease',
        })

        self.visit_model = self.env['hr.hospital.visit']
        self.diagnosis_model = self.env['hr.hospital.diagnosis']
