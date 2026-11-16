# Confirm Employee Data Change Request

> **Module:** `ssi_hr_employee_data_change`
>
> **Model:** `employee_data_change_request`
>
> **Menu:** Human Resource > Employees > Employee Data Change Request
>
> **Actor:** user in group _Employee Data Change Request — User_
>
> **State:** `draft` → `confirm`
>
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Draft**.
- **Record:** At least one **New** value, child line, or academic history line is
  filled.
- **Data:** The employee of the record has a **Private Address** partner. Without it the
  confirmation is refused, because the personal data fields would silently lose the
  written values.
- **Config:** An active `policy.template` for this model grants `confirm_ok` for state
  `draft` to the actor's group (see the _Standard_ `policy.template`).
- **Config:** An active `approval.template` for this model matches this record and has
  at least one approver level (see the _Standard_ `approval.template`, which defines a
  single sequential level approved by group _Employee Data Change Request — Validator_).
- **Access:** User is in group _Employee Data Change Request — User_.

## Flow

1. Open the **Human Resource > Employees > Employee Data Change Request** menu.
2. Open the record to confirm.
3. Click the **Confirm** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Waiting for Approval**.
- The **Previous** values are taken again from the employee, so they show the data at
  the time of submission.
- Approval records are created for each approver level defined by the _Standard_
  `approval.template`.
- Once every approval level has approved (see `05-approve`), the document transitions to
  **Done** automatically and the new values are applied to the employee.
