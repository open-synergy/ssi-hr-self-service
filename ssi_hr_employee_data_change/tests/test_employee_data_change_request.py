# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestEmployeeDataChangeRequest(YamlTransactionCase):
    """Cover the ``employee_data_change_request`` workflow scenarios."""

    def test_employee_data_change_request(self):
        """Run the snapshot, constraint, approval and cancel scenarios."""
        self.run_yaml_scenario("test_data_employee_data_change_request.yaml")
