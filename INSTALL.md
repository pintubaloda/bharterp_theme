# BhartERP Theme — Installation Guide

## Prerequisites
- ERPNext v15 running via Docker on your server
- Site: erp.paisape.org

## Step 1 — Copy app to server
```bash
# From your local machine
scp -r bharterp_theme/ root@149.56.47.92:/opt/bharterp_theme/
```

## Step 2 — Copy into Docker container
```bash
docker cp /opt/bharterp_theme/ erpnext-backend:/home/frappe/frappe-bench/apps/bharterp_theme
```

## Step 3 — Install the app
```bash
docker exec -it erpnext-backend bash

# Inside container:
cd /home/frappe/frappe-bench
pip install -e apps/bharterp_theme
bench --site erp.paisape.org install-app bharterp_theme
bench build --app bharterp_theme
bench --site erp.paisape.org migrate
exit
```

## Step 4 — Restart
```bash
docker compose -f /root/erpnext-custom/docker-compose.yml restart
```

## Step 5 — Verify
Open https://erp.paisape.org — you should see BhartERP branding.

## Rollback
```bash
docker exec -it erpnext-backend bash -c \
  "bench --site erp.paisape.org uninstall-app bharterp_theme --yes"
```
