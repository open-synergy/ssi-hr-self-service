# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

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
            {"name": "EDC P1 Private %s" % tag, "type": "private"}
        )
        employee = self.env["hr.employee"].create(
            {
                "name": "EDC P1 Employee %s" % tag,
                "user_id": user.id,
                "address_home_id": partner.id,
                "emergency_phone": "PHONE-%s" % tag,
            }
        )
        return user, employee

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
