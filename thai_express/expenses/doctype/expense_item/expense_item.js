/*
*  ERPNext Expenses © 2022
*  Author:  Ameen Ahmed
*  Company: Level Up Marketing & Software Development Services
*  Licence: Please refer to LICENSE file
*/


frappe.ui.form.on('Expense Item', {
    setup: function(frm) {
        frappe.Expenses();
        frappe.E.form(frm);
        frm.X = {
            companies: frappe.E.uniqueArray(),
        };
    },
    onload: function(frm) {
        frappe.E.setFieldProperties('expense_accounts.account', {reqd: 0, bold: 0});
        frappe.E.setFieldsProperty(
            'expense_section cost min_cost max_cost expense_column qty min_qty max_qty',
            'hidden', 0, 'expense_accounts'
        );
        frappe.E.setFieldsProperty('cost qty', 'in_list_view', 1, 'expense_accounts');
        
        frm.set_query('expense_type', {query: frappe.E.path('search_types')});
        frm.set_query('company', 'expense_accounts', function(doc, cdt, cdn) {
            let filters = {is_group: 0};
            if (frm.X.companies.length) {
                filters.name = ['not in', frm.X.companies.all];
            }
            return {filters};
        });
        frm.set_query('account', 'expense_accounts', function(doc, cdt, cdn) {
            return {filters: {
                is_group: 0,
                root_type: 'Expense',
                company: locals[cdt][cdn].company,
            }};
        });
        
        frm.add_fetch('account', 'account_currency', 'currency', 'Expense Account');
        
        if (!frm.is_new()) {
            frappe.E.each(frm.doc.expense_accounts, function(v) {
                frm.X.companies.push(v.company, v.name);
            });
        }
    },
});

frappe.ui.form.on('Expense Account', {
    before_expense_accounts_remove: function(frm, cdt, cdn) {
        frm.X.companies.del(cdn, 1);
    },
    company: function(frm, cdt, cdn) {
        let row = locals[cdt][cdn];
        if (!row.company) {
            frm.X.companies.del(cdn, 1);
            frappe.E.setDocValue(row, 'account', '');
            return;
        }
        if (!frm.X.companies.has(row.company)) {
            frm.X.companies.push(row.company, cdn);
            return;
        }
        frappe.E.error(
            'The expense account for {0} has already been set',
            [row.company]
        );
        frappe.E.setDocValue(row, 'company', '');
    },
    account: function(frm, cdt, cdn) {
        let row = locals[cdt][cdn];
        if (!row.account || row.company) return;
        frappe.E.error('Please select a company first');
        frappe.E.setDocValue(row, 'account', '');
    },
    cost: function(frm, cdt, cdn) {
        let row = locals[cdt][cdn];
        if (!flt(row.cost)) return;
        if (flt(row.cost) < 0) {
            frappe.E.setDocValue(row, 'cost', 0);
            return;
        }
        frappe.E.refreshRowField('expense_accounts', cdn, 'min_cost', 'max_cost');
    },
    min_cost: function(frm, cdt, cdn) {
        let row = locals[cdt][cdn],
        val = flt(row.min_cost);
        if (!val) return;
        let max = flt(row.max_cost);
        if (val < 0 || flt(row.cost) > 0 || (max > 0 && val >= max)) {
            frappe.E.setDocValue(row, 'min_cost', 0);
        }
    },
    max_cost: function(frm, cdt, cdn) {
        let row = locals[cdt][cdn],
        val = flt(row.max_cost);
        if (!val) return;
        let min = flt(row.min_cost);
        if (val < 0 || flt(row.cost) > 0 || (min > 0 && val <= min)) {
            frappe.E.setDocValue(row, 'max_cost', 0);
        }
    },
    qty: function(frm, cdt, cdn) {
        let row = locals[cdt][cdn];
        if (!flt(row.qty)) return;
        if (flt(row.qty) < 0) {
            frappe.E.setDocValue(row, 'qty', 0);
            return;
        }
        frappe.E.refreshRowField('expense_accounts', cdn, 'min_qty', 'max_qty');
    },
    min_qty: function(frm, cdt, cdn) {
        let row = locals[cdt][cdn],
        val = flt(row.min_qty);
        if (!val) return;
        let max = flt(row.max_qty);
        if (val < 0 || flt(row.qty) > 0 || (max > 0 && val >= max)) {
            frappe.E.setDocValue(row, 'min_qty', 0);
        }
    },
    max_qty: function(frm, cdt, cdn) {
       let row = locals[cdt][cdn],
        val = flt(row.max_qty);
        if (!val) return;
        let min = flt(row.min_qty);
        if (val < 0 || flt(row.qty) > 0 || (min > 0 && val <= min)) {
            frappe.E.setDocValue(row, 'max_qty', 0);
        }
    },
});