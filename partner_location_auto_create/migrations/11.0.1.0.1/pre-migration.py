def migrate(cr, version):
    """remove company id fromm all locations of type supplier/vendor"""
    cr.execute("""
        update stock_location set company_id=Null where usage in ('supplier','customer');
    """)