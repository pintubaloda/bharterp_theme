"""
BhartERP Theme — Installation & Uninstallation
"""
import frappe
from frappe import _


def after_install():
    _set_system_settings()
    _create_roles()
    _create_custom_fields()

    _create_notifications()
    _create_client_scripts()
    _create_server_scripts()
    _create_reports()
    _create_dashboard()
    print("[BhartERP Theme] Installation complete.")


def _set_system_settings():
    try:
        ss = frappe.get_single("System Settings")
        ss.app_name = "BhartERP"
        ss.footer_powered_by = "Paisape Techfin Private Limited"
        ss.save(ignore_permissions=True)
    except Exception:
        pass

    # Website settings
    try:
        ws = frappe.get_single("Website Settings")
        ws.title = "BhartERP"
        ws.footer_powered_by = "Paisape Techfin Private Limited"
        ws.save(ignore_permissions=True)
    except Exception:
        pass


def _create_roles():
    roles = [
        ("BhartERP Sales User",     "Can create and manage sales transactions"),
        ("BhartERP Purchase User",  "Can create and manage purchase transactions"),
        ("BhartERP Accounts User",  "Full access to accounting modules"),
        ("BhartERP HR Manager",     "HR and payroll management"),
        ("BhartERP Read Only",      "Read-only access to all modules"),
    ]
    for name, desc in roles:
        if not frappe.db.exists("Role", name):
            frappe.get_doc({"doctype": "Role", "role_name": name,
                            "desk_access": 1, "description": desc}).insert()
    frappe.db.commit()


