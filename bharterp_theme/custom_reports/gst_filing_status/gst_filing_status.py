import frappe
from frappe import _
from frappe.utils import getdate, get_first_day, get_last_day, today

def execute(filters=None):
    filters = filters or {}
    company = filters.get("company") or frappe.defaults.get_global_default("company")
    columns = [
        {"label": _("Period"),          "fieldname": "period",          "fieldtype": "Data",     "width": 100},
        {"label": _("GSTR-1 Sales"),    "fieldname": "gstr1_sales",     "fieldtype": "Currency", "width": 130},
        {"label": _("GSTR-1 Tax"),      "fieldname": "gstr1_tax",       "fieldtype": "Currency", "width": 120},
        {"label": _("GSTR-1 Invoices"), "fieldname": "gstr1_count",     "fieldtype": "Int",      "width": 110},
        {"label": _("ITC Available"),   "fieldname": "itc_available",   "fieldtype": "Currency", "width": 130},
        {"label": _("Purchase Bills"),  "fieldname": "purchase_count",  "fieldtype": "Int",      "width": 120},
        {"label": _("Net Tax Payable"), "fieldname": "net_tax",         "fieldtype": "Currency", "width": 130},
        {"label": _("Filing Status"),   "fieldname": "status",          "fieldtype": "Data",     "width": 120},
    ]
    from_date = filters.get("from_date") or frappe.utils.add_months(today(), -6)
    to_date   = filters.get("to_date")   or today()
    months = []
    cur = getdate(get_first_day(from_date))
    end = getdate(get_last_day(to_date))
    while cur <= end:
        months.append(cur)
        cur = getdate(frappe.utils.add_months(str(cur), 1))
    data = []
    for m in months:
        m_start = str(get_first_day(m))
        m_end   = str(get_last_day(m))
        period  = m.strftime("%b %Y")
        def safe_sum(doctype, field, extra=None):
            f = {"company": company, "docstatus": 1, "posting_date": ["between", [m_start, m_end]]}
            if extra: f.update(extra)
            try:
                r = frappe.db.get_value(doctype, f, f"sum({field})")
                return float(r or 0)
            except: return 0.0
        def safe_count(doctype, extra=None):
            f = {"company": company, "docstatus": 1, "posting_date": ["between", [m_start, m_end]]}
            if extra: f.update(extra)
            try: return frappe.db.count(doctype, f) or 0
            except: return 0
        sales_total = safe_sum("Sales Invoice", "grand_total")
        sales_tax   = safe_sum("Sales Invoice", "total_taxes_and_charges")
        sales_count = safe_count("Sales Invoice")
        itc         = safe_sum("Purchase Invoice", "total_taxes_and_charges")
        purch_count = safe_count("Purchase Invoice")
        net_tax     = max(0, sales_tax - itc)
        data.append({"period": period, "gstr1_sales": sales_total,
                     "gstr1_tax": sales_tax, "gstr1_count": sales_count,
                     "itc_available": itc, "purchase_count": purch_count,
                     "net_tax": net_tax,
                     "status": "✓ Filed" if not net_tax else "⚠ Pending"})
    return columns, data
