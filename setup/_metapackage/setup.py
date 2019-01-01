import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo9-addons-oca-stock-logistics-warehouse",
    description="Meta package for oca-stock-logistics-warehouse Odoo addons",
    version=version,
    install_requires=[
        'odoo9-addon-account_move_line_product',
        'odoo9-addon-account_move_line_stock_info',
        'odoo9-addon-procurement_auto_create_group',
        'odoo9-addon-stock_account_change_product_valuation',
        'odoo9-addon-stock_account_quant_merge',
        'odoo9-addon-stock_available',
        'odoo9-addon-stock_available_immediately',
        'odoo9-addon-stock_available_mrp',
        'odoo9-addon-stock_available_unreserved',
        'odoo9-addon-stock_cycle_count',
        'odoo9-addon-stock_demand_estimate',
        'odoo9-addon-stock_inventory_chatter',
        'odoo9-addon-stock_inventory_discrepancy',
        'odoo9-addon-stock_inventory_exclude_sublocation',
        'odoo9-addon-stock_inventory_lockdown',
        'odoo9-addon-stock_inventory_preparation_filter',
        'odoo9-addon-stock_inventory_revaluation',
        'odoo9-addon-stock_inventory_verification_request',
        'odoo9-addon-stock_location_area_data',
        'odoo9-addon-stock_location_lockdown',
        'odoo9-addon-stock_move_partner_info',
        'odoo9-addon-stock_mts_mto_rule',
        'odoo9-addon-stock_orderpoint_generator',
        'odoo9-addon-stock_orderpoint_manual_procurement',
        'odoo9-addon-stock_orderpoint_uom',
        'odoo9-addon-stock_partner_lot',
        'odoo9-addon-stock_putaway_product',
        'odoo9-addon-stock_quant_manual_assign',
        'odoo9-addon-stock_quant_merge',
        'odoo9-addon-stock_quant_reserved_qty_uom',
        'odoo9-addon-stock_removal_location_by_priority',
        'odoo9-addon-stock_reserve',
        'odoo9-addon-stock_valuation_account_manual_adjustment',
        'odoo9-addon-stock_warehouse_orderpoint_stock_info',
        'odoo9-addon-stock_warehouse_orderpoint_stock_info_unreserved',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
    ]
)
