# ERPNext Express © 2024
# Author:  Anndream
# Company: Level Up Marketing & Software Development Services
# Licence: Please refer to LICENSE file


from frappe import _


def get_data():
    return [
        {
            "module_name": "Thai Express",
            "category": "Modules",
            "color": "blue",
            "icon": "octicon octicon-note",
            "type": "module",
            "label": _("Thai Expenses"),
            "description": _("Thai Express")
        }
    ]