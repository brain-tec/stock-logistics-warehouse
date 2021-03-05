# Copyright 2014 Numérigraphe SARL
# Copyright 2017 Tecnativa - David Vidal
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from collections import Counter

from odoo import api, fields, models


class ProductProduct(models.Model):
    """Add the computation for the stock available to promise"""
    _inherit = 'product.product'

    sale_order_line_ids = fields.One2many(
        'sale.order.line', 'product_id',
        help='Technical: used to compute quantities.')
    quoted_qty = fields.Float(
        compute='_compute_quoted_qty',
        type='float',
        digits='Product Unit of Measure',
        string='Quoted',
        help="Total quantity of this Product that have been included in "
             "Quotations (Draft Sale Orders).\n"
             "In a context with a single Warehouse, this includes "
             "Quotation processed in this Warehouse.\n"
             "In a context with a single Stock Location, this includes "
             "Quotation processed at any Warehouse using "
             "this Location, or any of its children, as it's Stock "
             "Location.\n"
             "Otherwise, this includes every Quotation.",
    )

    def _compute_available_quantities_dict(self):
        res, stock_dict = super(ProductProduct,
                                self)._compute_available_quantities_dict()
        for product in self:
            res[product.id]['immediately_usable_qty'] -= \
                product.quoted_qty
        return res, stock_dict

    @api.depends('sale_order_line_ids',
                 'sale_order_line_ids.state',
                 'sale_order_line_ids.product_id',
                 'sale_order_line_ids.company_id',
                 'sale_order_line_ids.order_id',
                 'sale_order_line_ids.order_id.warehouse_id',
                 'sale_order_line_ids.order_id.warehouse_id.lot_stock_id',
                 'sale_order_line_ids.order_id.commitment_date',
                 'sale_order_line_ids.order_id.date_order')
    def _compute_quoted_qty(self):
        """Compute the quantities in Quotations."""
        domain = [('state', '=', 'draft'),
                  ('product_id', 'in', self.ids)]
        #  Limit to a specific company
        if self.env.context.get('force_company', False):
            domain.append(
                ('company_id', '=', self.env.context['force_company']))
        # when we search locations, should children be searched too?
        if self.env.context.get('compute_child', True):
            loc_op = 'child_of'
        else:
            loc_op = 'in'
        # Limit to some locations
        # Take warehouses that have these locations as stock locations
        if self.env.context.get('location', False):
            # Search by ID
            if isinstance(self.env.context['location'], int):
                domain.append(
                    ('order_id.warehouse_id.lot_stock_id', loc_op,
                     [self.env.context['location']]))
            # Search by name
            elif isinstance(self.env.context['location'], str):
                location_ids = [
                    l.id
                    for l in self.env['stock.location'].search([
                        ('complete_name', 'ilike',
                         self.env.context['location'])])]
                domain.append(
                    ('order_id.warehouse_id.lot_stock_id', loc_op,
                     location_ids))
            # Search by whatever the context has - probably a list of IDs
            else:
                domain.append(
                    ('order_id.warehouse_id.lot_stock_id', loc_op,
                     self.env.context['location']))
        # Limit to a warehouse
        if self.env.context.get('warehouse', False):
            domain.append(
                ('order_id.warehouse_id', '=', self.env.context['warehouse']))
        # Limit to a period
        from_date = self.env.context.get('from_date', False)
        to_date = self.env.context.get('to_date', False)
        if from_date:
            domain.extend([
                ('order_id.commitment_date', '>=', from_date),
                '&',  # only consider 'date_order' when 'commitment_date' is empty
                ('order_id.commitment_date', '=', False),
                ('order_id.date_order', '>=', from_date),
                ])
        if to_date:
            domain.extend([
                ('order_id.commitment_date', '<=', to_date),
                '&',  # only consider 'date_order' when 'commitment_date' is empty
                ('order_id.commitment_date', '=', False),
                ('order_id.date_order', '<=', to_date),
                ])
        # Compute the quoted quantity for each product
        results = Counter()
        for group in self.env[
            'sale.order.line'].with_context(lang='').read_group(
                domain, ['product_uom_qty', 'product_id', 'product_uom'],
                ['product_id', 'product_uom'], lazy=False):
            product_id = group['product_id'][0]
            uom_id = group['product_uom'][0]
            # Compute the quoted quantity in the product's UoM
            # Rounding is OK since small values have not been squashed before
            results += Counter({
                product_id:
                    self.env['uom.uom'].browse(uom_id)._compute_quantity(
                        group['product_uom_qty'],
                        self.browse(product_id).uom_id)
            })
        for product in self:
            product.quoted_qty = results.get(product.id, 0.0)
