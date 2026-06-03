/* ============================================================
   BhartERP — App Switcher + Navbar Enhancements
   Injects a module switcher into ERPNext navbar so users can
   jump to CRM, Helpdesk, HRMS and Drive with one click.
   All apps must be installed on the same site.
   Paisape Techfin Private Limited
   ============================================================ */

(function () {
  'use strict';

  /* ── App definitions ─────────────────────────────────────── */
  var BHARTERP_APPS = [
    {
      id:    'erpnext',
      label: 'ERPNext',
      sub:   'Accounts · GST · Inventory',
      url:   '/app',
      color: '#E8641A',
      icon:  '<svg width="18" height="18" viewBox="0 0 40 40" fill="none"><path d="M20 4L36 20L20 36L4 20Z" fill="none" stroke="rgba(232,100,26,.4)" stroke-width="1.5"/><circle cx="20" cy="20" r="5" fill="#E8641A"/><circle cx="20" cy="6" r="2" fill="rgba(232,100,26,.6)"/><circle cx="34" cy="20" r="2" fill="rgba(232,100,26,.6)"/><circle cx="20" cy="34" r="2" fill="rgba(232,100,26,.6)"/><circle cx="6" cy="20" r="2" fill="rgba(232,100,26,.6)"/></svg>',
    },
    {
      id:    'crm',
      label: 'CRM',
      sub:   'Leads · Deals · Pipeline',
      url:   '/crm',
      color: '#4B91E2',
      icon:  '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#4B91E2" stroke-width="1.8" stroke-linecap="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>',
    },
    {
      id:    'helpdesk',
      label: 'Helpdesk',
      sub:   'Tickets · SLA · KB',
      url:   '/helpdesk',
      color: '#8B5CF6',
      icon:  '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#8B5CF6" stroke-width="1.8" stroke-linecap="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>',
    },
    {
      id:    'hrms',
      label: 'HR',
      sub:   'Employees · Payroll · Leaves',
      url:   '/hrms',
      color: '#1A6B4A',
      icon:  '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#1A6B4A" stroke-width="1.8" stroke-linecap="round"><rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/></svg>',
    },
    {
      id:    'drive',
      label: 'Drive',
      sub:   'Files · Documents',
      url:   '/drive',
      color: '#D4A843',
      icon:  '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#D4A843" stroke-width="1.8" stroke-linecap="round"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/></svg>',
    },
  ];

  /* ── Detect which app is currently active ────────────────── */
  function getActiveApp() {
    var path = window.location.pathname;
    if (path.startsWith('/crm'))      return 'crm';
    if (path.startsWith('/helpdesk')) return 'helpdesk';
    if (path.startsWith('/hrms'))     return 'hrms';
    if (path.startsWith('/drive'))    return 'drive';
    return 'erpnext';
  }

  /* ── Detect which apps are actually installed ─────────────── */
  function getInstalledApps() {
    var installed = (frappe && frappe.boot && frappe.boot.installed_apps) || [];
    return {
      crm:       installed.indexOf('crm') !== -1,
      helpdesk:  installed.indexOf('helpdesk') !== -1,
      hrms:      installed.indexOf('hrms') !== -1,
      drive:     installed.indexOf('drive') !== -1,
      erpnext:   true,
    };
  }

  /* ── Build the switcher HTML ──────────────────────────────── */
  function buildSwitcher() {
    var active    = getActiveApp();
    var installed = getInstalledApps();
    var activeApp = BHARTERP_APPS.find(function(a) { return a.id === active; });

    var btn = document.createElement('div');
    btn.id  = 'bt-app-btn';
    btn.innerHTML =
      '<div id="bt-app-trigger" title="Switch App">' +
        '<span id="bt-app-trigger-icon">' + (activeApp ? activeApp.icon : BHARTERP_APPS[0].icon) + '</span>' +
        '<span id="bt-app-trigger-label">' + (activeApp ? activeApp.label : 'BhartERP') + '</span>' +
        '<svg id="bt-chevron" width="10" height="10" viewBox="0 0 10 10" fill="none"><path d="M2 3.5L5 6.5L8 3.5" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"/></svg>' +
      '</div>' +
      '<div id="bt-app-dropdown">' +
        '<div class="bt-dd-header">BhartERP Suite</div>' +
        BHARTERP_APPS.filter(function(a) {
          return a.id === 'erpnext' || installed[a.id];
        }).map(function(app) {
          var isActive = app.id === active;
          return (
            '<a class="bt-dd-item' + (isActive ? ' bt-dd-active' : '') + '" href="' + app.url + '">' +
              '<span class="bt-dd-icon" style="background:' + app.color + '18;border:1px solid ' + app.color + '30">' +
                app.icon +
              '</span>' +
              '<span class="bt-dd-text">' +
                '<span class="bt-dd-name">' + app.label + '</span>' +
                '<span class="bt-dd-sub">' + app.sub + '</span>' +
              '</span>' +
              (isActive ? '<svg class="bt-dd-check" width="14" height="14" viewBox="0 0 14 14" fill="none"><path d="M2.5 7L5.5 10L11.5 4" stroke="#E8641A" stroke-width="1.5" stroke-linecap="round"/></svg>' : '') +
            '</a>'
          );
        }).join('') +
        '<div class="bt-dd-footer">Paisape Techfin · erp.paisape.org</div>' +
      '</div>';

    return btn;
  }

  /* ── Inject CSS ───────────────────────────────────────────── */
  function injectStyles() {
    var style = document.createElement('style');
    style.textContent = [
      '#bt-app-btn{position:relative;display:flex;align-items:center;margin-right:4px}',
      '#bt-app-trigger{display:flex;align-items:center;gap:6px;padding:5px 10px;',
        'border-radius:7px;cursor:pointer;color:rgba(240,237,232,.85);',
        'border:1px solid rgba(255,255,255,.08);transition:all .15s;',
        'font-size:13px;font-family:"DM Sans",sans-serif;font-weight:500;',
        'background:transparent;user-select:none;}',
      '#bt-app-trigger:hover{background:rgba(255,255,255,.08);color:#F0EDE8}',
      '#bt-chevron{color:rgba(240,237,232,.5);transition:transform .15s}',
      '#bt-app-btn.open #bt-chevron{transform:rotate(180deg)}',
      '#bt-app-dropdown{',
        'position:absolute;top:calc(100% + 8px);left:0;',
        'background:#1A1A1C;border:0.5px solid rgba(255,255,255,.12);',
        'border-radius:12px;padding:6px;min-width:240px;',
        'box-shadow:0 16px 40px rgba(0,0,0,.5);',
        'opacity:0;visibility:hidden;transform:translateY(-6px);',
        'transition:all .18s;z-index:9999;}',
      '#bt-app-btn.open #bt-app-dropdown{opacity:1;visibility:visible;transform:translateY(0)}',
      '.bt-dd-header{font-size:9px;font-weight:700;text-transform:uppercase;',
        'letter-spacing:.1em;color:rgba(255,255,255,.3);padding:4px 8px 8px;',
        'border-bottom:0.5px solid rgba(255,255,255,.06);margin-bottom:4px}',
      '.bt-dd-item{display:flex;align-items:center;gap:10px;padding:8px 8px;',
        'border-radius:8px;text-decoration:none;transition:background .12s;',
        'color:#F0EDE8;}',
      '.bt-dd-item:hover{background:rgba(255,255,255,.06)}',
      '.bt-dd-active{background:rgba(232,100,26,.08) !important}',
      '.bt-dd-icon{width:34px;height:34px;border-radius:8px;',
        'display:flex;align-items:center;justify-content:center;flex-shrink:0}',
      '.bt-dd-text{display:flex;flex-direction:column;gap:1px;flex:1}',
      '.bt-dd-name{font-size:13px;font-weight:500;color:#F0EDE8;line-height:1.2}',
      '.bt-dd-sub{font-size:10px;color:rgba(240,237,232,.4);line-height:1.2}',
      '.bt-dd-check{flex-shrink:0}',
      '.bt-dd-footer{font-size:9px;color:rgba(255,255,255,.2);',
        'padding:8px 8px 4px;border-top:0.5px solid rgba(255,255,255,.06);margin-top:4px}',
    ].join('');
    document.head.appendChild(style);
  }

  /* ── Mount into ERPNext navbar ────────────────────────────── */
  function mount() {
    /* Already mounted */
    if (document.getElementById('bt-app-btn')) return;

    /* ERPNext navbar brand area */
    var navbar = document.querySelector('.navbar-header') ||
                 document.querySelector('.navbar .container') ||
                 document.querySelector('header .navbar');
    if (!navbar) return;

    injectStyles();

    var switcher = buildSwitcher();
    var brand = navbar.querySelector('.navbar-brand');
    if (brand && brand.nextSibling) {
      navbar.insertBefore(switcher, brand.nextSibling);
    } else {
      navbar.appendChild(switcher);
    }

    /* Toggle dropdown */
    var trigger = switcher.querySelector('#bt-app-trigger');
    trigger.addEventListener('click', function(e) {
      e.stopPropagation();
      switcher.classList.toggle('open');
    });

    /* Close on outside click */
    document.addEventListener('click', function() {
      switcher.classList.remove('open');
    });

    /* Close on Escape */
    document.addEventListener('keydown', function(e) {
      if (e.key === 'Escape') switcher.classList.remove('open');
    });
  }

  /* ── Wait for ERPNext desk to load ───────────────────────── */
  function init() {
    /* frappe.ui.toolbar fires after desk is ready */
    if (window.frappe && frappe.after_ajax) {
      frappe.after_ajax(function() {
        setTimeout(mount, 300);
      });
    }

    /* Fallback: observe DOM for navbar */
    var observer = new MutationObserver(function() {
      var navbar = document.querySelector('.navbar-header') ||
                   document.querySelector('.navbar .container');
      if (navbar && !document.getElementById('bt-app-btn')) {
        mount();
      }
    });
    observer.observe(document.body, { childList: true, subtree: true });

    /* Final fallback */
    setTimeout(mount, 1500);
    setTimeout(mount, 3000);
  }

  /* ── Boot ─────────────────────────────────────────────────── */
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

})();
