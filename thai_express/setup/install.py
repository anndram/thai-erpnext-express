# ERPNext Express © 2024
# Author:  Anndream
# Company: Level Up Marketing & Software Development Services
# Licence: Please refer to LICENSE file


import frappe
from frappe.utils import now
from frappe.utils.user import get_system_managers

from thai_express import __version__
from thai_express.utils.settings import settings


def after_install():
    if (managers := get_system_managers(only_name=True)):
        if "Administrator" in managers:
            sender = "Administrator"
        else:
            sender = managers[0]
        
        doc = settings(True)
        doc.update_notification_sender = sender
        
        if doc.update_notification_receivers:
            doc.update_notification_receivers.clear()
        
        for manager in managers:
            doc.append(
                "update_notification_receivers",
                {"user": manager}
            )
        
        doc.latest_version = __version__
        doc.latest_check = now()
        doc.has_update = 0
        
        doc.save(ignore_permissions=True)