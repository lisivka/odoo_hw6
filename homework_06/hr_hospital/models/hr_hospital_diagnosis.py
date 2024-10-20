import logging
from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class Diagnosis(models.Model):
    """
    Model representing a medical diagnosis.

    This model stores information about a medical diagnosis, including
    the associated doctor,patient, disease, and other related fields.
    It inherits from `mail.thread` to allow tracking of field changes
    in the diagnosis.
    """

    _name = 'hr.hospital.diagnosis'
    _inherit = ['mail.thread']
    _description = 'Diagnosis'

    name = fields.Char(compute='_compute_name',
                       store=True)
    is_approved = fields.Boolean(tracking=True)
    date = fields.Datetime(copy=False,
                           default=fields.Date.today())
    doctor_id = fields.Many2one('hr.hospital.doctor')
    disease_id = fields.Many2one('hr.hospital.disease',
                                 required=True)
    disease_type_id = fields.Many2one('hr.hospital.disease',
                                      compute='_compute_disease_type',
                                      store=True,
                                      string='Disease Type')
    description = fields.Text(tracking=True)

    patient_id = fields.Many2one('hr.hospital.patient',
                                 compute='_compute_patient_id',
                                 ondelete='cascade')

    visit_id = fields.Many2one('hr.hospital.visit',
                               ondelete='cascade')

    mentor_id = fields.Many2one('hr.hospital.doctor',
                                compute='_compute_doctor_info', store=True)
    can_approve = fields.Boolean(compute='_compute_can_approve')

    @api.depends('visit_id.patient_id')
    def _compute_patient_id(self):
        """
        Compute the patient associated with the diagnosis based on the visit.

        If there is a related visit with an associated patient,
        this method assigns the  patient to the `patient_id` field.
        Otherwise, it sets the field to False.
        """

        for rec in self:
            if rec.visit_id and rec.visit_id.patient_id:
                rec.patient_id = rec.visit_id.patient_id
            else:
                rec.patient_id = False

    @api.depends('visit_id')
    def _compute_doctor_info(self):
        """
        Compute the doctor and mentor associated with the diagnosis.

        If the diagnosis is linked to a visit,
        this method assigns the doctor from the  visit and,
        if applicable, assigns the mentor if the doctor is an intern.
        """

        for rec in self:
            if rec.visit_id:
                doctor = rec.visit_id.doctor_id
                rec.doctor_id = doctor
                rec.mentor_id = doctor.mentor_id if doctor.is_intern else False

    @api.depends('doctor_id')
    def _compute_can_approve(self):
        """
        Determine whether the diagnosis can be approved.

        This method checks if the assigned doctor is an intern.
        Only an intern can approve the diagnosis.
        """

        for rec in self:
            # Можна погодити лише якщо лікар є інтерном
            rec.can_approve = rec.doctor_id.is_intern

    @api.depends('disease_id')
    def _compute_disease_type(self):
        """
        Compute the disease type based on the selected disease.

        If the selected disease has a parent disease
        (i.e., it is a sub-disease), this method
        assigns the parent disease to the `disease_type_id` field.
        """
        for record in self:
            if record.disease_id:
                record.disease_type_id = record.disease_id.parent_id
            else:
                record.disease_type_id = False

    @api.depends('patient_id', 'doctor_id')
    def _compute_name(self):
        """Compute the name field of the diagnosis."""
        for record in self:
            record.name = (f"{record.patient_id.name}" +
                           f" | {record.doctor_id.name}" +
                           f" | {record.disease_id.name}")

    @api.model
    def create(self, vals):
        """ Override the create method to assign the doctor from the visit. """
        if 'visit_id' in vals and vals['visit_id']:
            visit = self.env['hr.hospital.visit'].browse(vals['visit_id'])
            if visit.doctor_id:
                vals['doctor_id'] = visit.doctor_id.id
        return super(Diagnosis, self).create(vals)

    @api.onchange('visit_id')
    def _onchange_visit_id(self):
        """ Update the doctor and patient when the visit is changed. """
        if self.visit_id:
            self.doctor_id = self.visit_id.doctor_id
            self.patient_id = self.visit_id.patient_id
