# ERPNext Express © 2024
# Author:  Anndream
# Company: Level Up Marketing & Software Development Services
# Licence: Please refer to LICENSE file


import frappe


def after_uninstall():
    data = {
        "Role": "Expenses Reviewer",
        "Workflow": "Expenses Request Review",
        "Workflow State": [
            "Draft",
            "Pending",
            "Cancelled",
            "Approved",
            "Rejected",
            "Processed"
        ],
        "Workflow Action Master": [
            "Submit",
            "Cancel",
            "Approve",
            "Reject"
        ],
    }
    for doctype, name in data.items():
        if isinstance(name, list):
            for doc_name in name:
                delete_doc(doctype, doc_name)
        else:
            delete_doc(doctype, name)


def delete_doc(doctype, name):
    frappe.delete_doc(
        doctype,
        name,
        force=True,
        ignore_permissions=True,
        ignore_on_trash=True,
        ignore_missing=True,
        delete_permanently=True
    )