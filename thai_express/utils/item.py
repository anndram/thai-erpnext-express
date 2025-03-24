# ERPNext Express © 2024
# Author:  Anndream
# Company: Level Up Marketing & Software Development Services
# Licence: Please refer to LICENSE file


import frappe

from .account import get_company_account_data_by_parent
from .common import (
    error,
    get_cache,
    set_cache,
    is_doc_exist,
    get_cached_value
)
from .doctypes import _ITEM, _ITEM_TYPE, _ITEM_ACCOUNTS
from .search import filter_search, prepare_data
from .type import (
    get_types_filter_query,
    get_type_company_account_data
)


## Expense Type
def items_of_expense_type_exists(expense_type):
    return is_doc_exist(_ITEM, {_ITEM_TYPE: expense_type})


## Expense Form
## Expense List
@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def search_items(doctype, txt, searchfield, start, page_len, filters, as_dict=False):
    doc = frappe.qb.DocType(_ITEM)
    qry = (frappe.qb.from_(doc)
        .select(doc.name)
        .where(doc.disabled == 0))
    
    qry = filter_search(doc, qry, _ITEM, txt, doc.name, "name")
    
    type_qry = get_types_filter_query()
    qry = qry.where(doc.expense_type.isin(type_qry))
    
    data = qry.run(as_dict=as_dict)
    
    data = prepare_data(data, _ITEM, "name", txt, as_dict)
    
    return data


## Expense Form
## Expense List
## Expense
@frappe.whitelist(methods=["POST"])
def get_item_company_account_data(item, company):
    if (
        not item or not isinstance(item, str) or
        not company or not isinstance(company, str)
    ):
        return {}
    
    ckey = f"{item}-{company}-accounts-data"
    cache = get_cache(_ITEM, ckey)
    if cache and isinstance(cache, dict):
        return cache
    
    if not is_doc_exist(_ITEM, item):
        return {}
    
    expense_type = get_cached_value(_ITEM, item, _ITEM_TYPE)
    if (data := get_type_company_account_data(expense_type, company)):
        if (item_data := get_company_account_data_by_parent(
            company,
            item,
            _ITEM,
            _ITEM_ACCOUNTS
        )):
            if isinstance(item_data, dict):
                for k, v in item_data.items():
                    if v:
                        data[k] = v;
    
    else:
        account = ""
        currency = ""
        
        if is_doc_exist("Company", company):
            account = get_cached_value("Company", company, "default_expense_account")
        if account and is_doc_exist("Account", account):
            currency = get_cached_value("Account", account, "account_currency")
        
        data = frappe._dict({
            "account": account,
            "currency": currency,
            "cost": 0.0,
            "min_cost": 0.0,
            "max_cost": 0.0,
            "qty": 0.0,
            "min_qty": 0.0,
            "max_qty": 0.0,
        })
    
    set_cache(_ITEM, ckey, data)
    
    return data