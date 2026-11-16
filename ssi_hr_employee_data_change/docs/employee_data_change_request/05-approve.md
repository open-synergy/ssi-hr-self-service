# Approve Employee Data Change Request

> **Module:** `ssi_hr_employee_data_change`
>
> **Model:** `employee_data_change_request`
>
> **Menu:** Human Resource > Employees > Employee Data Change Request
>
> **Actor:** user in group registered as an approver on the pending approval level
>
> **State:** `confirm` → `done`
>
> **Requires:** `04-confirm`

## Pre-Condition

- **Record:** Status is **Waiting for Approval**.
- **Config:** An active `policy.template` grants `approve_ok` to the actor — computed
  dynamically: the user must be registered as an approver on the currently pending
  approval level (see the _Standard_ `policy.template`).
- **Access:** User is registered as an approver on the approval level that is currently
  **pending**. The _Standard_ `approval.template` uses sequential approval with a single
  level, approved by group _Employee Data Change Request — Validator_.

## Flow

1. Open the **Human Resource > Employees > Employee Data Change Request** menu.
2. Open the record to approve.
3. Click the **Approve** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- If all approval levels are fulfilled, status changes to **Done** and every filled
  **New** value is written to the employee and its private address. New children are
  linked to the employee, and new academic history is added to the private address.
- If there are still pending approval levels, status remains **Waiting for Approval**
  and the next level becomes pending.
