.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

==============================
Employee Data Change Request
==============================

Lets an employee change his or her own personal data.

* Contact and emergency data are written directly through the self-service
  methods of the ``employee_data_change_request`` model.
* Other personal data (identification number, place and date of birth,
  gender, marital status, spouse, religion, certificate level, photo, new
  children and new academic history) are submitted as a request with
  multiple approval. After the last approval the new values are applied to
  the employee automatically.

The self-service methods are called by an external application through a
service account in the group *Employee Self-Service API*. Every write is
made as the employee, so the audit trail shows the employee and not the
service account.


Work Instruction
================

* `Create Employee Data Change Request <docs/employee_data_change_request/01-create.html>`_
* `Edit Employee Data Change Request <docs/employee_data_change_request/02-edit.html>`_
* `Delete Employee Data Change Request <docs/employee_data_change_request/03-delete.html>`_
* `Confirm Employee Data Change Request <docs/employee_data_change_request/04-confirm.html>`_
* `Approve Employee Data Change Request <docs/employee_data_change_request/05-approve.html>`_
* `Reject Employee Data Change Request <docs/employee_data_change_request/06-reject.html>`_
* `Finish Employee Data Change Request <docs/employee_data_change_request/09-finish.html>`_
* `Cancel Employee Data Change Request <docs/employee_data_change_request/10-cancel.html>`_
* `Restart Employee Data Change Request <docs/employee_data_change_request/12-restart.html>`_
* `Restart Approval Process of Employee Data Change Request <docs/employee_data_change_request/14-restart-approval.html>`_


Installation
============

To install this module, you need to:

1.  Clone the branch 14.0 of the repository https://github.com/open-synergy/ssi-hr-self-service
2.  Add the path to this repository in your configuration (addons-path)
3.  Update the module list (Must be on developer mode)
4.  Go to menu *Apps -> Apps -> Main Apps*
5.  Search For *Employee Data Change Request*
6.  Install the module


Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/open-synergy/ssi-hr-self-service/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smash it by providing detailed and welcomed feedback.


Credits
=======

Contributors
------------

* Andhitia Rama <andhitia.r@gmail.com>

Maintainer
----------

.. image:: https://simetri-sinergi.id/logo.png
   :alt: PT. Simetri Sinergi Indonesia
   :target: https://simetri-sinergi.id

This module is maintained by the PT. Simetri Sinergi Indonesia.
