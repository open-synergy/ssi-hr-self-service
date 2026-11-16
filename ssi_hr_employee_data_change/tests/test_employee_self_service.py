# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestEmployeeSelfService(YamlTransactionCase):
    """Cover the contact write and access scenarios of the self-service API."""

    def test_employee_self_service(self):
        """Run the write contact, whitelist and access scenarios."""
        self.run_yaml_scenario("test_data_employee_self_service.yaml")
