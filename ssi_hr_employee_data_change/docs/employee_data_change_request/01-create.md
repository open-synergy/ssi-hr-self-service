# Create Employee Data Change Request

> **Module:** `ssi_hr_employee_data_change`
>
> **Model:** `employee_data_change_request`
>
> **Menu:** Human Resource > Employees > Employee Data Change Request
>
> **Actor:** user in group _Employee Data Change Request — User_
>
> **State:** `—` → `draft`

## Pre-Condition

- **Config:** An active `policy.template` for this model exists — see the _Standard_
  `policy.template` shipped with this module. It grants `confirm_ok` (state `draft`) and
  `done_ok` (state `confirm`) to group _Employee Data Change Request — User_, and
  `cancel_ok`, `restart_ok`, `restart_approval_ok`, and `manual_number_ok` to group
  _Employee Data Change Request — Validator_.
- **Config:** An active `approval.template` for this model exists — see the _Standard_
  `approval.template`, which defines a single sequential level approved by group
  _Employee Data Change Request — Validator_ (`mixin.multiple_approval`).
- **Config:** An active `sequence.template` for this model exists — see the _Standard_
  `sequence.template` shipped with this module (`mixin.sequence`).
- **Data:** The **Employee** to select has an `hr.employee` record. The employee needs a
  **Private Address** before the request can be confirmed (see `04-confirm`).
- **Access:** User is in group _Employee Data Change Request — User_.

## Flow

1. Open the **Human Resource > Employees > Employee Data Change Request** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the required fields:
   - **Employee** _(required)_: Automatically filled from the current user's linked
     employee record, if any. Change if needed.
   - **Department**, **Manager**, **Job Position**: Automatically filled from
     **Employee**. Read-only.
4. Open the **Personal Data** tab. Fill in only the fields to change in the **New**
   group; leave a field empty to keep its current value. The **Previous** group shows
   the current value of the employee after the record is saved.
5. Optionally, open the **Children** tab and add one line per child to add. Fill in the
   line fields:
   - **Name** _(required)_: Full name of the child.
   - **Birthdate**: Birth date of the child.
   - **Gender**: Gender of the child.
6. Optionally, open the **Academic History** tab and add one line per education to add.
   Fill in the line fields:
   - **Institution** _(required)_: Name of the school or university.
   - **Education Level**: Level of the education.
   - **Field of Study**: Field of study.
   - **Date Start** _(required)_: Date the study started.
   - **Date End**: Date the study ended.
   - **Diploma Number**: Number of the diploma.
   - **Latest GPA**: Latest grade point average.
7. Click **Save**.

## Post-Condition

- A new data change request record is created in **Draft** status.
- The **Previous** group of the **Personal Data** tab shows the values of the employee
  at the time of saving.
- The document number stays **/** until the record transitions to **Done** — unless the
  actor has _Can Input Manual Document Number_ access.
