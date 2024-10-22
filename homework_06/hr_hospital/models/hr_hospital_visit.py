import logging
from datetime import timedelta
from odoo import models, fields, api, exceptions, _

_logger = logging.getLogger(__name__)


class Visit(models.Model):
    """
    Represents a patient visit to the hospital.

    Each visit is linked to a patient and a doctor and can include
    details such as planned and actual dates, diagnosis, notes,
    and visit status (e.g., scheduled, done, canceled).
    """
    _name = 'hr.hospital.visit'
    _inherit = ['mail.thread']  # Додаємо можливість відстежувати зміни
    _description = 'Patient Visit'

    active = fields.Boolean(default=True)
    name = fields.Char(compute='_compute_name',
                       store=True)
    patient_id = fields.Many2one('hr.hospital.patient',
                                 string='Patient',
                                 required=True,
                                 tracking=True)
    doctor_id = fields.Many2one('hr.hospital.doctor', string='Doctor',
                                required=True,
                                tracking=True)
    planned_date = fields.Datetime(copy=False,
                                   tracking=True)
    actual_date = fields.Datetime(copy=False,
                                  tracking=True)
    diagnosis_id = fields.One2many('hr.hospital.diagnosis',
                                   'visit_id',
                                   copy=False,
                                   tracking=True)
    notes = fields.Text(copy=False,
                        tracking=True)
    status = fields.Selection(
        selection=[
            ('canceled', 'Canceled'),
            ('scheduled', 'Scheduled'),
            ('processed', 'Processed'),
            ('done', 'Done'),
        ],
        default='scheduled',
        copy=False,
        tracking=True  # Додаємо відстеження змін статусу
    )

    @api.depends('patient_id', 'doctor_id', 'planned_date')
    def _compute_name(self):
        """
            Computes the visit's display name based on the planned date,
            patient's name, and doctor's name.
            """
        for record in self:
            record.name = (f"{record.planned_date}" +
                           f" {record.patient_id.name}" +
                           f" | {record.doctor_id.name}")

    @api.constrains('planned_date', 'doctor_id', 'patient_id')
    def _check_duplicate_visit(self):
        """
           Ensures that the same patient cannot have multiple visits scheduled
           with the same doctor on the same day.

           Raises a ValidationError if a duplicate visit is detected.
           """
        for record in self:
            if record.planned_date:
                # Перевірка, чи вже існує візит для цього лікаря
                # та пацієнта в той самий день
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
                        _('Duplicate visit detected.'))

    @api.model
    def create(self, vals_list):
        """
        Overrides the default create method.

        Automatically sets the actual visit date if the status is set
        to 'done' and the actual date is not provided.
        """

        if isinstance(vals_list, dict):
            vals_list = [vals_list]

        for vals in vals_list:
            if vals.get('status') == 'done' and not vals.get('actual_date'):
                vals['actual_date'] = fields.Datetime.now()

        return super(Visit, self).create(vals_list)

    def write(self, vals):
        """
        Overrides the default write method.

        Ensures that if a visit is marked as 'done', fields such as
        doctor and dates cannot be modified.
        Automatically sets the actual visit date if the status
        is changed to 'done'.
        """
        for record in self:
            # Отримуємо поточний статус з бази
            current_status = record.read(['status'])[0]['status']

            # Якщо запис вже має статус 'done',
            # перевіряємо, чи намагаємося змінити дату або лікаря
            if current_status == 'done':
                if ('doctor_id' in vals) or ('planned_date' in vals) or (
                        'actual_date' in vals):
                    raise exceptions.ValidationError(_('Visit is done.'))

        # Якщо статус змінюється на 'done', встановлюємо фактичну дату візиту
        if vals.get('status') == 'done' and not vals.get('actual_date'):
            vals['actual_date'] = fields.Datetime.now()

        return super(Visit, self).write(vals)

    @api.onchange('status')
    def _onchange_status(self):
        """
        Automatically sets the actual visit date when the status is
        changed to 'done' and no actual date is provided.
        """
        if self.status == 'done' and not self.actual_date:
            self.actual_date = fields.Datetime.now()

    def unlink(self):
        """
        Prevents deleting visits that have associated diagnoses.

        Raises a UserError if the visit contains any diagnoses.
        """
        for record in self:
            if record.diagnosis_id:
                raise exceptions.UserError(
                    _('Cannot delete visit with associated diagnoses'))

        return super(Visit, self).unlink()
