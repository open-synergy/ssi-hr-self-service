import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo14-addons-open-synergy-ssi-hr-self-service",
    description="Meta package for open-synergy-ssi-hr-self-service Odoo addons",
    version=version,
    install_requires=[
        'odoo14-addon-ssi_hr_employee_data_change',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 14.0',
    ]
)
