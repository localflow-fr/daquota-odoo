# -*- coding: utf-8 -*-
import requests
from odoo import http
from odoo.http import request
import logging
import json
from urllib.parse import urlencode

_logger = logging.getLogger('odoo')

class DaquotaAppProxyController(http.Controller):

    @http.route("/daquota_app_launcher/redirect", type="http", auth="user")
    def redirect_to_daquota(self, app_name=None):

        if not app_name:
            return "Missing app name. Please pass ?app_name=xxx in the URL."
        
        icp = request.env["ir.config_parameter"].sudo()
        proxy_url = "https://backoffice.daquota.io"

        integration_url = request.httprequest.url_root.rstrip('/')
        integration_db = icp.get_param("daquota_app_launcher.integration_db")
        auth_method = icp.get_param("daquota_app_launcher.proxy_auth_method", "login_pass")

        if auth_method == "login_pass":
            integration_login = icp.get_param("daquota_app_launcher.integration_login")
            integration_password = icp.get_param("daquota_app_launcher.integration_password")

            if not (integration_url and integration_db and integration_login and integration_password):
                return "Missing configuration for Login/Password authentication. Please check Daquota settings."

            auth_payload = {
                "url": integration_url,
                "db": integration_db,
                "username": integration_login,
                "password": integration_password
            }
            _logger.info(f"Proxy login: {integration_login}")

        elif auth_method == "user_apikey":
            # Use the current logged-in user's login and API key
            user = request.env.user
            # For Odoo 16+, API keys are stored in `api_key_ids`.
            # We'll take the first one if it exists.
            if not user.api_key_ids:
                return "Current user has no API key. Please create one in Preferences."
            
            api_key = user.api_key_ids[0].key

            if not (integration_url and integration_db):
                return "Missing DB configuration for API Key authentication. Please check Daquota settings."

            auth_payload = {
                "url": integration_url,
                "db": integration_db,
                "username": user.login,
                "password": api_key
            }
            _logger.info(f"Proxy login (using user API key): {user.login}")

        else:
            return "Invalid proxy authentication method configuration."
                
        _logger.info(f"Proxy server URL: {integration_url}")
        _logger.info(f"Proxy DB: {integration_db}")
        _logger.info(f"Proxy app name: {app_name}")

        server_domain = request.httprequest.host

        self._ensure_tenant_exists(proxy_url, 'v1', auth_payload, server_domain)

        try:

            app_base_url = f"https://apps.daquota.io/{server_domain}/{app_name}"

            response = requests.get(app_base_url + '/index.html')
            response.raise_for_status()  # raises error if request failed
            target_content = response.text

            # Extract bundledApplicationModel
            start_delim = "window.bundledApplicationModel = window.bundledApplicationModel || "
            start_index = target_content.find(start_delim)
            if start_index == -1:
                raise ValueError("Start delimiter not found in file")

            bundled_application_model = target_content[start_index + len(start_delim):]
            end_index = bundled_application_model.find("</script>")
            if end_index == -1:
                raise ValueError("End delimiter not found in file")

            bundled_application_model = bundled_application_model[:end_index]

            # Recursive search for BackofficeConnector
            def find_backoffice_proxy_version(data):
                if isinstance(data, dict):
                    if data.get("type") == "BackofficeConnector":
                        return data.get("proxyVersion")
                    for value in data.values():
                        result = find_backoffice_proxy_version(value)
                        if result is not None:
                            return result
                elif isinstance(data, list):
                    for value in data:
                        result = find_backoffice_proxy_version(value)
                        if result is not None:
                            return result
                return None

            # Decode JSON and search for proxy version
            try:
                model_data = json.loads(bundled_application_model)
            except json.JSONDecodeError as e:
                raise ValueError(f"Failed to parse bundled application model: {e}")

            proxy_version = find_backoffice_proxy_version(model_data)
            _logger.info(f"proxy version: {proxy_version}")

            token = self._login_to_proxy(proxy_url, proxy_version, auth_payload)
            if not token:
                return "No access token in proxy response."

            # Redirect to app

            _logger.info(f"Redirecting to: {app_base_url}")
            
            #return request.redirect(f"{app_base_url}?token={token}")
            html = f"""
            <html>
            <body onload="document.forms[0].submit()">
                <form action="{app_base_url}" method="get">
                <input type="hidden" name="token" value="{token}">
                </form>
            </body>
            </html>
            """
            return request.make_response(html, headers=[('Content-Type', 'text/html')])

        except Exception as e:
            return f"Error connecting to proxy: {e}"

    def _login_to_proxy(self, proxy_url, proxy_version, auth_payload):
        # Login to proxy
        json_data = {
            "type": "odoo",
            "config": auth_payload
        }

        _logger.info("Connecting with:\n%s", json.dumps(json_data, indent=2))
        resp = requests.post(proxy_url + "/" + proxy_version + "/session", json=json_data, timeout=10)

        if resp.status_code != 200:
            return f"Proxy returned error: {resp.status_code} - {json.dumps(json_data)}"

        data = resp.json()
        _logger.info("Result:\n%s", json.dumps(data, indent=2))

        return data.get("token")
    
    def _ensure_tenant_exists(self, proxy_url, proxy_version, auth_payload, server_domain):
        # 1️⃣ Determine tenant (use current host)
        _logger.info(f"Tenant resolved as: {server_domain}")

        # 2️⃣ Check if tenant exists
        tenant_check_url = f"https://apps.daquota.io/{server_domain}/daquota_admin/api/authenticate.php"
        tenant_exists = False
        try:
            resp = requests.get(tenant_check_url, timeout=5)
            if resp.status_code == 200:
                tenant_exists = True
                _logger.info(f"Tenant {server_domain} exists.")
        except requests.RequestException as e:
            _logger.warning(f"Error checking tenant {server_domain}: {e}")

        # 3️⃣ If not exists → create it
        if not tenant_exists:
            _logger.info(f"Tenant {server_domain} does not exist. Creating tenant...")

            token = self._login_to_proxy(proxy_url, proxy_version, auth_payload)
            if not token:
                return "No access token in proxy response."

            # Odoo user info
            user = request.env.user
            email = user.login

            params = {
                "templateTenant": "template1-odoo",
                "targetTenant": server_domain
            }

            create_url = (
                f"https://apps.daquota.io/template1-odoo/daquota_admin/api/admin/create_backoffice_tenant.php?"
                + urlencode(params)
            )

            _logger.info("Create URL: %s", create_url)

            try:
                resp = requests.post(create_url, json={}, headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {token}",
                    "X-User": email
                }, timeout=10)
                if resp.ok:
                    _logger.info(f"Tenant {server_domain} successfully created.")
                else:
                    _logger.error(f"Failed to create tenant {server_domain}. Status: {resp.status_code}")
                    return f"Error creating tenant {server_domain}."
            except requests.RequestException as e:
                _logger.error(f"Error creating tenant {server_domain}: {e}")
                return f"Error creating tenant {server_domain}: {e}"
