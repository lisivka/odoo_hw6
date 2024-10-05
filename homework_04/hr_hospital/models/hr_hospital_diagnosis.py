import logging

from odoo import models, fields, api
from odoo.tools.populate import compute

_logger = logging.getLogger(__name__)


class Diagnosis(models.Model):
    _name = 'hr.hospital.diagnosis'
    _inherit = ['mail.thread']
    _description = 'Diagnosis'

    name = fields.Char(compute='_compute_name',
                       store=True)
    is_approved = fields.Boolean(tracking=True)
    doctor_id = fields.Many2one('hr.hospital.doctor')
    # doctor_name = fields.Char(compute='_compute_person_names',
    #                           store=True)
    disease_id = fields.Many2one('hr.hospital.disease',
                                 required=True)
    description = fields.Text(tracking=True)
    # patient_name = fields.Char(compute='_compute_person_names',
    #                            store=True)

    patient_id = fields.Many2one('hr.hospital.patient',
                                 compute = '_compute_patient_id',
                                 ondelete='cascade')
    visit_id = fields.Many2one('hr.hospital.visit',
                               ondelete='cascade')

    mentor_id = fields.Many2one('hr.hospital.doctor', compute='_compute_doctor_info', store=True)
    can_approve = fields.Boolean(compute='_compute_can_approve')

    @api.depends('visit_id.patient_id')
    def _compute_patient_id(self):
        for rec in self:
            if rec.visit_id and rec.visit_id.patient_id:
                rec.patient_id = rec.visit_id.patient_id
            else:
                rec.patient_id = False

    @api.depends('visit_id')
    def _compute_doctor_info(self):
        for rec in self:
            if rec.visit_id:
                doctor = rec.visit_id.doctor_id
                rec.doctor_id = doctor
                rec.mentor_id = doctor.mentor_id if doctor.is_intern else False

    @api.depends('doctor_id')
    def _compute_can_approve(self):
        for rec in self:
            # Можна погодити лише якщо лікар є інтерном
            rec.can_approve = rec.doctor_id.is_intern

    @api.depends('patient_id', 'doctor_id')
    def _compute_name(self):
        """Обчислює значення для збереженого поля name"""
        for record in self:
            record.name = (f"{record.patient_id.name}" +
                           f" | {record.doctor_id.name}" +
                           f" | {record.disease_id.name}" +
                           f" | ")



    @api.model
    def create(self, vals):
        if 'visit_id' in vals and vals['visit_id']:
            visit = self.env['hr.hospital.visit'].browse(vals['visit_id'])
            if visit.doctor_id:
                vals['doctor_id'] = visit.doctor_id.id
        return super(Diagnosis, self).create(vals)

    @api.onchange('visit_id')
    def _onchange_visit_id(self):
        if self.visit_id:
            self.doctor_id = self.visit_id.doctor_id
            self.patient_id = self.visit_id.patient_id


