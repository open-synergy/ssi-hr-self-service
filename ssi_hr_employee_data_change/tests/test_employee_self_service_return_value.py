# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo import fields
from odoo.exceptions import AccessError, UserError
from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestEmployeeSelfServiceReturnValue(YamlTransactionCase):
    """Assert the return values of the self-service model methods."""

    def setUp(self):
        """Create a service account and two employees with their users."""
        super().setUp()
        group = self.env.ref(
            "ssi_hr_employee_data_change.group_employee_self_service_api"
        )
        self.service_user = self.env["res.users"].create(
            {
                "name": "EDC P1 Service",
                "login": "edc_p1_service",
                "groups_id": [(4, group.id)],
            }
        )
        self.user_a, self.employee_a = self._create_employee_user("A")
        self.user_b, self.employee_b = self._create_employee_user("B")
        self.model = self.env["employee_data_change_request"].with_user(
            self.service_user
        )

    def _create_employee_user(self, tag):
        """Create a user with an employee that has a private address.

        :param str tag: suffix that makes the names and login unique
        :return: tuple of the user and the employee
        """
        user = self.env["res.users"].create(
            {"name": "EDC P1 User %s" % tag, "login": "edc_p1_user_%s" % tag.lower()}
        )
        partner = self.env["res.partner"].create(
            {
                "name": "EDC P1 Private %s" % tag,
                "type": "private",
                "vat": "VAT-%s" % tag,
            }
        )
        status = self.env["hr.employment_status"].create(
            {"name": "EDC P1 Status %s" % tag, "code": "/"}
        )
        grade = self.env["hr.job_grade"].create(
            {"name": "EDC P1 Grade %s" % tag, "code": "/"}
        )
        employee = self.env["hr.employee"].create(
            {
                "name": "EDC P1 Employee %s" % tag,
                "user_id": user.id,
                "address_home_id": partner.id,
                "emergency_phone": "PHONE-%s" % tag,
                "employment_status_id": status.id,
                "job_grade_id": grade.id,
                "date_join": "2020-01-15",
                "date_permanent": "2020-07-15",
            }
        )
        return user, employee

    def _create_request(self, employee, state=False):
        """Create a data change request of an employee.

        :param employee: the employee that owns the request
        :param str state: state to force on the request, if any
        :return: the new request
        """
        request = self.env["employee_data_change_request"].create(
            {
                "employee_id": employee.id,
                "new_identification_id": "P1-REQ-%s" % employee.id,
                "new_place_of_birth": "P1 City",
            }
        )
        if state:
            request.write({"state": state})
        return request

    def test_self_service_read(self):
        """Return the data of the employee of the user, not of another one.

        Pure Python - trigger P1 (L-01: the ``call`` action discards the
        return value of a method, so YAML cannot assert it at all).
        """
        data = self.model.self_service_read(self.user_a.id)
        self.assertEqual(data["id"], self.employee_a.id)
        self.assertEqual(data["name"], "EDC P1 Employee A")
        self.assertEqual(data["emergency_phone"], "PHONE-A")
        for key in ("labels", "children", "academics", "identification_id"):
            self.assertIn(key, data)
        self.assertNotEqual(data["id"], self.employee_b.id)

    def test_self_service_read_view_only(self):
        """Return the five view-only keys and keep the old keys.

        Pure Python - trigger P1 (L-01: the ``call`` action discards the
        return value of a method, so YAML cannot assert it at all).
        """
        data = self.model.self_service_read(self.user_a.id)
        employee = self.employee_a
        self.assertEqual(
            data["employment_status_id"],
            [employee.employment_status_id.id, "EDC P1 Status A"],
        )
        self.assertEqual(
            data["job_grade_id"], [employee.job_grade_id.id, "EDC P1 Grade A"]
        )
        self.assertEqual(data["date_join"], "2020-01-15")
        self.assertEqual(data["date_permanent"], "2020-07-15")
        self.assertEqual(data["vat"], employee.address_home_id.vat)
        self.assertEqual(data["vat"], "VAT-A")
        self.assertEqual(data["labels"]["job_grade_id"], "Job Grade")
        self.assertIn("vat", data["labels"])
        for key in ("work_email", "department_id", "has_private_address"):
            self.assertIn(key, data)

    def test_self_service_read_view_only_empty(self):
        """Return ``False`` for the view-only keys of an empty employee.

        Pure Python - trigger P1 (L-01: the ``call`` action discards the
        return value of a method, so YAML cannot assert it at all).
        """
        self.employee_a.write(
            {
                "employment_status_id": False,
                "job_grade_id": False,
                "date_join": False,
                "date_permanent": False,
                "address_home_id": False,
            }
        )
        data = self.model.self_service_read(self.user_a.id)
        for key in (
            "employment_status_id",
            "job_grade_id",
            "date_join",
            "date_permanent",
            "vat",
        ):
            self.assertIs(data[key], False)

    def test_self_service_list_request(self):
        """List the requests of the user's employee only, newest first.

        Pure Python - trigger P1 (L-01: the ``call`` action discards the
        return value of a method, so YAML cannot assert it at all).
        """
        first = self._create_request(self.employee_a)
        second = self._create_request(self.employee_a)
        other = self._create_request(self.employee_b)
        result = self.model.self_service_list_request(self.user_a.id)
        ids = [item["id"] for item in result]
        self.assertEqual(ids, [second.id, first.id])
        self.assertNotIn(other.id, ids)
        item = result[0]
        for key in ("id", "name", "state", "state_label", "date", "create_date"):
            self.assertIn(key, item)
        self.assertEqual(item["state"], "draft")
        self.assertEqual(item["state_label"], "Draft")
        today = fields.Date.to_string(fields.Date.context_today(second))
        self.assertEqual(item["date"], today)
        self.assertIn("Identification No", " ".join(item["summary"]))
        self.assertIn("Place of Birth", " ".join(item["summary"]))
        self.assertEqual(len(item["summary"]), 2)

    def test_self_service_list_request_lines(self):
        """Count the child and academic lines in the summary.

        Pure Python - trigger P1 (L-01: the ``call`` action discards the
        return value of a method, so YAML cannot assert it at all).
        """
        request = self._create_request(self.employee_a)
        request.write(
            {
                "child_ids": [
                    (0, 0, {"name": "P1 Child 1", "birthdate_date": "2020-02-02"}),
                    (0, 0, {"name": "P1 Child 2", "birthdate_date": "2021-03-03"}),
                ],
                "academic_ids": [
                    (0, 0, {"name": "P1 University", "date_start": "2015-08-01"})
                ],
            }
        )
        result = self.model.self_service_list_request(self.user_a.id)
        self.assertEqual(len(result), 1)
        self.assertIn("Child: 2", result[0]["summary"])
        self.assertIn("Academic: 1", result[0]["summary"])

    def test_self_service_list_request_date(self):
        """Return the ``date`` field of the request, not ``create_date``.

        Pure Python - trigger P1 (L-01: the ``call`` action discards the
        return value of a method, so YAML cannot assert it at all).
        """
        request = self._create_request(self.employee_a)
        request.write({"date": "2020-05-17"})
        result = self.model.self_service_list_request(self.user_a.id)
        self.assertEqual(result[0]["date"], "2020-05-17")
        self.assertNotEqual(result[0]["date"], result[0]["create_date"][:10])

    def test_self_service_list_request_empty(self):
        """Return an empty list for an employee without requests.

        Pure Python - trigger P1 (L-01: the ``call`` action discards the
        return value of a method, so YAML cannot assert it at all).
        """
        self._create_request(self.employee_b)
        self.assertEqual(self.model.self_service_list_request(self.user_a.id), [])

    def test_self_service_list_request_access(self):
        """Refuse a caller that is not a service account.

        Pure Python - trigger P1 (L-01: the ``call`` action discards the
        return value of a method, so YAML cannot assert it at all).
        """
        model = self.env["employee_data_change_request"].with_user(self.user_a)
        with self.assertRaises(AccessError):
            model.self_service_list_request(self.user_a.id)

    def test_self_service_cancel_request(self):
        """Return True and cancel the request as the employee.

        Pure Python - trigger P1 (L-01: the ``call`` action discards the
        return value of a method, so YAML cannot assert it at all).
        """
        request = self._create_request(self.employee_a)
        result = self.model.self_service_cancel_request(self.user_a.id, request.id)
        self.assertIs(result, True)
        request.invalidate_cache()
        self.assertEqual(request.state, "cancel")
        self.assertEqual(request.write_uid, self.user_a)
        self.assertFalse(request.cancel_reason_id)

    def test_self_service_cancel_request_other(self):
        """Refuse a request of another employee, same as a missing one.

        Pure Python - trigger P1 (L-01: the ``call`` action discards the
        return value of a method, so YAML cannot assert it at all).
        """
        other = self._create_request(self.employee_b)
        with self.assertRaises(AccessError) as other_error:
            self.model.self_service_cancel_request(self.user_a.id, other.id)
        with self.assertRaises(AccessError) as missing_error:
            self.model.self_service_cancel_request(self.user_a.id, other.id + 100000)
        self.assertNotIn("another", str(other_error.exception))
        self.assertEqual(
            str(other_error.exception).split("Database ID")[0],
            str(missing_error.exception).split("Database ID")[0],
        )
        other.invalidate_cache()
        self.assertEqual(other.state, "draft")

    def test_self_service_cancel_request_state(self):
        """Refuse to cancel a request that is already done.

        Pure Python - trigger P1 (L-01: the ``call`` action discards the
        return value of a method, so YAML cannot assert it at all).
        """
        request = self._create_request(self.employee_a, state="done")
        with self.assertRaises(UserError):
            self.model.self_service_cancel_request(self.user_a.id, request.id)
        request.invalidate_cache()
        self.assertEqual(request.state, "done")

    def test_self_service_cancel_request_access(self):
        """Refuse a caller that is not a service account.

        Pure Python - trigger P1 (L-01: the ``call`` action discards the
        return value of a method, so YAML cannot assert it at all).
        """
        request = self._create_request(self.employee_a)
        model = self.env["employee_data_change_request"].with_user(self.user_a)
        with self.assertRaises(AccessError):
            model.self_service_cancel_request(self.user_a.id, request.id)

    def test_self_service_create_request(self):
        """Return the id of a confirmed request owned by the user's employee.

        The ``employee_id`` smuggled into the values is ignored.

        Pure Python - trigger P1 (L-01: the ``call`` action discards the
        return value of a method, so YAML cannot assert it at all).
        """
        request_id = self.model.self_service_create_request(
            self.user_a.id,
            {
                "employee_id": self.employee_b.id,
                "new_identification_id": "P1-NEW-ID",
            },
        )
        request = self.env["employee_data_change_request"].browse(request_id)
        self.assertEqual(request.employee_id, self.employee_a)
        self.assertEqual(request.create_uid, self.user_a)
        self.assertEqual(request.state, "confirm")
        self.assertEqual(request.old_identification_id, False)
        self.assertEqual(request.date, fields.Date.context_today(request))

    def test_self_service_write_uid(self):
        """Write the contact as the user, so ``write_uid`` is not the service.

        Pure Python - trigger P1 (L-01: the ``call`` action discards the
        return value of a method, so YAML cannot assert it at all).
        """
        result = self.model.self_service_write_contact(
            self.user_a.id, {"emergency_phone": "PHONE-A-NEW"}
        )
        self.assertTrue(result)
        self.employee_a.invalidate_cache()
        self.assertEqual(self.employee_a.emergency_phone, "PHONE-A-NEW")
        self.assertEqual(self.employee_a.write_uid, self.user_a)
        self.assertNotEqual(self.employee_a.write_uid, self.service_user)