def _create_custom_fields():
    """Add India-specific custom fields to standard doctypes."""
    fields = [
        # Customer
        {"dt": "Customer", "fieldname": "custom_gstin",       "label": "GSTIN",               "fieldtype": "Data",   "insert_after": "tax_id",       "length": 15},
        {"dt": "Customer", "fieldname": "custom_pan",         "label": "PAN",                 "fieldtype": "Data",   "insert_after": "custom_gstin", "length": 10},
        {"dt": "Customer", "fieldname": "custom_business_type","label": "Business Type",      "fieldtype": "Select", "insert_after": "custom_pan",   "options": "\nProprietorship\nPartnership\nPrivate Limited\nPublic Limited\nLLP\nTrust\nSociety"},
        {"dt": "Customer", "fieldname": "custom_credit_days", "label": "Credit Days",         "fieldtype": "Int",    "insert_after": "credit_limit"},
        # Supplier
        {"dt": "Supplier", "fieldname": "custom_gstin",       "label": "GSTIN",               "fieldtype": "Data",   "insert_after": "tax_id",       "length": 15},
        {"dt": "Supplier", "fieldname": "custom_pan",         "label": "PAN",                 "fieldtype": "Data",   "insert_after": "custom_gstin", "length": 10},
        {"dt": "Supplier", "fieldname": "custom_msme_reg_no", "label": "MSME Registration No","fieldtype": "Data",   "insert_after": "custom_pan"},
        {"dt": "Supplier", "fieldname": "custom_msme_category","label": "MSME Category",      "fieldtype": "Select", "insert_after": "custom_msme_reg_no", "options": "\nMicro\nSmall\nMedium"},
        {"dt": "Supplier", "fieldname": "custom_bank_ifsc",   "label": "Bank IFSC",           "fieldtype": "Data",   "insert_after": "custom_msme_category", "length": 11},
        # Item
        {"dt": "Item",     "fieldname": "custom_mrp",         "label": "MRP (₹)",             "fieldtype": "Currency","insert_after": "standard_rate"},
        {"dt": "Item",     "fieldname": "custom_brand",       "label": "Brand",               "fieldtype": "Data",   "insert_after": "custom_mrp"},
        {"dt": "Item",     "fieldname": "custom_country_of_origin","label": "Country of Origin","fieldtype": "Link","insert_after": "custom_brand",  "options": "Country"},
        # Sales Invoice
        {"dt": "Sales Invoice", "fieldname": "custom_lr_number",  "label": "LR Number",       "fieldtype": "Data",   "insert_after": "vehicle_no"},
        {"dt": "Sales Invoice", "fieldname": "custom_is_proforma","label": "Is Proforma",     "fieldtype": "Check",  "insert_after": "is_return"},
        # Employee
        {"dt": "Employee", "fieldname": "custom_aadhaar",     "label": "Aadhaar Number",      "fieldtype": "Data",   "insert_after": "pan_number",   "length": 12},
        {"dt": "Employee", "fieldname": "custom_uan",         "label": "UAN (PF)",            "fieldtype": "Data",   "insert_after": "pf_number",    "length": 12},
        {"dt": "Employee", "fieldname": "custom_esic_ip_no",  "label": "ESIC IP Number",      "fieldtype": "Data",   "insert_after": "esic_number"},
        {"dt": "Employee", "fieldname": "custom_bank_ifsc",   "label": "Bank IFSC",           "fieldtype": "Data",   "insert_after": "bank_name",    "length": 11},
        # Company
        {"dt": "Company",  "fieldname": "custom_cin",         "label": "CIN",                 "fieldtype": "Data",   "insert_after": "company_name"},
        {"dt": "Company",  "fieldname": "custom_tan",         "label": "TAN",                 "fieldtype": "Data",   "insert_after": "custom_cin",   "length": 10},
        {"dt": "Company",  "fieldname": "custom_pf_reg_no",   "label": "PF Registration No",  "fieldtype": "Data",   "insert_after": "custom_tan"},
        {"dt": "Company",  "fieldname": "custom_esic_reg_no", "label": "ESIC Registration No","fieldtype": "Data",   "insert_after": "custom_pf_reg_no"},
        {"dt": "Company",  "fieldname": "custom_pt_reg_no",   "label": "Professional Tax Reg No","fieldtype": "Data","insert_after": "custom_esic_reg_no"},

        # Purchase Invoice — RCM + MSME
        {"dt": "Purchase Invoice", "fieldname": "custom_rcm_applicable",  "label": "RCM Applicable",          "fieldtype": "Check",  "insert_after": "is_return",      "description": "Reverse Charge Mechanism — tax to be paid by buyer"},
        {"dt": "Purchase Invoice", "fieldname": "custom_msme_supplier",   "label": "MSME Supplier",            "fieldtype": "Check",  "insert_after": "custom_rcm_applicable"},
        {"dt": "Purchase Invoice", "fieldname": "custom_msme_due_date",   "label": "MSME 45-day Due Date",     "fieldtype": "Date",   "insert_after": "custom_msme_supplier"},
        # Sales Invoice — SEZ + Composition
        {"dt": "Sales Invoice",    "fieldname": "custom_sez_supply",      "label": "SEZ Supply",               "fieldtype": "Check",  "insert_after": "custom_is_proforma"},
        {"dt": "Sales Invoice",    "fieldname": "custom_export_type",     "label": "Export Type",              "fieldtype": "Select", "insert_after": "custom_sez_supply", "options": "\nWith Payment of Tax\nWithout Payment of Tax"},
        # Customer — additional India fields
        {"dt": "Customer",         "fieldname": "custom_aadhaar",         "label": "Aadhaar (Individual)",     "fieldtype": "Data",   "insert_after": "custom_pan",       "length": 12},
        {"dt": "Customer",         "fieldname": "custom_payment_mode",    "label": "Preferred Payment Mode",   "fieldtype": "Select", "insert_after": "custom_aadhaar",   "options": "\nNEFT\nRTGS\nUPI\nCheque\nDD\nCash"},
        {"dt": "Customer",         "fieldname": "custom_composition",     "label": "Composition Dealer",       "fieldtype": "Check",  "insert_after": "custom_payment_mode"},
        # Quotation — validity
        {"dt": "Quotation",        "fieldname": "custom_validity_days",   "label": "Validity (Days)",          "fieldtype": "Int",    "insert_after": "valid_till",       "default": "30"},
        # Employee — emergency contact
        {"dt": "Employee",         "fieldname": "custom_emergency_name",  "label": "Emergency Contact Name",   "fieldtype": "Data",   "insert_after": "custom_bank_ifsc", "length": 140},
        {"dt": "Employee",         "fieldname": "custom_emergency_phone", "label": "Emergency Contact Phone",  "fieldtype": "Data",   "insert_after": "custom_emergency_name", "length": 15},

        # Asset
        {"dt": "Asset",           "fieldname": "custom_insurance_no",    "label": "Insurance Policy No",      "fieldtype": "Data",   "insert_after": "location"},
        {"dt": "Asset",           "fieldname": "custom_insurance_expiry","label": "Insurance Expiry",         "fieldtype": "Date",   "insert_after": "custom_insurance_no"},
        {"dt": "Asset",           "fieldname": "custom_vendor_amc",      "label": "AMC Vendor",               "fieldtype": "Link",   "insert_after": "custom_insurance_expiry", "options": "Supplier"},
        # Lead
        {"dt": "Lead",            "fieldname": "custom_gstin",           "label": "GSTIN",                    "fieldtype": "Data",   "insert_after": "company_name", "length": 15},
        {"dt": "Lead",            "fieldname": "custom_annual_turnover", "label": "Annual Turnover (₹)",      "fieldtype": "Currency","insert_after": "annual_revenue"},
        # Issue / Support
        {"dt": "Issue",           "fieldname": "custom_sla_breached",    "label": "SLA Breached",             "fieldtype": "Check",  "insert_after": "status"},
        {"dt": "Issue",           "fieldname": "custom_first_response",  "label": "First Response Time",      "fieldtype": "Duration","insert_after": "custom_sla_breached"},
        # POS Invoice
        {"dt": "POS Invoice",     "fieldname": "custom_upi_ref",         "label": "UPI Reference",            "fieldtype": "Data",   "insert_after": "remarks"},
        # Purchase Invoice additional
        {"dt": "Purchase Invoice","fieldname": "custom_vendor_invoice_no","label": "Vendor Invoice No",       "fieldtype": "Data",   "insert_after": "bill_no"},
        {"dt": "Purchase Invoice","fieldname": "custom_vendor_invoice_date","label": "Vendor Invoice Date",   "fieldtype": "Date",   "insert_after": "custom_vendor_invoice_no"},
        # Stock Entry
        {"dt": "Stock Entry",      "fieldname": "custom_gate_pass_no",    "label": "Gate Pass No.",            "fieldtype": "Data",   "insert_after": "title"},
        {"dt": "Stock Entry",      "fieldname": "custom_reason",          "label": "Reason for Transfer",      "fieldtype": "Small Text", "insert_after": "custom_gate_pass_no"},
        # Company — additional
        {"dt": "Company",          "fieldname": "custom_pan",             "label": "Company PAN",              "fieldtype": "Data",   "insert_after": "custom_cin",       "length": 10},
        {"dt": "Company",          "fieldname": "custom_roc_no",          "label": "ROC Filing No.",           "fieldtype": "Data",   "insert_after": "custom_pan"},
    ]
    for f in fields:
        if not frappe.db.exists("Custom Field", f"{f['dt']}-{f['fieldname']}"):
            cf = frappe.get_doc({"doctype": "Custom Field", "module": "BhartERP Theme", **f})
            cf.insert(ignore_permissions=True)
    frappe.db.commit()
    print("[BhartERP Theme] Custom fields created.")



