import logging

from odoo import models, fields, api, exceptions
from datetime import datetime, timedelta

_logger = logging.getLogger(__name__)


class Visit(models.Model):
    _name = 'hr.hospital.visit'
    _description = 'Patient Visit'

    name = fields.Char(string='Name', compute='_compute_name', store=True)
    patient_id = fields.Many2one('hr.hospital.patient', string='Patient',
                                 required=True)
    doctor_id = fields.Many2one('hr.hospital.doctor', string='Doctor',
                                required=True)
    planned_date = fields.Datetime(string='Planned Date', copy=False)
    actual_date = fields.Datetime(string='Actual Date', copy=False)
    diagnosis_id = fields.Many2one('hr.hospital.diagnosis', copy=False)
    notes = fields.Text(string='Notes', copy=False)
    status = fields.Selection(
        selection=[
            ('draft', 'Draft'),
            ('scheduled', 'Scheduled'),
            ('expired', 'Expired'),  # Змінив порядок
            ('canceled', 'Canceled'),
            ('processed', 'Processed'),
            ('done', 'Done'),
        ],
        string='Status',
        default='scheduled',  # Виправлено помилку
        copy=False
    )
    @api.depends('patient_id', 'doctor_id', 'planned_date')
    def _compute_name(self):
        """Обчислює значення для збереженого поля name"""
        for record in self:
            record.name = f"{record.planned_date} {record.patient_id.name} | {record.doctor_id.name}"

    @api.constrains('planned_date', 'doctor_id', 'patient_id')
    def _check_duplicate_visit(self):
        for record in self:
            if record.planned_date:
                # Перевірка, чи вже існує візит для цього лікаря та пацієнта в той самий день
                visit_count = self.env['hr.hospital.visit'].search_count([
                    ('doctor_id', '=', record.doctor_id.id),
                    ('patient_id', '=', record.patient_id.id),
                    ('planned_date', '>=', record.planned_date.date()),
                    ('planned_date', '<',
                     (record.planned_date + timedelta(days=1)).date()),
                    ('id', '!=', record.id)  # виключити поточний візит
                ])
                if visit_count > 0:
                    raise exceptions.ValidationError(
                        'Пацієнт уже записаний до цього лікаря на той самий день.')

    @api.model
    def create(self, vals):
        # Автоматично встановлюємо дату фактичного візиту, якщо статус "done"
        if vals.get('status') == 'done' and not vals.get('actual_date'):
            vals['actual_date'] = fields.Datetime.now()
        return super(Visit, self).create(vals)

    def write(self, vals):
        for record in self:
            # Отримуємо поточний статус з бази
            current_status = record.read(['status'])[0]['status']

            # Якщо запис вже має статус 'done', перевіряємо, чи намагаємося змінити дату або лікаря
            if current_status == 'done':
                if 'doctor_id' in vals or 'planned_date' in vals or 'actual_date' in vals:
                    raise exceptions.ValidationError(
                        "Неможливо змінити дату, час або лікаря для завершеного візиту.")

        # Якщо статус змінюється на 'done', встановлюємо фактичну дату візиту
        if vals.get('status') == 'done' and not vals.get('actual_date'):
            vals['actual_date'] = fields.Datetime.now()

        return super(Visit, self).write(vals)

    @api.onchange('status')
    def _onchange_status(self):
        if self.status == 'done' and not self.actual_date:
            self.actual_date = fields.Datetime.now()

    def unlink(self):
        for record in self:
            if record.diagnosis_id:
                raise exceptions.UserError(
                    "Неможливо видалити візит із діагнозами.")
        return super(Visit, self).unlink()
