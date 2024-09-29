import logging
from datetime import datetime
from odoo import models, fields, api


_logger = logging.getLogger(__name__)

class ReportDiagnosisWizard(models.TransientModel):
    _name = 'report.diagnosis.wizard'
    _description = 'Wizard for generating disease report'

    date_from = fields.Date(string='Date From', required=True,
                            default=lambda self: datetime.today().replace(day=1).date())
    date_to = fields.Date(string='Date To', required=True, default=fields.Date.today() )

    def action_generate_report(self):
        """Generate the report based on selected dates."""
        domain = [
            ('visit_id.planned_date', '>=', self.date_from),
            ('visit_id.planned_date', '<=', self.date_to),
        ]
        diagnosis_records = self.env['hr.hospital.diagnosis'].search(domain)
        # You can return a report view or a list view based on the records found
        return {
            'type': 'ir.actions.act_window',
            'name': 'Diagnosis Report',
            'res_model': 'hr.hospital.diagnosis',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', diagnosis_records.ids)],
            'target': 'current',
        }
