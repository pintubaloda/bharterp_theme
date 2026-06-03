# BhartERP Theme

> Complete branding, India-compliance templates and app switcher for ERPNext — by **Paisape Techfin Private Limited**

[![ERPNext](https://img.shields.io/badge/ERPNext-v15-E8641A)](https://github.com/frappe/erpnext)
[![License](https://img.shields.io/badge/License-MIT-1A6B4A)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10+-blue)](https://python.org)

---

## What it does

`bharterp_theme` is a Frappe app that installs on ERPNext and adds:

- **BhartERP branding** — logo, saffron/jade colors, branded login page
- **App switcher** — one-click access to Frappe CRM, Helpdesk, HRMS and Drive from the ERPNext navbar
- **31 print templates** — GST Tax Invoice, PO, Salary Slip, Form 16, Cheque and more
- **29 email templates** — order confirmation, payment reminders, HR alerts and more
- **7 auto notifications** — payment due, overdue, low stock, order confirmation
- **2 client scripts** — live GSTIN format validation on Customer and Supplier
- **3 server scripts** — reorder level alert, MSME 45-day payment alert, monthly GST filing reminder
- **3 custom reports** — MSME Payment Report, Sales Commission, GST Filing Status
- **BhartERP Dashboard** — 6 KPI cards (unpaid invoices, overdue, open POs, employees, tickets, leads)
- **48 custom fields** — GSTIN, PAN, MSME, UAN, CIN, TAN and more across 13 doctypes
- **5 roles** — Sales User, Purchase User, Accounts User, HR Manager, Read Only

---

## App Switcher

When Frappe CRM, Helpdesk, HRMS and Drive are installed on the same site, the app switcher appears in the ERPNext navbar automatically:

```
erp.paisape.org/app       → ERPNext (Accounts, GST, Inventory)
erp.paisape.org/crm       → Frappe CRM (Leads, Deals, Pipeline)
erp.paisape.org/helpdesk  → Frappe Helpdesk (Tickets, SLA, KB)
erp.paisape.org/hrms      → Frappe HR (Employees, Payroll, Leaves)
erp.paisape.org/drive     → Frappe Drive (Files, Documents)
```

All apps share **one database, one login, one server**. Data is automatically synced — no API or webhooks needed.

---

## Requirements

| Dependency | Version |
|---|---|
| Frappe Framework | v15 |
| ERPNext | v15 |
| India Compliance | v15 (recommended) |
| Python | 3.10+ |

Optional (for app switcher):
- Frappe CRM
- Frappe Helpdesk
- Frappe HRMS
- Frappe Drive

---

## Installation

### Step 1 — Add to your Docker image

Add `bharterp_theme` to your `apps.json` before building:

```json
[
  { "url": "https://github.com/frappe/erpnext",                         "branch": "version-15" },
  { "url": "https://github.com/frappe/payments",                        "branch": "version-15" },
  { "url": "https://github.com/resilient-tech/india-compliance",        "branch": "version-15" },
  { "url": "https://github.com/frappe/hrms",                            "branch": "version-15" },
  { "url": "https://github.com/frappe/crm",                             "branch": "main"       },
  { "url": "https://github.com/frappe/helpdesk",                        "branch": "main"       },
  { "url": "https://github.com/frappe/drive",                           "branch": "main"       },
  { "url": "https://github.com/paisape-techfin/bharterp_theme",         "branch": "main"       }
]
```

### Step 2 — Build Docker image

```bash
cd /opt/frappe_docker

docker build \
  --no-cache \
  --secret id=apps_json,src=apps.json \
  --build-arg=FRAPPE_PATH=https://github.com/frappe/frappe \
  --build-arg=FRAPPE_BRANCH=version-15 \
  --build-arg=PYTHON_VERSION=3.11.9 \
  --build-arg=NODE_VERSION=18.20.2 \
  --tag=paisape-erp:v15-full \
  --file=images/custom/Containerfile .
```

### Step 3 — Install on your site

```bash
docker exec -it erpnext-backend bash

bench --site erp.paisape.org install-app hrms
bench --site erp.paisape.org install-app crm
bench --site erp.paisape.org install-app helpdesk
bench --site erp.paisape.org install-app drive
bench --site erp.paisape.org install-app bharterp_theme
bench --site erp.paisape.org migrate
bench build --app bharterp_theme
```

### Step 4 — Restart

```bash
exit
cd /root/erpnext-custom && docker compose restart
```

---

## Manual Install (without Docker rebuild)

```bash
# Copy app into container
docker cp bharterp_theme/ erpnext-backend:/home/frappe/frappe-bench/apps/bharterp_theme

# Install
docker exec -it erpnext-backend bash -c "
  pip install -e apps/bharterp_theme --break-system-packages &&
  bench --site erp.paisape.org install-app bharterp_theme &&
  bench build --app bharterp_theme &&
  bench --site erp.paisape.org migrate
"

# Restart
cd /root/erpnext-custom && docker compose restart
```

---

## Rollback

```bash
docker exec -it erpnext-backend bash -c "
  bench --site erp.paisape.org uninstall-app bharterp_theme --yes &&
  bench --site erp.paisape.org migrate
"
cd /root/erpnext-custom && docker compose restart
```

---

## What's Included

### Print Templates (31)
Sales: GST Tax Invoice, Bill of Supply, Proforma Invoice, Sales Order, Quotation, Delivery Challan, Packing Slip, Credit Note, Payment Receipt, POS Invoice

Purchase: Purchase Order, Supplier Quotation, RFQ, Purchase Receipt, Debit Note, Material Request, Stock Entry, Landed Cost Voucher

HR & Compliance: Salary Slip, Form 16, Appointment Letter, Job Offer, Gratuity, Loan Agreement, Full & Final Settlement, Expense Claim

Accounts: Journal Entry, Bank Reconciliation, Cheque Print, Work Order, Warranty Claim, Asset Register

### Email Templates (29)
Sales (9), Purchase (3), HR (9), Alerts (8)

### India-specific Custom Fields (48 across 13 doctypes)
Customer (7), Supplier (5), Company (7), Employee (6), Purchase Invoice (5), Sales Invoice (4), Item (3), Asset (3), Lead (2), Issue (2), POS Invoice (1), Quotation (1), Stock Entry (2)

---

## Developed by

**Paisape Techfin Private Limited**
[paisape.org](https://paisape.org) · [dev@paisape.org](mailto:dev@paisape.org)

Built on [Frappe Framework](https://frappeframework.com) and [ERPNext](https://erpnext.com).
