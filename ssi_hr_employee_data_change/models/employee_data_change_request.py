# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import AccessError, UserError, ValidationError

from odoo.addons.ssi_decorator import ssi_decorator

SELF_SERVICE_GROUP = "ssi_hr_employee_data_change.group_employee_self_service_api"

# Employee fields that can be changed through an approved request.
# Each has an ``old_<name>`` snapshot and a ``new_<name>`` target field.
CHANGE_FIELDS = [
    "identification_id",
    "place_of_birth",
    "birthday",
    "gender",
    "marital",
    "spouse_complete_name",
    "spouse_birthdate",
    "religion_id",
    "certificate",
    "image_1920",
]

# Employee fields returned by ``self_service_read`` for viewing only.
VIEW_ONLY_FIELDS = [
    "employment_status_id",
    "date_join",
    "date_permanent",
    "job_grade_id",
]

# Keys of ``self_service_write_contact`` written to the private partner.
CONTACT_PARTNER_KEYS = {
    "street": "street",
    "street2": "street2",
    "city": "city",
    "state_id": "state_id",
    "zip": "zip",
    "country_id": "country_id",
    "phone": "phone",
    "mobile": "mobile",
    "private_email": "email",
}

# Keys of ``self_service_write_contact`` written to the employee.
CONTACT_EMPLOYEE_KEYS = ["emergency_contact", "emergency_phone"]

# Line keys accepted by ``self_service_create_request``.
CHILD_LINE_KEYS = ["name", "birthdate_date", "gender"]
ACADEMIC_LINE_KEYS = [
    "name",
    "education_level_id",
    "field_of_study_id",
    "date_start",
    "date_end",
    "diploma",
    "gpa",
]


