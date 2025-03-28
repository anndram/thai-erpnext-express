# ERPNext Express © 2024
# Author:  Anndream
# Company: Level Up Marketing & Software Development Services
# Licence: Please refer to LICENSE file


import re

import frappe
from frappe import _
from frappe.utils import cint, get_request_session, now, markdown

from frappe.desk.doctype.notification_settings.notification_settings import (
    is_notifications_enabled
)

from thai_express import __version__
from .common import log_error, parse_json_if_valid
from .settings import *


## Hooks
def auto_check_for_update():
    if cint(settings().auto_check_for_update):
        check_for_update()


## Self
def check_for_update():
    try:
        http = get_request_session()
        request = http.request(
            "GET",
            "https://api.github.com/repos/kid1194/erpnext_expenses/releases/latest"
        )
        status_code = request.status_code
        data = request.json()
    except Exception as exc:
        log_error(exc)
        return 0
    
    if status_code != 200 and status_code != 201:
        return 0
    
    data = parse_json_if_valid(data)
    
    if (
        not data or not isinstance(data, dict) or
        not data.get("tag_name") or not data.get("body")
    ):
        return 0
    
    latest_version = re.sub("[^0-9\.]", "", str(data.get("tag_name")))
    has_update = 1 if compare_versions(latest_version, __version__) > 0 else 0
    
    doc = settings(True)
    doc.has_update = has_update
    doc.latest_check = now()
    
    if has_update:
        doc.latest_version = latest_version
        if cint(doc.send_update_notification):
            enqueue_send_notification(
                latest_version,
                doc.update_notification_sender,
                [v.user for v in doc.update_notification_receivers],
                markdown(response.get("body"))
            )
    
    doc.save(ignore_permissions=True)
    return 1


## Self
def compare_versions(verA, verB):
    verA = verA.split(".")
    lenA = len(verA)
    verB = verB.split(".")
    lenB = len(verB)
    
    if lenA > lenB:
        for i in range(lenB, lenA):
            verB.append(0)
    elif lenA < lenB:
        for i in range(lenA, lenB):
            verA.append(0)
    
    for a, b in zip(verA, verB):
        d = cint(a) - cint(b)
        if d == 0:
            continue
        return 1 if d > 0 else -1
    
    return 0


## Self
def enqueue_send_notification(version, sender, receivers, message):
    frappe.enqueue(
        "expenses.utils.update.send_notification",
        job_name=f"expenses-send-notification-{version}",
        is_async=True,
        version=version,
        sender=sender,
        receivers=receivers,
        message=message
    )


## Self
def send_notification(version, sender, receivers, message):
    for receiver in receivers:
        if is_notifications_enabled(user):
            (frappe.new_doc("Notification Log")
                .update({
                    "document_type": _SETTINGS,
                    "document_name": _SETTINGS,
                    "from_user": sender,
                    "for_user": receiver,
                    "subject": "Expenses: A New Version Is Available",
                    "type": "Alert",
                    "email_content": f"<p><h2>Version {version}</h2></p>{message}",
                })
                .insert(ignore_permissions=True, ignore_mandatory=True))