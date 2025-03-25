# ERPNext Express © 2024
# Author:  Anndream
# Company: Level Up Marketing & Software Development Services
# Licence: Please refer to LICENSE file


from frappe.model.document import Document

from thai_express.utils import clear_document_cache


class ExpensesSettings(Document):
    def before_save(self):
        clear_document_cache(self.doctype)