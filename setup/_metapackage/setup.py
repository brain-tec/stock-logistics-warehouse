import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo12-addons-oca-stock-logistics-warehouse",
    description="Meta package for oca-stock-logistics-warehouse Odoo addons",
    version=version,
    install_requires=[
        'odoo12-addon-account_move_line_stock_info',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
    ]
)
