import logging
from datetime import datetime
from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class ReportDiagnosisWizard(models.TransientModel):
    _name = 'report.diagnosis.wizard'
    _description = 'Wizard for generating disease report'

    date_from = fields.Date(string='Date From', required=True,
                            default=lambda self: datetime.today().replace(
                                day=1).date())
    date_to = fields.Date(string='Date To', required=True,
                          default=fields.Date.today())
    doctor_ids = fields.Many2many('hr.hospital.doctor', string='Doctors',
                                  default=lambda self: self.env.context.get(
                                      'default_doctor_ids'))
    disease_ids = fields.Many2many('hr.hospital.disease', string='Diseases')

    @api.model
    def default_get(self, fields):
        res = super(ReportDiagnosisWizard, self).default_get(fields)
        # Якщо контекст містить дані про лікарів, встановлюємо їх як значення за замовчуванням
        if self.env.context.get('default_doctor_ids'):
            res['doctor_ids'] = [
                (6, 0, self.env.context.get('default_doctor_ids'))]
        return res

    def action_generate_report(self):
        """Generate the report based on selected dates."""
        domain = [('visit_id.planned_date', '>=', self.date_from),
                  ('visit_id.planned_date', '<=', self.date_to)]

        # Додаємо фільтрацію по лікарям, якщо вибрано
        if self.doctor_ids:
            domain.append(('visit_id.doctor_id', 'in', self.doctor_ids.ids))

        # Додаємо фільтрацію по хворобам, якщо вибрано
        if self.disease_ids:
            domain.append(('disease_id', 'in', self.disease_ids.ids))

        # Отримуємо діагнози відповідно до домену та сортуємо по хворобі
        diagnosis_records = self.env[
            'hr.hospital.diagnosis'].search(domain, order='disease_id asc')

        return {
            'type': 'ir.actions.act_window',
            'name': 'Grouped Diagnosis Report',
            'res_model': 'hr.hospital.diagnosis',
            'view_mode': 'tree',
            'domain': [('id', 'in', diagnosis_records.ids)],
            'context': {
                'group_by': 'disease_id',  # Групування по хворобі
            },
            'target': 'current',
        }
