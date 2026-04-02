from odoo import models, fields, api

class JsonData(models.Model):
    _name = 'fr.localflow.json_data'
    _description = 'JSON Data Holder'
    _order = 'id'

    name = fields.Char(string="Name", required=True, copy=False)
    application_name = fields.Text(string="Application Name")
    description = fields.Text(string="Description")
    type = fields.Text(string="Type")
    
    # Odoo 17+ uses fields.Json. 
    # For older versions, use fields.Text
    content = fields.Json(string="Content")

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            # Ensure the sequence code matches the new _name
            vals['name'] = self.env['ir.sequence'].next_by_code('fr.localflow.json_data') or 'New'
        return super(JsonData, self).create(vals)
    