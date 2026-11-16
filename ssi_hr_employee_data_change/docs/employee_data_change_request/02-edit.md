# Edit Employee Data Change Request

> **Module:** `ssi_hr_employee_data_change`
>
> **Model:** `employee_data_change_request`
>
> **Menu:** Human Resource > Employees > Employee Data Change Request
>
> **Actor:** user in group _Employee Data Change Request — User_
>
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Draft**.
- **Access:** User is in group _Employee Data Change Request — User_.

## Flow

1. Open the **Human Resource > Employees > Employee Data Change Request** menu.
2. Find and open the record to edit.
3. Change **Employee** (and, while in **Draft**, **Date**) as needed. The **Previous**
   values are taken again from the new employee when the record is saved.
4. Change the **New** values in the **Personal Data** tab, and the lines of the
   **Children** and **Academic History** tabs, as needed.
5. Click **Save**.

## Post-Condition

- The record is updated with the new values.
