from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    # Override the partner_id field to modify its display
    partner_id = fields.Many2one(
        'res.partner',
        string='Customer',
        readonly=True,
        states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},
        required=True,
        change_default=True,
        index=True,
        tracking=1,
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",
        context={'show_job_in_name': True, 'from_sale_order': True}
    )
    
    @api.depends('partner_id', 'partner_id.function')
    def _compute_partner_display_name(self):
        """Compute a display name for partner that includes job position"""
        for order in self:
            if order.partner_id:
                if order.partner_id.function:
                    order.partner_display_name = f"{order.partner_id.name} - {order.partner_id.function}"
                else:
                    order.partner_display_name = order.partner_id.name
            else:
                order.partner_display_name = ''
    
    partner_display_name = fields.Char(
        string='Customer Display Name',
        compute='_compute_partner_display_name',
        store=True,
        help="Customer name with job position for display purposes"
    )
    
    def _get_name_sale_report(self, name):
        """Override for sale report name display"""
        return super()._get_name_sale_report(name)

# ==== Additional method to ensure proper display in debug menu ====
class SaleOrderDebugEnhancement(models.Model):
    _inherit = 'sale.order'
    
    def read(self, fields=None, load='_classic_read'):
        """Override read method to enhance partner_id display in debug mode"""
        result = super().read(fields, load)
        
        # Check if partner_id is being read and enhance it
        if isinstance(result, list):
            for record in result:
                if 'partner_id' in record and record['partner_id']:
                    partner_id = record['partner_id'][0] if isinstance(record['partner_id'], tuple) else record['partner_id']
                    partner = self.env['res.partner'].browse(partner_id)
                    if partner.function:
                        display_name = f"{partner.name} - {partner.function}"
                        if isinstance(record['partner_id'], tuple):
                            record['partner_id'] = (partner_id, display_name)
                        
        elif isinstance(result, dict):
            if 'partner_id' in result and result['partner_id']:
                partner_id = result['partner_id'][0] if isinstance(result['partner_id'], tuple) else result['partner_id']
                partner = self.env['res.partner'].browse(partner_id)
                if partner.function:
                    display_name = f"{partner.name} - {partner.function}"
                    if isinstance(result['partner_id'], tuple):
                        result['partner_id'] = (partner_id, display_name)
        
        return result