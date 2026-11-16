# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# pylint: disable=C8101

{
    "name": "Employee Data Change Request",
    "version": "14.0.1.0.1",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "contributors": [
        "Andhitia Rama <andhitia.r@gmail.com>",
    ],
    "license": "AGPL-3",
    "installable": True,
    "application": False,
    "depends": [
        "ssi_hr",
        "ssi_hr_employee",
        "ssi_hr_employee_personal_from_work_address",
        "ssi_hr_employee_experience_from_work_address",
        "ssi_employee_document_mixin",
        "ssi_transaction_confirm_mixin",
        "ssi_transaction_done_mixin",
        "ssi_transaction_cancel_mixin",
        "web_tour",
    ],
    "data": [
        "security/ir_module_category/employee_data_change_request.xml",
        "security/res_groups/employee_data_change_request.xml",
        "security/res_groups/employee_self_service_api.xml",
        "security/ir_model_access/employee_data_change_request.xml",
        "security/ir_model_access/employee_data_change_request_child.xml",
        "security/ir_model_access/employee_data_change_request_academic.xml",
        "security/ir_rule/employee_data_change_request.xml",
        "ir_sequence/employee_data_change_request.xml",
        "sequence_template/employee_data_change_request.xml",
        "approval_template/employee_data_change_request.xml",
        "policy_template/employee_data_change_request.xml",
        "views/employee_data_change_request_views.xml",
        "views/assets.xml",
    ],
}
