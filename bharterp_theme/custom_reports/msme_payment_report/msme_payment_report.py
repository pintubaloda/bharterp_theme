import frappe
from frappe import _
from frappe.utils import today, date_diff, getdate

def execute(filters=None):
    filters = filters or {}
    company = filters.get("company") or frappe.defaults.get_global_default("company")
    columns = [
        {"label": _("Invoice"),       "fieldname": "name",             "fieldtype": "Link",     "options": "Purchase Invoice", "width": 140},
        {"label": _("Supplier"),      "fieldname": "supplier_name",    "fieldtype": "Data",     "width": 160},
        {"label": _("MSME Category"), "fieldname": "msme_category",    "fieldtype": "Data",     "width": 100},
        {"label": _("MSME Reg No"),   "fieldname": "msme_reg_no",      "fieldtype": "Data",     "width": 120},
        {"label": _("Invoice Date"),  "fieldname": "posting_date",     "fieldtype": "Date",     "width": 100},
        {"label": _("Due Date (45d)"), "fieldname": "msme_due_date",   "fieldtype": "Date",     "width": 110},
        {"label": _("Invoice Amount"),"fieldname": "grand_total",      "fieldtype": "Currency", "width": 120},
        {"label": _("Outstanding"),   "fieldname": "outstanding_amount","fieldtype": "Currency", "width": 120},
        {"label": _("Days Overdue"),  "fieldname": "days_overdue",     "fieldtype": "Int",      "width": 100},
        {"label": _("Status"),        "fieldname": "payment_status",   "fieldtype": "Data",     "width": 110},
    ]
    msme_suppliers = frappe.db.get_all("Supplier",
        filters={"custom_msme_reg_no": ["!=", ""]},
        fields=["name","custom_msme_category","custom_msme_reg_no"])
    if not msme_suppliers:
        return columns, []
    supplier_map = {s.name: s for s in msme_suppliers}
    f = {"supplier": ["in", list(supplier_map.keys())], "docstatus": 1, "company": company}
    if filters.get("from_date"): f["posting_date"] = [">=", filters["from_date"]]
    if filters.get("to_date"):   f["posting_date"] = ["<=", filters["to_date"]]
    invoices = frappe.get_all("Purchase Invoice", filters=f,
        fields=["name","supplier","supplier_name","posting_date",
                "due_date","grand_total","outstanding_amount","custom_msme_due_date"])
    today_d = getdate(today())
    data = []
    for inv in invoices:
        msme_due = inv.custom_msme_due_date or frappe.utils.add_days(inv.posting_date, 45)
        days_over = date_diff(today_d, getdate(msme_due)) if float(inv.outstanding_amount or 0) > 0 else 0
        sup = supplier_map.get(inv.supplier, frappe._dict())
        status = ("✓ Paid" if float(inv.outstanding_amount or 0) <= 0
                  else (f"⚠ {days_over}d Overdue" if days_over > 0 else "Pending"))
        data.append({"name": inv.name, "supplier_name": inv.supplier_name,
                     "msme_category": sup.get("custom_msme_category",""),
                     "msme_reg_no": sup.get("custom_msme_reg_no",""),
                     "posting_date": inv.posting_date, "msme_due_date": msme_due,
                     "grand_total": inv.grand_total, "outstanding_amount": inv.outstanding_amount,
                     "days_overdue": max(days_over, 0), "payment_status": status})
    data.sort(key=lambda x: x["days_overdue"], reverse=True)
    return columns, data
