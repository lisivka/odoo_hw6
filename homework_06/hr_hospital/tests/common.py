from odoo.tests.common import TransactionCase


class TestHospitalCommon(TransactionCase):
    """ Common setup for all tests in the hospital module. """

    def setUp(self):
        super(TestHospitalCommon, self).setUp()

        # Створимо фіктивні дані для тестів
        self.patient = self.env['hr.hospital.patient'].create({
            'name': 'Test Patient',
        })

        self.doctor = self.env['hr.hospital.doctor'].create({
            'name': 'Test Doctor',
        })

        self.visit_model = self.env['hr.hospital.visit']
