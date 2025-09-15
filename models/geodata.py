from odoo import models, fields, api

class GeoData(models.Model):
    _name = 'fr.localflow.geodata'
    _description = 'Geodata'

    name = fields.Char(string="Name", required=True, copy=False)
    type = fields.Selection(
        selection=[
            ('id_list', 'ID List'),
            ('kml', 'KML'),
            ('geojson', 'GEOJSON'),
        ],
        string="Type",
        required=True
    )
    content = fields.Text(string="Content")

    @api.model
    def create(self, vals):
        # If no name provided, generate one from a sequence
        if not vals.get('name'):
            vals['name'] = self.env['ir.sequence'].next_by_code('fr.localflow.geodata') or 'New'
        return super().create(vals)
    
    # Standard audit fields (provided automatically in Odoo 17):
    # - id (primary key)
    # - create_uid (owner)
    # - create_date
    # - write_uid
    # - write_date