class EmployeeDataChangeRequest(models.Model):
    """Request to change the personal data of an employee.

    A transactional document with multiple approval. Each personal
    data field has an ``old_*`` snapshot and a ``new_*`` value (empty
    means unchanged). When the last approval is granted the document
    is done and every filled ``new_*`` value, child line, and academic
    line is written to the employee and the private partner of the
    employee.

    The model also exposes public ``@api.model`` methods that an
    external self-service application calls through a service
    account. They run as the employee, never as the service account.
    """

    _name = "employee_data_change_request"
    _description = "Employee Data Change Request"
    _inherit = [
        "mixin.transaction_confirm",
        "mixin.transaction_done",
        "mixin.transaction_cancel",
        "mixin.employee_document",
    ]

    # Multiple Approval Attribute
    _approval_from_state = "draft"
    _approval_to_state = "done"
    _approval_state = "confirm"
    _after_approved_method = "action_done"

    # Attributes related to add element on view automatically
    _automatically_insert_view_element = True

    # Attributes related to add element on form view automatically
    _automatically_insert_multiple_approval_page = True
    _statusbar_visible_label = "draft,confirm,done"
    _policy_field_order = [
        "confirm_ok",
        "approve_ok",
        "reject_ok",
        "restart_approval_ok",
        "cancel_ok",
        "restart_ok",
        "done_ok",
        "manual_number_ok",
    ]
    _header_button_order = [
        "action_confirm",
        "action_approve_approval",
        "action_reject_approval",
        "action_done",
        "%(ssi_transaction_cancel_mixin.base_select_cancel_reason_action)d",
        "action_restart",
    ]

    # Attributes related to add element on search view automatically
    _state_filter_order = [
        "dom_draft",
        "dom_confirm",
        "dom_reject",
        "dom_done",
        "dom_cancel",
    ]

    _order = "id desc"

    # Sequence attribute
    _create_sequence_state = "done"

    @api.model
    def _selection_gender(self):
        """Return the gender options of the private partner.

        :return: selection list of ``res.partner.gender``
        """
        return self.env["res.partner"]._fields["gender"].selection

    @api.model
    def _selection_marital(self):
        """Return the marital status options of the private partner.

        :return: selection list of ``res.partner.marital``
        """
        return self.env["res.partner"]._fields["marital"].selection

    @api.model
    def _selection_certificate(self):
        """Return the certificate level options of the employee.

        :return: selection list of ``hr.employee.certificate``
        """
        return self.env["hr.employee"]._fields["certificate"].selection

    date = fields.Date(
        string="Date",
        required=True,
        default=lambda self: fields.Date.context_today(self),
        readonly=True,
        states={"draft": [("readonly", False)]},
        copy=False,
        help="Date of the data change request. Defaults to today.",
    )

    # Previous values (snapshot of the employee)
    old_identification_id = fields.Char(
        string="Previous Identification No",
        readonly=True,
        help="Identification number of the employee before the change.",
    )
    old_place_of_birth = fields.Char(
        string="Previous Place of Birth",
        readonly=True,
        help="Place of birth of the employee before the change.",
    )
    old_birthday = fields.Date(
        string="Previous Date of Birth",
        readonly=True,
        help="Date of birth of the employee before the change.",
    )
    old_gender = fields.Selection(
        string="Previous Gender",
        selection="_selection_gender",
        readonly=True,
        help="Gender of the employee before the change.",
    )
    old_marital = fields.Selection(
        string="Previous Marital Status",
        selection="_selection_marital",
        readonly=True,
        help="Marital status of the employee before the change.",
    )
    old_spouse_complete_name = fields.Char(
        string="Previous Spouse Complete Name",
        readonly=True,
        help="Spouse name of the employee before the change.",
    )
    old_spouse_birthdate = fields.Date(
        string="Previous Spouse Birthdate",
        readonly=True,
        help="Spouse birthdate of the employee before the change.",
    )
    old_religion_id = fields.Many2one(
        string="Previous Religion",
        comodel_name="res_partner_religion",
        readonly=True,
        ondelete="restrict",
        help="Religion of the employee before the change.",
    )
    old_certificate = fields.Selection(
        string="Previous Certificate Level",
        selection="_selection_certificate",
        readonly=True,
        help="Certificate level of the employee before the change.",
    )
    old_image_1920 = fields.Image(
        string="Previous Photo",
        attachment=True,
        readonly=True,
        help="Photo of the employee before the change.",
    )

    # New values (empty means unchanged)
    new_identification_id = fields.Char(
        string="New Identification No",
        readonly=True,
        states={"draft": [("readonly", False)]},
        help="New identification number. Leave empty to keep the current one.",
    )
    new_place_of_birth = fields.Char(
        string="New Place of Birth",
        readonly=True,
        states={"draft": [("readonly", False)]},
        help="New place of birth. Leave empty to keep the current one.",
    )
    new_birthday = fields.Date(
        string="New Date of Birth",
        readonly=True,
        states={"draft": [("readonly", False)]},
        help="New date of birth. Leave empty to keep the current one.",
    )
    new_gender = fields.Selection(
        string="New Gender",
        selection="_selection_gender",
        readonly=True,
        states={"draft": [("readonly", False)]},
        help="New gender. Leave empty to keep the current one.",
    )
    new_marital = fields.Selection(
        string="New Marital Status",
        selection="_selection_marital",
        readonly=True,
        states={"draft": [("readonly", False)]},
        help="New marital status. Leave empty to keep the current one.",
    )
    new_spouse_complete_name = fields.Char(
        string="New Spouse Complete Name",
        readonly=True,
        states={"draft": [("readonly", False)]},
        help="New spouse name. Leave empty to keep the current one.",
    )
    new_spouse_birthdate = fields.Date(
        string="New Spouse Birthdate",
        readonly=True,
        states={"draft": [("readonly", False)]},
        help="New spouse birthdate. Leave empty to keep the current one.",
    )
    new_religion_id = fields.Many2one(
        string="New Religion",
        comodel_name="res_partner_religion",
        readonly=True,
        ondelete="restrict",
        states={"draft": [("readonly", False)]},
        help="New religion. Leave empty to keep the current one.",
    )
    new_certificate = fields.Selection(
        string="New Certificate Level",
        selection="_selection_certificate",
        readonly=True,
        states={"draft": [("readonly", False)]},
        help="New certificate level. Leave empty to keep the current one.",
    )
    new_image_1920 = fields.Image(
        string="New Photo",
        attachment=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
        help="New photo. Leave empty to keep the current one.",
    )

    child_ids = fields.One2many(
        string="New Children",
        comodel_name="employee_data_change_request_child",
        inverse_name="request_id",
        readonly=True,
        states={"draft": [("readonly", False)]},
        help="Children to add to the employee once the request is done.",
    )
    academic_ids = fields.One2many(
        string="New Academic History",
        comodel_name="employee_data_change_request_academic",
        inverse_name="request_id",
        readonly=True,
        states={"draft": [("readonly", False)]},
        help="Academic history entries to add once the request is done.",
    )

    @ssi_decorator.insert_on_form_view()
    def _insert_form_element(self, view_arch):
        if self._automatically_insert_view_element:
            view_arch = self._reconfigure_statusbar_visible(view_arch)
        return view_arch

    @api.model
    def _get_policy_field(self):
        res = super()._get_policy_field()
        policy_field = [
            "confirm_ok",
            "approve_ok",
            "reject_ok",
            "restart_approval_ok",
            "cancel_ok",
            "restart_ok",
            "done_ok",
            "manual_number_ok",
        ]
        res += policy_field
        return res

    # Snapshot of the employee values
    def _prepare_old_values(self):
        """Build the ``old_*`` values from the current employee data.

        :return: dict of ``old_<field>`` values, empty without employee
        """
        self.ensure_one()
        result = {}
        if not self.employee_id:
            return result
        employee = self.employee_id.sudo()
        for name in CHANGE_FIELDS:
            old_field = self._fields["old_%s" % name]
            value = employee[name]
            if old_field.type == "many2one":
                value = value.id
            result["old_%s" % name] = value
        return result

    def _refresh_old_values(self):
        """Overwrite the ``old_*`` snapshot with the current employee data.

        :return: nothing; writes the snapshot of each record
        """
        for record in self:
            record.write(record._prepare_old_values())

    @api.model
    def create(self, values):
        """Create the request and take the snapshot of the employee.

        :param dict values: values of the new request
        :return: the created request
        """
        result = super().create(values)
        result._refresh_old_values()
        return result

    def write(self, values):
        """Write the request and re-take the snapshot on employee change.

        :param dict values: values to write
        :return: result of the underlying ``write``
        """
        result = super().write(values)
        if "employee_id" in values:
            self.filtered(lambda r: r.state == "draft")._refresh_old_values()
        return result

    @ssi_decorator.pre_confirm_action()
    def _01_refresh_old_values_before_confirm(self):
        """Take the snapshot again so it reflects the data at submission.

        :return: nothing; refreshes the ``old_*`` values
        """
        self._refresh_old_values()

    # Constraints, evaluated when the request is submitted
    def _has_change(self):
        """Tell whether the request contains at least one change.

        :return: True when any ``new_*`` value or line is filled
        """
        self.ensure_one()
        for name in CHANGE_FIELDS:
            if self["new_%s" % name]:
                return True
        return bool(self.child_ids or self.academic_ids)

    @api.constrains("state")
    def _check_home_address_on_confirm(self):
        """Require a home address partner when the request is submitted.

        The related employee fields lose written values silently when
        the employee has no ``address_home_id``.

        :raises ValidationError: if the employee has no home address
        """
        for record in self.filtered(lambda r: r.state == "confirm"):
            if not record.employee_id.sudo().address_home_id:
                error_message = """
Context: Submit employee data change request
Database ID: %s
Problem: Employee has no private address partner
Solution: Fill the Private Address of the employee, then submit again
""" % (
                    record.id,
                )
                raise ValidationError(_(error_message))

    @api.constrains("state")
    def _check_has_change_on_confirm(self):
        """Require at least one change when the request is submitted.

        :raises ValidationError: if no value or line is filled
        """
        for record in self.filtered(lambda r: r.state == "confirm"):
            if not record._has_change():
                error_message = """
Context: Submit employee data change request
Database ID: %s
Problem: The request does not contain any change
Solution: Fill at least one new value, child, or academic history
""" % (
                    record.id,
                )
                raise ValidationError(_(error_message))

    # Apply the change when the request is done
    @ssi_decorator.post_done_action()
    def _01_apply_data_change_on_done(self):
        """Apply the approved change to the employee when done.

        :return: nothing; see ``_apply_data_change``
        """
        self._apply_data_change()

    def _prepare_employee_values(self):
        """Build the employee values from the filled ``new_*`` fields.

        :return: dict of employee values for the filled fields
        """
        self.ensure_one()
        result = {}
        for name in CHANGE_FIELDS:
            new_field = self._fields["new_%s" % name]
            value = self["new_%s" % name]
            if not value:
                continue
            if new_field.type == "many2one":
                value = value.id
            result[name] = value
        return result

    def _apply_data_change(self):
        """Write the approved changes to the employee and partner.

        Filled ``new_*`` values are written to the employee (related
        fields write through to the private partner). Child lines
        become private partners linked as children, and academic lines
        become ``partner.academic`` of the private partner. Runs with
        ``sudo`` so approvers outside HR are not blocked by the groups
        of the core employee fields.

        :return: nothing
        """
        self.ensure_one()
        employee = self.employee_id.sudo()
        values = self._prepare_employee_values()
        if values:
            employee.write(values)
        for child in self.child_ids:
            child._apply_to_employee(employee)
        for academic in self.academic_ids:
            academic._apply_to_employee(employee)

    # Self-service API
    @api.model
    def _self_service_scope(self, user_id):
        """Check the caller and scope the work to the employee of a user.

        Order of checks: the service account must be in the group
        ``group_employee_self_service_api``; the user must exist; the
        user must have an employee. The returned environment runs as
        the user (so ``create_uid`` and ``write_uid`` are the user)
        with ``sudo``, and the target is always the employee of the
        user.

        :param int user_id: id of the ``res.users`` record to act as
        :return: tuple of the scoped model and the employee record
        :raises AccessError: if the caller is not a self-service account
        :raises UserError: if the user does not exist or has no employee
        """
        if not self.env.user.has_group(SELF_SERVICE_GROUP):
            error_message = """
Context: Employee self-service
Problem: The caller is not an Employee Self-Service API account
Solution: Add the service account to the group Employee Self-Service API
"""
            raise AccessError(_(error_message))
        user = self.env["res.users"].sudo().browse(user_id).exists()
        if not user:
            error_message = """
Context: Employee self-service
Database ID: %s
Problem: The user does not exist
Solution: Use the id of an existing user
""" % (
                user_id,
            )
            raise UserError(_(error_message))
        scoped = self.with_user(user).sudo()
        employee = scoped.env["res.users"].browse(user.id).employee_id
        if not employee:
            error_message = """
Context: Employee self-service
Database ID: %s
Problem: The user is not linked to any employee
Solution: Link an employee to the user, then try again
""" % (
                user.id,
            )
            raise UserError(_(error_message))
        return scoped, employee

    @api.model
    def _self_service_name(self, value):
        """Return ``[id, name]`` for a record, or False when empty.

        :param value: a recordset of at most one record
        :return: ``[id, display_name]`` or False
        """
        if not value:
            return False
        return [value.id, value.display_name]

    @api.model
    def _self_service_selection_label(self, record, name):
        """Return the English label of the selection value of a field.

        :param record: record owning the field
        :param str name: field name
        :return: label of the value, or False when empty
        """
        value = record[name]
        if not value:
            return False
        selection = record._fields[name]._description_selection(record.env)
        return dict(selection).get(value, value)

    @api.model
    def self_service_read(self, user_id):
        """Return the data of the employee that belongs to a user.

        Public self-service method. The keys are the field names; the
        key ``labels`` maps each field name to its English label, and
        selection fields have an extra ``<name>_label`` key. Many2one
        values are ``[id, name]``, dates are ISO strings. The photo is
        returned as the small ``image_128`` thumbnail. The keys
        ``employment_status_id``, ``date_join``, ``date_permanent``,
        ``job_grade_id`` and ``vat`` (tax id of the private partner)
        are view-only data.

        Python test only: ``P1`` and ``L-01`` (the YAML ``call`` action
        drops the return value of a method).

        :param int user_id: id of the user to read the employee of
        :return: dict of view-only and changeable employee data
        :raises AccessError: if the caller is not a service account
        :raises UserError: if the user has no employee
        """
        scoped, employee = self._self_service_scope(user_id)
        employee = employee.sudo()
        partner = employee.address_home_id
        result = {
            "id": employee.id,
            "name": employee.name,
            "work_email": employee.work_email or False,
            "work_phone": employee.work_phone or False,
            "mobile_phone": employee.mobile_phone or False,
            "company_id": self._self_service_name(employee.company_id),
            "department_id": self._self_service_name(employee.department_id),
            "job_id": self._self_service_name(employee.job_id),
            "parent_id": self._self_service_name(employee.parent_id),
            "image_128": (employee.image_128 or b"").decode() or False,
            "emergency_contact": employee.emergency_contact or False,
            "emergency_phone": employee.emergency_phone or False,
            "has_private_address": bool(partner),
        }
        labels = {}
        for name in CHANGE_FIELDS + VIEW_ONLY_FIELDS:
            if name == "image_1920":
                continue
            field = employee._fields[name]
            labels[name] = field.string
            value = employee[name]
            if field.type == "many2one":
                value = self._self_service_name(value)
            elif field.type == "date":
                value = fields.Date.to_string(value) or False
            result[name] = value or False
            if field.type == "selection":
                result["%s_label" % name] = self._self_service_selection_label(
                    employee, name
                )
        for key, partner_key in CONTACT_PARTNER_KEYS.items():
            value = partner[partner_key] if partner else False
            if partner and partner._fields[partner_key].type == "many2one":
                value = self._self_service_name(value)
            result[key] = value or False
        result["vat"] = (partner.vat or False) if partner else False
        labels["vat"] = _("Tax ID (NPWP/NIK)")
        result["children"] = [
            {
                "id": child.id,
                "name": child.name,
                "gender": child.gender or False,
                "birthdate_date": fields.Date.to_string(child.birthdate_date) or False,
            }
            for child in (partner.children_ids if partner else [])
        ]
        result["academics"] = [
            {
                "id": academic.id,
                "name": academic.name or False,
                "education_level_id": self._self_service_name(
                    academic.education_level_id
                ),
                "field_of_study_id": self._self_service_name(
                    academic.field_of_study_id
                ),
                "date_start": fields.Date.to_string(academic.date_start) or False,
                "date_end": fields.Date.to_string(academic.date_end) or False,
                "diploma": academic.diploma or False,
                "gpa": academic.gpa,
            }
            for academic in (partner.academic_ids if partner else [])
        ]
        result["labels"] = labels
        return result

    @api.model
    def self_service_write_contact(self, user_id, vals):
        """Write the contact data of the employee that belongs to a user.

        Public self-service method. Keys are validated first, so a key
        outside the whitelist raises before anything is written. The
        keys ``street``, ``street2``, ``city``, ``state_id``, ``zip``,
        ``country_id``, ``phone``, ``mobile`` and ``private_email`` go
        to the private partner (``private_email`` is written to
        ``email``); ``emergency_contact`` and ``emergency_phone`` go to
        the employee. The write runs as the user, so ``write_uid`` is
        the user and not the service account.

        Python test only: ``P1`` and ``L-01`` (the YAML ``call`` action
        drops the return value of a method).

        :param int user_id: id of the user to write for
        :param dict vals: contact values to write
        :return: True
        :raises AccessError: if the caller is not a service account
        :raises UserError: if the user has no employee
        :raises ValidationError: on a key outside the whitelist, or
            when a partner key is sent and there is no private address
        """
        scoped, employee = self._self_service_scope(user_id)
        vals = vals or {}
        allowed = set(CONTACT_PARTNER_KEYS) | set(CONTACT_EMPLOYEE_KEYS)
        unknown = sorted(set(vals) - allowed)
        if unknown:
            error_message = """
Context: Employee self-service write contact
Problem: These keys cannot be written: %s
Solution: Use only %s
""" % (
                ", ".join(unknown),
                ", ".join(sorted(allowed)),
            )
            raise ValidationError(_(error_message))
        partner_vals = {
            CONTACT_PARTNER_KEYS[key]: value
            for key, value in vals.items()
            if key in CONTACT_PARTNER_KEYS
        }
        employee_vals = {
            key: value for key, value in vals.items() if key in CONTACT_EMPLOYEE_KEYS
        }
        partner = employee.address_home_id
        if partner_vals and not partner:
            error_message = """
Context: Employee self-service write contact
Database ID: %s
Problem: Employee has no private address partner
Solution: Fill the Private Address of the employee first
""" % (
                employee.id,
            )
            raise ValidationError(_(error_message))
        if partner_vals:
            partner.write(partner_vals)
        if employee_vals:
            employee.write(employee_vals)
        # Flush inside the scoped environment so no stored recompute
        # stays pending and gets written later as another user.
        employee.flush()
        return True

    @api.model
    def _self_service_lines(self, lines, allowed_keys):
        """Convert plain line dicts into ``(0, 0, vals)`` commands.

        :param list lines: list of dicts, or of ``(0, 0, dict)`` tuples
        :param list allowed_keys: keys a line may contain
        :return: list of create commands
        :raises ValidationError: on a malformed line or an unknown key
        """
        commands = []
        for line in lines or []:
            if isinstance(line, (list, tuple)) and len(line) == 3 and line[0] == 0:
                line = line[2]
            if not isinstance(line, dict):
                error_message = """
Context: Employee self-service create request
Problem: A line must be a dict of values
Solution: Send each child or academic line as a dict
"""
                raise ValidationError(_(error_message))
            unknown = sorted(set(line) - set(allowed_keys))
            if unknown:
                error_message = """
Context: Employee self-service create request
Problem: These line keys cannot be used: %s
Solution: Use only %s
""" % (
                    ", ".join(unknown),
                    ", ".join(allowed_keys),
                )
                raise ValidationError(_(error_message))
            commands.append((0, 0, dict(line)))
        return commands

    @api.model
    def self_service_create_request(self, user_id, vals):
        """Create a data change request for a user and submit it.

        Public self-service method. Accepted keys are the ``new_*``
        fields, ``child_ids`` and ``academic_ids`` (lists of dicts);
        ``employee_id`` is ignored because the employee is always the
        employee of the user, and any other key raises. The request is
        created as the user, so ``create_uid`` is the user, and then
        confirmed with the confirm policy bypassed because the
        service account, not the employee, is the actor.

        Python test only: ``P1`` and ``L-01`` (the YAML ``call`` action
        drops the return value of a method).

        :param int user_id: id of the user to create the request for
        :param dict vals: ``new_*``, ``child_ids`` and ``academic_ids``
        :return: id of the request, already in state ``confirm``
        :raises AccessError: if the caller is not a service account
        :raises UserError: if the user has no employee
        :raises ValidationError: on an unknown key or line
        """
        scoped, employee = self._self_service_scope(user_id)
        values = dict(vals or {})
        values.pop("employee_id", None)
        allowed = ["new_%s" % name for name in CHANGE_FIELDS]
        allowed += ["child_ids", "academic_ids"]
        unknown = sorted(set(values) - set(allowed))
        if unknown:
            error_message = """
Context: Employee self-service create request
Problem: These keys cannot be used: %s
Solution: Use only %s
""" % (
                ", ".join(unknown),
                ", ".join(allowed),
            )
            raise ValidationError(_(error_message))
        if "child_ids" in values:
            values["child_ids"] = self._self_service_lines(
                values["child_ids"], CHILD_LINE_KEYS
            )
        if "academic_ids" in values:
            values["academic_ids"] = self._self_service_lines(
                values["academic_ids"], ACADEMIC_LINE_KEYS
            )
        values["employee_id"] = employee.id
        values["user_id"] = scoped.env.uid
        request = scoped.create(values)
        request.with_context(bypass_policy_check=True).action_confirm()
        # Flush inside the scoped environment so every pending write
        # is made as the user and not by a later caller.
        request.flush()
        return request.id

    @api.model
    def _self_service_summary(self, request):
        """Return the labels of what a request changes.

        :param request: one ``employee_data_change_request`` record
        :return: list of the labels of the filled ``new_*`` fields,
            followed by ``Child: N`` and ``Academic: N`` when there
            are lines
        """
        employee = request.employee_id
        summary = []
        for name in CHANGE_FIELDS:
            if request["new_%s" % name]:
                summary.append(employee._fields[name].string)
        if request.child_ids:
            summary.append("Child: %s" % len(request.child_ids))
        if request.academic_ids:
            summary.append("Academic: %s" % len(request.academic_ids))
        return summary

    @api.model
    def self_service_list_request(self, user_id):
        """Return the data change requests of the employee of a user.

        Public self-service method. The environment is ``sudo`` and so
        skips the record rules; the domain on the employee is what
        scopes the result, so requests of other employees are never
        returned. Newest first. The key ``date`` is the ``date`` field of
        the request.

        Python test only: ``P1`` and ``L-01`` (the YAML ``call`` action
        drops the return value of a method).

        :param int user_id: id of the user to list the requests of
        :return: list of dicts with ``id``, ``name``, ``state``,
            ``state_label``, ``date``, ``create_date`` and ``summary``
        :raises AccessError: if the caller is not a service account
        :raises UserError: if the user has no employee
        """
        scoped, employee = self._self_service_scope(user_id)
        requests = scoped.search([("employee_id", "=", employee.id)], order="id desc")
        result = []
        for request in requests:
            created = request.create_date
            result.append(
                {
                    "id": request.id,
                    "name": request.name,
                    "state": request.state,
                    "state_label": self._self_service_selection_label(request, "state"),
                    "date": fields.Date.to_string(request.date) or False,
                    "create_date": created.isoformat() if created else False,
                    "summary": self._self_service_summary(request),
                }
            )
        return result

    @api.model
    def self_service_cancel_request(self, user_id, request_id):
        """Cancel a data change request of the employee of a user.

        Public self-service method. Only a request of the employee of
        the user can be cancelled, and only in state ``draft`` or
        ``confirm``. The answer for a missing request and for a request
        of another employee is the same. The cancel runs as the user
        with the cancel policy bypassed, because the service account,
        not the employee, is the actor; no cancel reason is set.

        Python test only: ``P1`` and ``L-01`` (the YAML ``call`` action
        drops the return value of a method).

        :param int user_id: id of the user to cancel the request for
        :param int request_id: id of the request to cancel
        :return: True
        :raises AccessError: if the caller is not a service account, or
            the request does not exist or belongs to another employee
        :raises UserError: if the user has no employee, or the request
            is not in state ``draft`` or ``confirm``
        """
        scoped, employee = self._self_service_scope(user_id)
        request = scoped.browse(request_id).exists()
        if not request or request.employee_id.id != employee.id:
            error_message = """
Context: Employee self-service cancel request
Database ID: %s
Problem: The request is not available for this user
Solution: Use the id of a request of the employee of the user
""" % (
                request_id,
            )
            raise AccessError(_(error_message))
        if request.state not in ("draft", "confirm"):
            error_message = """
Context: Employee self-service cancel request
Database ID: %s
Problem: Only a draft or confirmed request can be cancelled
Solution: Leave a request in another state as it is
""" % (
                request_id,
            )
            raise UserError(_(error_message))
        request.with_context(bypass_policy_check=True).action_cancel()
        # Flush inside the scoped environment so every pending write
        # is made as the user and not by a later caller.
        request.flush()
        return True
