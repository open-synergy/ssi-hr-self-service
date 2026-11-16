# Finish Employee Data Change Request

> **Module:** `ssi_hr_employee_data_change`
>
> **Model:** `employee_data_change_request`
>
> **Menu:** Human Resource > Employees > Employee Data Change Request
>
> **Actor:** user in group _Employee Data Change Request — User_
>
> **State:** `confirm` → `done`
>
> **Requires:** `04-confirm`

## Pre-Condition

- **Record:** Status is **Waiting for Approval**.
- **Config:** An active `policy.template` for this model grants `done_ok` for state
  `confirm` to the actor's group (see the _Standard_ `policy.template`).
- **Access:** User is in group _Employee Data Change Request — User_.

## Flow

1. Open the **Human Resource > Employees > Employee Data Change Request** menu.
2. Open the record to finish.
3. Click the **Done** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Done**.
- Every filled **New** value is written to the employee and its private address, new
  children are linked to the employee, and new academic history is added.
