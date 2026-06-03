app_name        = "bharterp_theme"
app_title       = "BhartERP Theme"
app_publisher   = "Paisape Techfin Private Limited"
app_description = "Complete branding, print templates, email templates and India-specific customisations for BhartERP"
app_email       = "dev@paisape.org"
app_license     = "Proprietary"
app_version     = "1.0.0"
app_source_link  = "https://github.com/paisape-techfin/bharterp_theme"

after_install   = "bharterp_theme.install.after_install"
before_uninstall = "bharterp_theme.install.before_uninstall"

app_include_css = ["/assets/bharterp_theme/css/bharterp.css"]
app_include_js  = ["/assets/bharterp_theme/js/bharterp.js"]

fixtures = [
    {"dt": "Print Format",    "filters": [["module", "=", "BhartERP Theme"]]},
    {"dt": "Email Template",  "filters": [["module", "=", "BhartERP Theme"]]},
    {"dt": "Custom Field",    "filters": [["module", "=", "BhartERP Theme"]]},
    {"dt": "Client Script",   "filters": [["module", "=", "BhartERP Theme"]]},
    {"dt": "Server Script",   "filters": [["module", "=", "BhartERP Theme"]]},
    {"dt": "Notification",    "filters": [["module", "=", "BhartERP Theme"]]},
    {"dt": "Report",          "filters": [["module", "=", "BhartERP Theme"]]},
    {"dt": "Dashboard",       "filters": [["module", "=", "BhartERP Theme"]]},
    {"dt": "Dashboard Chart", "filters": [["module", "=", "BhartERP Theme"]]},
    {"dt": "Number Card",     "filters": [["module", "=", "BhartERP Theme"]]},
    {"dt": "Workspace",       "filters": [["module", "=", "BhartERP Theme"]]},
    {"dt": "Role",            "filters": [["name", "in", [
        "BhartERP Sales User","BhartERP Purchase User",
        "BhartERP Accounts User","BhartERP HR Manager","BhartERP Read Only"
    ]]]},
]

# Scheduler — GST filing reminder runs monthly
scheduler_events = {
    "monthly": [
        "bharterp_theme.bharterp_theme.server_script.gst_filing_reminder.run_gst_reminder",
    ],
    "daily": [
        "bharterp_theme.bharterp_theme.server_script.msme_payment_alert.run_msme_alert",
    ],
}
