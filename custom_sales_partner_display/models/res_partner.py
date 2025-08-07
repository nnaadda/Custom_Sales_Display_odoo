from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    @api.depends('name', 'function')
    def _compute_name_with_job(self):
        """Compute display name with job position"""
        for partner in self:
            if partner.function:
                partner.name_with_job = f"{partner.name} - {partner.function}"
            else:
                partner.name_with_job = partner.name or ''
    
    name_with_job = fields.Char(
        string='Name with Job Position',
        compute='_compute_name_with_job',
        help="Partner name combined with their job position"
    )
    
    def name_get(self):
        """Override name_get to include job position in certain contexts"""
        result = []
        for partner in self:
            # Check if we're in a sales order context
            context = self.env.context
            if context.get('show_job_in_name', False) or context.get('from_sale_order', False):
                if partner.function:
                    name = f"{partner.name} - {partner.function}"
                else:
                    name = partner.name
            else:
                name = partner.name
            result.append((partner.id, name))
        return result