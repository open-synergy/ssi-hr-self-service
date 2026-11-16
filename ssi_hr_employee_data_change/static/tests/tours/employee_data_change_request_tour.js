odoo.define("ssi_hr_employee_data_change.employee_data_change_request_tour", function (
    require
) {
    "use strict";

    var tour = require("web_tour.tour");

    // Flow 1 of every IK in this file: "Open the Human Resource >
    // Employees > Employee Data Change Request menu." "Employees" has a
    // child menu, so it renders as a dropdown-toggle section; the request
    // menu is the leaf underneath it. The breadcrumb gate checks the ACTION
    // title ("Employee Data Change Request").
    var openList = function () {
        return [
            tour.stepUtils.showAppsMenuItem(),
            {
                content: "Open the Human Resource app",
                trigger: '.o_app[data-menu-xmlid="ssi_hr.menu_root_human_resource"]',
            },
            {
                content: "Open the Employees menu",
                trigger: '.o_menu_sections [data-menu-xmlid="ssi_hr.hr_employee_menu"]',
            },
            {
                content: "Open the Employee Data Change Request menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_hr_employee_data_change.employee_data_change_request_menu"]',
            },
            {
                content: "Employee Data Change Request list is displayed",
                trigger:
                    ".o_control_panel .breadcrumb-item.active:contains(Employee Data Change Request)",
                extra_trigger: ".o_list_view",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
        ];
    };

    // IK: docs/employee_data_change_request/01-create.md
    tour.register(
        "ssi_hr_employee_data_change_employee_data_change_request_create",
        {
            test: true,
            url: "/web",
        },
        [].concat(openList(), [
            // Flow 2 — Click the New button.
            {
                content: "Click New",
                trigger: ".o_list_button_add",
                extra_trigger: ".o_list_view",
            },
            {
                content: "Form is open in edit mode",
                trigger: ".o_form_view.o_form_editable",
                run: function () {
                    // Assertion only.
                },
            },
            // Flow 3 — Select the Employee.
            {
                content: "Select the Employee",
                trigger: ".o_field_many2one[name='employee_id'] input",
                extra_trigger: ".o_form_view.o_form_editable",
                run: "text TOUR EDC Employee Create",
            },
            {
                content: "Pick the Employee from the dropdown",
                trigger:
                    ".ui-autocomplete .ui-menu-item a:contains(TOUR EDC Employee Create)",
            },
            // Flow 4 — Fill in the New values of the Personal Data tab.
            {
                content: "Fill in New Identification No",
                trigger: ".o_field_widget[name='new_identification_id']",
                extra_trigger: ".o_form_view.o_form_editable",
                run: "text TOUR-EDC-NEW-ID",
            },
            {
                content: "Fill in New Date of Birth",
                trigger: ".o_field_widget[name='new_birthday'] input",
                extra_trigger: ".o_form_view.o_form_editable",
                run: "text 05/06/1992",
            },
            // Flow 5 — Add a child on the Children tab.
            {
                content: "Open the Children tab",
                trigger: ".o_notebook .nav-link:contains(Children)",
                extra_trigger: ".o_form_view.o_form_editable",
            },
            {
                content: "Add a child line",
                trigger:
                    ".o_field_x2many[name='child_ids'] .o_field_x2many_list_row_add a",
            },
            {
                content: "Fill in the child Name",
                trigger:
                    ".o_field_x2many[name='child_ids'] .o_selected_row .o_field_widget[name='name']",
                run: "text TOUR EDC Child",
            },
            // Flow 6 — Add an academic history on the Academic History tab.
            {
                content: "Open the Academic History tab",
                trigger: ".o_notebook .nav-link:contains(Academic History)",
                extra_trigger: ".o_form_view.o_form_editable",
            },
            {
                content: "Add an academic history line",
                trigger:
                    ".o_field_x2many[name='academic_ids'] .o_field_x2many_list_row_add a",
            },
            {
                content: "Fill in the Institution",
                trigger:
                    ".o_field_x2many[name='academic_ids'] .o_selected_row .o_field_widget[name='name']",
                run: "text TOUR EDC University",
            },
            {
                content: "Fill in the Date Start",
                trigger:
                    ".o_field_x2many[name='academic_ids'] .o_selected_row .o_field_widget[name='date_start'] input",
                run: "text 08/01/2010",
            },
            // Flow 7 — Click Save.
            {
                content: "Save the record",
                trigger: ".o_form_button_save",
            },
            // Post-Condition — a new record is created in Draft status.
            {
                content: "Record is saved",
                trigger: ".o_form_view.o_form_readonly",
                run: function () {
                    // Assertion only.
                },
            },
            {
                content: "Status is Draft",
                trigger:
                    ".o_statusbar_status .o_arrow_button[data-value='draft'].btn-primary",
                run: function () {
                    // Assertion only.
                },
            },
        ])
    );

    // IK: docs/employee_data_change_request/02-edit.md
    tour.register(
        "ssi_hr_employee_data_change_employee_data_change_request_edit",
        {
            test: true,
            url: "/web",
        },
        [].concat(openList(), [
            // Flow 2 — Open the record.
            {
                content: "Open the record",
                trigger:
                    ".o_data_row:contains(TOUR EDC Employee Edit) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                content: "Record is open",
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only.
                },
            },
            {
                content: "Click the Edit button",
                trigger: ".o_form_button_edit",
            },
            {
                content: "Form is now editable",
                trigger: ".o_form_view.o_form_editable",
                run: function () {
                    // Assertion only.
                },
            },
            // Flow 4 — Change the New values.
            {
                content: "Change New Place of Birth",
                trigger: ".o_field_widget[name='new_place_of_birth']",
                extra_trigger: ".o_form_view.o_form_editable",
                run: "text TOUR Edit City",
            },
            // Flow 5 — Click Save.
            {
                content: "Save the record",
                trigger: ".o_form_button_save",
            },
            // Post-Condition — the record is updated with the new values.
            {
                content: "Record is saved",
                trigger: ".o_form_view.o_form_readonly",
                run: function () {
                    // Assertion only.
                },
            },
        ])
    );

    // IK: docs/employee_data_change_request/03-delete.md
    tour.register(
        "ssi_hr_employee_data_change_employee_data_change_request_delete",
        {
            test: true,
            url: "/web",
        },
        [].concat(openList(), [
            // Flow 2 — Open the record.
            {
                content: "Open the record",
                trigger:
                    ".o_data_row:contains(TOUR EDC Employee Delete) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                content: "Record is open",
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only.
                },
            },
            // Flow 3 — Click Action > Delete.
            {
                content: "Open the Action menu",
                trigger: ".o_cp_action_menus button:contains(Action)",
            },
            {
                content: "Click Delete",
                trigger: ".o_cp_action_menus .o_menu_item a",
                run: function () {
                    var $delete = $(".o_cp_action_menus .o_menu_item a").filter(
                        function () {
                            return $(this).text().trim() === "Delete";
                        }
                    );
                    $delete[0].click();
                },
            },
            // Flow 4 — Click OK to confirm.
            {
                content: "Confirm the dialog",
                trigger: ".modal-footer button.btn-primary",
                in_modal: true,
            },
            // After delete, 14.0 can display the NEXT record instead of
            // returning to the list. Click the breadcrumb explicitly.
            {
                content: "Click the Employee Data Change Request breadcrumb",
                trigger:
                    ".breadcrumb-item.o_back_button a:contains(Employee Data Change Request)",
            },
            // Post-Condition — the record is permanently removed.
            {
                content: "Record is removed from the list",
                trigger:
                    ".o_list_view:not(:has(.o_data_row:contains(TOUR EDC Employee Delete)))",
                run: function () {
                    // Assertion only.
                },
            },
        ])
    );

    // IK: docs/employee_data_change_request/04-confirm.md
    tour.register(
        "ssi_hr_employee_data_change_employee_data_change_request_confirm",
        {
            test: true,
            url: "/web",
        },
        [].concat(openList(), [
            // Flow 2 — Open the record.
            {
                content: "Open the record",
                trigger:
                    ".o_data_row:contains(TOUR EDC Employee Confirm) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                content: "Record is open",
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only.
                },
            },
            // Flow 3 — Click the Confirm button.
            {
                content: "Click the Confirm button",
                trigger: ".o_statusbar_buttons button[name='action_confirm']",
                extra_trigger: ".o_form_view",
            },
            // Flow 4 — Click OK on the confirmation dialog.
            {
                content: "Confirm the dialog",
                trigger: ".modal-footer button.btn-primary",
                in_modal: true,
            },
            // Post-Condition.
            {
                content: "Status is Waiting for Approval",
                trigger:
                    ".o_statusbar_status .o_arrow_button[data-value='confirm'].btn-primary",
                run: function () {
                    // Assertion only.
                },
            },
        ])
    );

    // IK: docs/employee_data_change_request/05-approve.md
    tour.register(
        "ssi_hr_employee_data_change_employee_data_change_request_approve",
        {
            test: true,
            url: "/web",
        },
        [].concat(openList(), [
            // Flow 2 — Open the record.
            {
                content: "Open the record",
                trigger:
                    ".o_data_row:contains(TOUR EDC Employee Approve) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                content: "Record is open",
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only.
                },
            },
            // Flow 3 — Click the Approve button.
            {
                content: "Click the Approve button",
                trigger: ".o_statusbar_buttons button[name='action_approve_approval']",
                extra_trigger: ".o_form_view",
            },
            // Flow 4 — Click OK on the confirmation dialog.
            {
                content: "Confirm the dialog",
                trigger: ".modal-footer button.btn-primary",
                in_modal: true,
            },
            // Post-Condition.
            {
                content: "Status is Done",
                trigger:
                    ".o_statusbar_status .o_arrow_button[data-value='done'].btn-primary",
                run: function () {
                    // Assertion only.
                },
            },
        ])
    );

    // IK: docs/employee_data_change_request/06-reject.md
    tour.register(
        "ssi_hr_employee_data_change_employee_data_change_request_reject",
        {
            test: true,
            url: "/web",
        },
        [].concat(openList(), [
            // Flow 2 — Open the record.
            {
                content: "Open the record",
                trigger:
                    ".o_data_row:contains(TOUR EDC Employee Reject) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                content: "Record is open",
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only.
                },
            },
            // Flow 3 — Click the Reject button.
            {
                content: "Click the Reject button",
                trigger: ".o_statusbar_buttons button[name='action_reject_approval']",
                extra_trigger: ".o_form_view",
            },
            // Flow 4 — Click OK on the confirmation dialog.
            {
                content: "Confirm the dialog",
                trigger: ".modal-footer button.btn-primary",
                in_modal: true,
            },
            // Post-Condition.
            {
                content: "Status is Rejected",
                trigger:
                    ".o_statusbar_status .o_arrow_button[data-value='reject'].btn-primary",
                run: function () {
                    // Assertion only.
                },
            },
        ])
    );

    // IK: docs/employee_data_change_request/09-finish.md
    tour.register(
        "ssi_hr_employee_data_change_employee_data_change_request_finish",
        {
            test: true,
            url: "/web",
        },
        [].concat(openList(), [
            // Flow 2 — Open the record.
            {
                content: "Open the record",
                trigger:
                    ".o_data_row:contains(TOUR EDC Employee Finish) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                content: "Record is open",
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only.
                },
            },
            // Flow 3 — Click the Done button.
            {
                content: "Click the Done button",
                trigger: ".o_statusbar_buttons button[name='action_done']",
                extra_trigger: ".o_form_view",
            },
            // Flow 4 — Click OK on the confirmation dialog.
            {
                content: "Confirm the dialog",
                trigger: ".modal-footer button.btn-primary",
                in_modal: true,
            },
            // Post-Condition.
            {
                content: "Status is Done",
                trigger:
                    ".o_statusbar_status .o_arrow_button[data-value='done'].btn-primary",
                run: function () {
                    // Assertion only.
                },
            },
        ])
    );

    // IK: docs/employee_data_change_request/10-cancel.md
    tour.register(
        "ssi_hr_employee_data_change_employee_data_change_request_cancel",
        {
            test: true,
            url: "/web",
        },
        [].concat(openList(), [
            // Flow 2 — Open the record.
            {
                content: "Open the record",
                trigger:
                    ".o_data_row:contains(TOUR EDC Employee Cancel) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                content: "Record is open",
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only.
                },
            },
            // Flow 3 — Click the Cancel button. type="action": the rendered
            // `name` is a resolved numeric action id, so target by label.
            {
                content: "Click the Cancel button",
                trigger: ".o_statusbar_buttons button:enabled:contains('Cancel')",
                extra_trigger: ".o_form_view",
            },
            // Flow 4 — In the wizard, select the Reason.
            {
                content: "Wizard is open",
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only.
                },
            },
            {
                content: "Select the cancellation reason",
                trigger:
                    ".o_field_widget[name='cancel_reason_id'] .o_radio_item label:contains(TOUR EDC Cancel Reason)",
            },
            // Flow 5 — Click Confirm. The wizard's own Confirm button carries
            // confirm="Are you sure?" — a SECOND dialog stacks on the wizard.
            {
                content: "Confirm the wizard",
                trigger: ".modal-footer button[name='action_confirm']",
            },
            // Flow 6 — Click OK on the confirmation dialog.
            {
                content: "Confirm the dialog",
                trigger: ".modal-footer button.btn-primary",
                in_modal: true,
            },
            // Post-Condition — status changes to Cancelled.
            {
                content: "Status is Cancelled",
                trigger:
                    ".o_statusbar_status .o_arrow_button[data-value='cancel'].btn-primary",
                run: function () {
                    // Assertion only.
                },
            },
        ])
    );

    // IK: docs/employee_data_change_request/12-restart.md
    tour.register(
        "ssi_hr_employee_data_change_employee_data_change_request_restart",
        {
            test: true,
            url: "/web",
        },
        [].concat(openList(), [
            // Flow 2 — Open the record.
            {
                content: "Open the record",
                trigger:
                    ".o_data_row:contains(TOUR EDC Employee Restart) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                content: "Record is open",
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only.
                },
            },
            {
                content: "Click the Restart button",
                trigger: ".o_statusbar_buttons button[name='action_restart']",
                extra_trigger: ".o_form_view",
            },
            {
                content: "Confirm the dialog",
                trigger: ".modal-footer button.btn-primary",
                in_modal: true,
            },
            {
                content: "Status is Draft",
                trigger:
                    ".o_statusbar_status .o_arrow_button[data-value='draft'].btn-primary",
                run: function () {
                    // Assertion only.
                },
            },
        ])
    );

    // IK: docs/employee_data_change_request/14-restart-approval.md
    tour.register(
        "ssi_hr_employee_data_change_employee_data_change_request_restart_approval",
        {
            test: true,
            url: "/web",
        },
        [].concat(openList(), [
            // Flow 2 — Open the record.
            {
                content: "Open the record",
                trigger:
                    ".o_data_row:contains(TOUR EDC Employee Reload Approval) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                content: "Record is open",
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only.
                },
            },
            {
                content: "Click the Restart Approval Process button",
                trigger:
                    ".o_statusbar_buttons button[name='action_reload_approval_template']",
                extra_trigger: ".o_form_view",
            },
            {
                content: "Confirm the dialog",
                trigger: ".modal-footer button.btn-primary",
                in_modal: true,
            },
            {
                content: "Open the Approvals tab",
                trigger: ".o_notebook .nav-link:contains(Approvals)",
                extra_trigger: "body:not(:has(.modal))",
            },
            // The Pre-Condition record has no approval line at all, so a row
            // cannot appear here unless the restart actually ran.
            {
                content: "The approval process has been rebuilt",
                trigger: ".o_field_widget[name='approval_ids'] .o_data_row",
                run: function () {
                    // Assertion only.
                },
            },
            {
                content: "Status is Waiting for Approval",
                trigger:
                    ".o_statusbar_status .o_arrow_button[data-value='confirm'].btn-primary",
                run: function () {
                    // Assertion only.
                },
            },
        ])
    );
});
