# ERPNext Express © 2024
# Author:  Anndream
# Company: Level Up Marketing & Software Development Services
# Licence: Please refer to LICENSE file


from . import __version__ as app_version


app_name = "thai_express"
app_title = "Thai Express"
app_publisher = "Anndream"
app_description = "An expenses management module for ERPNext."
app_icon = "octicon octicon-note"
app_color = "blue"
app_email = "anndream.com@gmail.com"
app_license = "MIT"


doctype_js = {
    "Expenses Settings": "public/js/expenses.bundle.js",
    "Expense Type": "public/js/expenses.bundle.js",
    "Expense Item": "public/js/expenses.bundle.js",
    "Expense": "public/js/expenses.bundle.js",
    "Expenses Request": "public/js/expenses.bundle.js",
    "Expenses Entry": "public/js/expenses.bundle.js",
}


doctype_list_js = {
    "Expense Type": "public/js/expenses.bundle.js",
    "Expense": "public/js/expenses.bundle.js",
    "Expenses Request": "public/js/expenses.bundle.js",
}


after_install = "thai_express.setup.install.after_install"
after_uninstall = "thai_express.setup.uninstall.after_uninstall"


fixtures = [
    "Role",
    "Workflow",
    "Workflow State",
    "Workflow Action Master"
]


scheduler_events = {
    "daily": [
        "thai_express.utils.update.auto_check_for_update"
    ]
}


treeviews = [
    "Expense Type"
]