# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class EmployeeDataChangeRequestAcademic(models.Model):
    """Academic history entry to add through a data change request.

    When the parent request is done, a ``partner.academic`` record is
    created for the private address partner of the employee. Existing
    academic history is never changed or deleted by a request.
    """

    _name = "employee_data_change_request_academic"
    _description = "Employee Data Change Request - Academic"

    request_id = fields.Many2one(
        string="# Request",
        comodel_name="employee_data_change_request",
        required=True,
        ondelete="cascade",
        help="Data change request that adds this academic history.",
    )
    name = fields.Char(
        string="Institution",
        required=True,
        help="Name of the school or university.",
    )
    education_level_id = fields.Many2one(
        string="Education Level",
        comodel_name="partner.formal_education_level",
        ondelete="restrict",
        help="Level of the education.",
    )
    field_of_study_id = fields.Many2one(
        string="Field of Study",
        comodel_name="partner.field_of_study",
        ondelete="restrict",
        help="Field of study.",
    )
    date_start = fields.Date(
        string="Date Start",
        required=True,
        help="Date the study started.",
    )
    date_end = fields.Date(
        string="Date End",
        help="Date the study ended.",
    )
    diploma = fields.Char(
        string="Diploma Number",
        help="Number of the diploma.",
    )
    gpa = fields.Float(
        string="Latest GPA",
        help="Latest grade point average.",
    )

    @api.constrains("date_start", "date_end")
    def _check_date_end(self):
        """Require the end date to be on or after the start date.

        :raises ValidationError: if ``date_end`` is before ``date_start``
        """
        for record in self:
            if record.date_end and record.date_end < record.date_start:
                error_message = """
Context: Employee data change request academic
Database ID: %s
Problem: Date End is before Date Start
Solution: Set Date End on or after Date Start
""" % (
                    record.id,
                )
                raise ValidationError(_(error_message))

    def _prepare_academic_values(self, partner):
        """Build the values used to create the academic record.

        :param partner: the private address ``res.partner``
        :return: dict of ``partner.academic`` create values
        """
        self.ensure_one()
        return {
            "partner_id": partner.id,
            "name": self.name,
            "education_level_id": self.education_level_id.id,
            "field_of_study_id": self.field_of_study_id.id,
            "date_start": self.date_start,
            "date_end": self.date_end,
            "diploma": self.diploma,
            "gpa": self.gpa,
        }

    def _apply_to_employee(self, employee):
        """Create the academic record of the employee partner.

        :param employee: the ``hr.employee`` receiving the history
        :return: the created ``partner.academic`` record
        """
        self.ensure_one()
        partner = employee.sudo().address_home_id
        return (
            self.env["partner.academic"]
            .sudo()
            .create(self._prepare_academic_values(partner))
        )