def _create_notifications():
    """Create ERPNext Notification documents for all 7 alerts."""
    import os, json
    notif_dir = os.path.join(os.path.dirname(__file__), 'notification')
    if not os.path.exists(notif_dir):
        return
    for fname in os.listdir(notif_dir):
        if not fname.endswith('.json'): continue
        with open(os.path.join(notif_dir, fname)) as f:
            data = json.load(f)
        name = data.get("name")
        if not name: continue
        if not frappe.db.exists("Notification", name):
            try:
                doc = frappe.get_doc({"doctype": "Notification", **data})
                doc.insert(ignore_permissions=True)
            except Exception as e:
                frappe.log_error(f"Notification install error: {name}: {e}")
    frappe.db.commit()
    print("[BhartERP Theme] Notifications created.")


def _create_client_scripts():
    """Install GSTIN validation client scripts."""
    import os, json
    scripts_dir = os.path.join(os.path.dirname(__file__), 'client_script')
    if not os.path.exists(scripts_dir):
        return
    for fname in os.listdir(scripts_dir):
        if not fname.endswith('.json'): continue
        with open(os.path.join(scripts_dir, fname)) as f:
            data = json.load(f)
        name = data.get("name")
        if not name: continue
        if not frappe.db.exists("Client Script", name):
            try:
                doc = frappe.get_doc({"doctype": "Client Script", **data})
                doc.insert(ignore_permissions=True)
            except Exception as e:
                frappe.log_error(f"Client Script error: {name}: {e}")
    frappe.db.commit()
    print("[BhartERP Theme] Client scripts created.")


