# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class EmployeeDataChangeRequestChild(models.Model):
    """Child to add to an employee through a data change request.

    When the parent request is done, a private ``res.partner`` is
    created for the child and linked to the private address partner
    of the employee as a child.
    """

    _name = "employee_data_change_request_child"
    _description = "Employee Data Change Request - Child"

    request_id = fields.Many2one(
        string="# Request",
        comodel_name="employee_data_change_request",
        required=True,
        ondelete="cascade",
        help="Data change request that adds this child.",
    )
    name = fields.Char(
        string="Name",
        required=True,
        help="Full name of the child.",
    )
    birthdate_date = fields.Date(
        string="Birthdate",
        help="Birth date of the child.",
    )
    gender = fields.Selection(
        string="Gender",
        selection="_selection_gender",
        help="Gender of the child.",
    )

    @api.model
    def _selection_gender(self):
        """Return the gender options of the private partner.

        :return: selection list of ``res.partner.gender``
        """
        return self.env["res.partner"]._fields["gender"].selection

    def _prepare_child_values(self):
        """Build the values used to create the child partner.

        Same values as the Add Child wizard of the employee.

        :return: dict of ``res.partner`` create values
        """
        self.ensure_one()
        return {
            "name": self.name,
            "type": "private",
            "is_company": False,
            "birthdate_date": self.birthdate_date,
            "gender": self.gender,
        }

    def _get_relationship(self, employee):
        """Return the relationship of the employee towards the child.

        Follows the gender of the employee: father for male, mother
        for female, plain child otherwise.

        :param employee: the ``hr.employee`` receiving the child
        :return: ``father``, ``mother`` or False
        """
        self.ensure_one()
        return {"male": "father", "female": "mother"}.get(employee.gender, False)

    def _apply_to_employee(self, employee):
        """Create the child partner and link it to the employee.

        :param employee: the ``hr.employee`` receiving the child
        :return: the created child ``res.partner``
        """
        self.ensure_one()
        employee = employee.sudo()
        child = self.env["res.partner"].sudo().create(self._prepare_child_values())
        employee.address_home_id.link_child(child, self._get_relationship(employee))
        return child
