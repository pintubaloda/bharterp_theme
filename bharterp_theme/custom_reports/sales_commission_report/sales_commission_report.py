import frappe
from frappe import _

def execute(filters=None):
    filters = filters or {}
    company = filters.get("company") or frappe.defaults.get_global_default("company")
    from_date = filters.get("from_date")
    to_date   = filters.get("to_date")
    columns = [
        {"label": _("Sales Partner"),     "fieldname": "sales_partner",    "fieldtype": "Link",     "options": "Sales Partner", "width": 150},
        {"label": _("Commission Rate %"), "fieldname": "commission_rate",   "fieldtype": "Float",    "width": 120},
        {"label": _("Invoice Count"),     "fieldname": "invoice_count",     "fieldtype": "Int",      "width": 100},
        {"label": _("Total Sales (₹)"),   "fieldname": "total_sales",       "fieldtype": "Currency", "width": 140},
        {"label": _("Commission (₹)"),    "fieldname": "total_commission",  "fieldtype": "Currency", "width": 140},
        {"label": _("Paid Commission"),   "fieldname": "paid_commission",   "fieldtype": "Currency", "width": 140},
        {"label": _("Pending (₹)"),       "fieldname": "pending_commission","fieldtype": "Currency", "width": 140},
    ]
    f = {"company": company, "docstatus": 1,
         "sales_partner": ["!=", ""], "sales_partner": ["is", "set"]}
    if from_date: f["posting_date"] = [">=", from_date]
    if to_date:   f["posting_date"] = ["<=", to_date]
    rows = frappe.db.sql("""
        SELECT sales_partner, commission_rate,
               COUNT(name) as invoice_count,
               SUM(grand_total) as total_sales,
               SUM(total_commission) as total_commission
        FROM `tabSales Invoice`
        WHERE company = %(company)s AND docstatus = 1
          AND sales_partner IS NOT NULL AND sales_partner != ''
          %(date_filter)s
        GROUP BY sales_partner, commission_rate
        ORDER BY total_commission DESC
    """, {
        "company": company,
        "date_filter": (f"AND posting_date BETWEEN '{from_date}' AND '{to_date}'"
                        if from_date and to_date else "")
    }, as_dict=True)
    data = []
    for r in rows:
        commission = float(r.total_commission or 0)
        data.append({
            "sales_partner":     r.sales_partner,
            "commission_rate":   float(r.commission_rate or 0),
            "invoice_count":     int(r.invoice_count or 0),
            "total_sales":       float(r.total_sales or 0),
            "total_commission":  commission,
            "paid_commission":   0.0,
            "pending_commission": commission,
        })
    return columns, data