def _create_server_scripts():
    """Install server scripts for reorder alert and MSME alert."""
    import os, json
    scripts_dir = os.path.join(os.path.dirname(__file__), 'server_script')
    if not os.path.exists(scripts_dir):
        return
    for fname in os.listdir(scripts_dir):
        if not fname.endswith('.json'): continue
        with open(os.path.join(scripts_dir, fname)) as f:
            data = json.load(f)
        name = data.get("name")
        if not name: continue
        if not frappe.db.exists("Server Script", name):
            try:
                doc = frappe.get_doc({"doctype": "Server Script", **data})
                doc.insert(ignore_permissions=True)
            except Exception as e:
                frappe.log_error(f"Server Script error: {name}: {e}")
    frappe.db.commit()
    print("[BhartERP Theme] Server scripts created.")


def _create_reports():
    """Install custom Script Reports."""
    import os, json
    reports_dir = os.path.join(os.path.dirname(__file__), 'custom_reports')
    if not os.path.exists(reports_dir):
        return
    for report_folder in os.listdir(reports_dir):
        folder_path = os.path.join(reports_dir, report_folder)
        if not os.path.isdir(folder_path): continue
        json_file = os.path.join(folder_path, f"{report_folder}.json")
        py_file   = os.path.join(folder_path, f"{report_folder}.py")
        if not os.path.exists(json_file): continue
        with open(json_file) as f:
            data = json.load(f)
        name = data.get("name")
        if not name: continue
        if not frappe.db.exists("Report", name):
            try:
                # Read script content
                script = ""
                if os.path.exists(py_file):
                    with open(py_file) as f: script = f.read()
                doc = frappe.get_doc({
                    "doctype": "Report",
                    "module": "BhartERP Theme",
                    "is_standard": "No",
                    "script": script,
                    **data,
                })
                doc.insert(ignore_permissions=True)
            except Exception as e:
                frappe.log_error(f"Report install error: {name}: {e}")
    frappe.db.commit()
    print("[BhartERP Theme] Custom reports created.")


def _create_dashboard():
    """Create BhartERP Dashboard with KPI cards and charts."""
    try:
        if frappe.db.exists("Dashboard", "BhartERP Dashboard"):
            return

        # Number cards
        import json as _json
        cards_config = [
            ("BhartERP Unpaid Invoices",  "Sales Invoice",  _json.dumps({"docstatus": 1, "outstanding_amount": [">", 0]}), "Count", "#E8641A"),
            ("BhartERP Overdue Invoices", "Sales Invoice",  _json.dumps({"docstatus": 1, "status": "Overdue"}), "Count", "#991B1B"),
            ("BhartERP Open POs",         "Purchase Order", _json.dumps({"docstatus": 1, "status": ["in", ["To Receive and Bill","To Bill","To Receive"]]}), "Count", "#1A6B4A"),
            ("BhartERP Active Employees", "Employee",       _json.dumps({"status": "Active"}), "Count", "#4B91E2"),
            ("BhartERP Open Support",     "Issue",          _json.dumps({"status": "Open"}), "Count", "#8B5CF6"),
            ("BhartERP Open Leads",       "Lead",           _json.dumps({"status": ["not in", ["Converted","Do Not Contact"]]}), "Count", "#D4A843"),
        ]

        card_names = []
        for card_name, doctype, filters, func, color in cards_config:
            if not frappe.db.exists("Number Card", card_name):
                try:
                    card = frappe.get_doc({
                        "doctype": "Number Card",
                        "name": card_name,
                        "label": card_name.replace("BhartERP ", ""),
                        "document_type": doctype,
                        "filters_json": filters,
                        "function": func,
                        "color": color,
                        "module": "BhartERP Theme",
                        "is_public": 1,
                    })
                    card.insert(ignore_permissions=True)
                    card_names.append(card_name)
                except Exception as e:
                    frappe.log_error(f"Number Card error: {card_name}: {e}")

        # Dashboard
        dashboard = frappe.get_doc({
            "doctype": "Dashboard",
            "name": "BhartERP Dashboard",
            "dashboard_name": "BhartERP",
            "module": "BhartERP Theme",
            "is_default": 0,
            "cards": [{"card": n} for n in card_names],
        })
        dashboard.insert(ignore_permissions=True)
        frappe.db.commit()
        print("[BhartERP Theme] Dashboard created.")
    except Exception as e:
        frappe.log_error(f"Dashboard creation error: {e}")

def before_uninstall():
    # Remove all items added by this app
    for doctype in ["Custom Field", "Notification", "Client Script",
                    "Server Script", "Report", "Number Card", "Dashboard"]:
        try:
            frappe.db.delete(doctype, {"module": "BhartERP Theme"})
        except Exception:
            pass
    frappe.db.commit()
    print("[BhartERP Theme] Uninstalled cleanly.")
