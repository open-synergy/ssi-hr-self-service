# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

# HttpSavepointCase - NOT HttpCase. 14.0's HttpCase has no cls.env in
# setUpClass (see odoo-development-ui-test skill, structure-and-runner.md).
from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiEmployeeDataChangeRequest(HttpSavepointCase):
    """Tour tests for the ``employee_data_change_request`` work instructions."""

    @classmethod
    def setUpClass(cls):
        """Create the request fixtures each tour needs.

        ``employee_data_change_request_validator_group`` grants
        ``base.user_admin`` membership by default and implies the user and
        viewer groups, so ``admin`` can run every tour here, including
        approving: the shipped "Standard" ``approval.template`` draws its
        approvers from the same Validator group.

        Every request's ``user_id`` is set to ``admin`` explicitly, because
        ``cls.env`` runs as SUPERUSER and the internal user record rule
        would otherwise hide records owned by someone else from the tour
        session. The employee name is the stable marker each tour uses to
        find its row in the list view.
        """
        super().setUpClass()
        cls.admin = cls.env.ref("base.user_admin")
        cls.cancel_reason = cls.env["base.cancel_reason"].create(
            {
                "name": "TOUR EDC Cancel Reason",
                "code": "TOUREDC",
                "global_use": True,
            }
        )
        cls.employee_create = cls._create_employee("Create")
        cls._create_request("Edit")
        cls._create_request("Delete")
        cls._create_request("Confirm")
        cls._create_request("Approve").with_user(cls.admin).action_confirm()
        cls._create_request("Reject").with_user(cls.admin).action_confirm()
        cls._create_request("Finish").with_user(cls.admin).action_confirm()
        cls._create_request("Cancel")
        restart = cls._create_request("Restart")
        restart.with_user(cls.admin).with_context(
            bypass_policy_check=True
        ).action_cancel(cls.cancel_reason)

        # Pre-Condition of the restart-approval tour: the button only exists
        # while the confirmed record has NO approval template, so the
        # standard template is deactivated for this one confirmation.
        approval_template = cls.env.ref(
            "ssi_hr_employee_data_change.employee_data_change_request_approval_template"
        ).sudo()
        stalled = cls._create_request("Reload Approval")
        approval_template.write({"active": False})
        stalled.with_user(cls.admin).with_context(
            bypass_policy_check=True
        ).action_confirm()
        approval_template.write({"active": True})
        cls.env["employee_data_change_request"].invalidate_cache()

    @classmethod
    def _create_employee(cls, tag):
        """Create an employee that has a private address partner.

        :param str tag: marker appended to the employee name
        :return: the created ``hr.employee`` record
        """
        partner = cls.env["res.partner"].create(
            {"name": "TOUR EDC Private %s" % tag, "type": "private"}
        )
        return cls.env["hr.employee"].create(
            {
                "name": "TOUR EDC Employee %s" % tag,
                "address_home_id": partner.id,
            }
        )

    @classmethod
    def _create_request(cls, tag):
        """Create one draft request with a change to apply.

        :param str tag: marker of the employee the request belongs to
        :return: the created ``employee_data_change_request`` record
        """
        employee = cls._create_employee(tag)
        return cls.env["employee_data_change_request"].create(
            {
                "employee_id": employee.id,
                "user_id": cls.admin.id,
                "new_identification_id": "TOUR-EDC-%s" % tag.upper(),
            }
        )

    def test_create(self):
        """Run the create tour for ``employee_data_change_request``.

        IK: docs/employee_data_change_request/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_hr_employee_data_change_employee_data_change_request_create",
            login="admin",
        )

    def test_edit(self):
        """Run the edit tour for ``employee_data_change_request``.

        IK: docs/employee_data_change_request/02-edit.md
        """
        self.start_tour(
            "/web",
            "ssi_hr_employee_data_change_employee_data_change_request_edit",
            login="admin",
        )

    def test_delete(self):
        """Run the delete tour for ``employee_data_change_request``.

        IK: docs/employee_data_change_request/03-delete.md
        """
        self.start_tour(
            "/web",
            "ssi_hr_employee_data_change_employee_data_change_request_delete",
            login="admin",
        )

    def test_confirm(self):
        """Run the confirm tour for ``employee_data_change_request``.

        IK: docs/employee_data_change_request/04-confirm.md
        """
        self.start_tour(
            "/web",
            "ssi_hr_employee_data_change_employee_data_change_request_confirm",
            login="admin",
        )

    def test_approve(self):
        """Run the approve tour for ``employee_data_change_request``.

        IK: docs/employee_data_change_request/05-approve.md
        """
        self.start_tour(
            "/web",
            "ssi_hr_employee_data_change_employee_data_change_request_approve",
            login="admin",
        )

    def test_reject(self):
        """Run the reject tour for ``employee_data_change_request``.

        IK: docs/employee_data_change_request/06-reject.md
        """
        self.start_tour(
            "/web",
            "ssi_hr_employee_data_change_employee_data_change_request_reject",
            login="admin",
        )

    def test_finish(self):
        """Run the finish tour for ``employee_data_change_request``.

        IK: docs/employee_data_change_request/09-finish.md
        """
        self.start_tour(
            "/web",
            "ssi_hr_employee_data_change_employee_data_change_request_finish",
            login="admin",
        )

    def test_cancel(self):
        """Run the cancel tour for ``employee_data_change_request``.

        IK: docs/employee_data_change_request/10-cancel.md
        """
        self.start_tour(
            "/web",
            "ssi_hr_employee_data_change_employee_data_change_request_cancel",
            login="admin",
        )

    def test_restart(self):
        """Run the restart tour for ``employee_data_change_request``.

        IK: docs/employee_data_change_request/12-restart.md
        """
        self.start_tour(
            "/web",
            "ssi_hr_employee_data_change_employee_data_change_request_restart",
            login="admin",
        )

    def test_restart_approval(self):
        """Run the restart approval tour for ``employee_data_change_request``.

        IK: docs/employee_data_change_request/14-restart-approval.md
        """
        self.start_tour(
            "/web",
            "ssi_hr_employee_data_change_employee_data_change_request_restart_approval",
            login="admin",
        )
