# -*- coding: utf-8 -*-
from odoo import fields, models, api


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    proxy_auth_method = fields.Selection(
        [
            ("login_pass", "Integration Login/Password"),
            ("user_apikey", "Current User API Key"),
        ],
        string="Proxy Authentication Method",
        default="login_pass",
        config_parameter="daquota_app_launcher.proxy_auth_method",
        help="Choose how Odoo authenticates to the proxy (login/password or user API key)."
    )
    integration_db = fields.Char(
        string="Integration DB",
        config_parameter="daquota_app_launcher.integration_db",
        help="Database name to connect to."
    )
    integration_login = fields.Char(
        string="Integration Login",
        config_parameter="daquota_app_launcher.integration_login",
        help="Login (integration user, not used if API key is selected)."
    )
    integration_password = fields.Char(
        string="Integration Password",
        config_parameter="daquota_app_launcher.integration_password",
        help="Password (integration user, not used if API key is selected)."
    )
    # app_base_url = fields.Char(
    #     string="Daquota App Name",
    #     config_parameter="daquota_app_launcher.app_base_url",
    #     help="The Daquota app URL to open after obtaining token (token will be appended as ?token=...)"
    # )
    # app_name = fields.Char(
    #     string="Daquota App Name",
    #     config_parameter="daquota_app_launcher.app_name",
    #     help="The Daquota app to be started from Odoo."
    # )

    @api.model
    def get_values(self):
        res = super().get_values()
        icp = self.env["ir.config_parameter"].sudo()
        integration_db = icp.get_param("daquota_app_launcher.integration_db")
        if not integration_db:
            integration_db = self.env.cr.dbname  # fallback to current DB
        res.update(
            integration_db=integration_db,
        )
        return res

    def set_values(self):
        super().set_values()
        icp = self.env["ir.config_parameter"].sudo()
        icp.set_param("daquota_app_launcher.integration_db", self.integration_db or self.env.cr.dbname)
