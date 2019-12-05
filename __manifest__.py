# -*- coding: utf-8 -*-
{
    'name': "Sanwa Manufacturing Cost Report",

    'summary': """
        Sanwa Manufacturing Cost Report""",

    'description': """
        Sanwa Manufacturing Cost Report
    """,

    'author': "butirpadi@gmail.com",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account'],

    # always loaded
    'data': [
        # security
        'security/ir.model.access.csv',
        # data
        'data/ir_default_data.xml',
        # views
        'views/gmc_report_config_view.xml',
        'views/gmc_report_view.xml',
        'reports/gmc_report_template.xml',
        'views/opr_exp_report_config_view.xml',
        'views/opr_exp_report_view.xml',
        # Reports
        'reports/action_report.xml',
        'reports/opr_exp_report_template.xml',
        # 'views/views.xml',
        # 'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
    'installable': True,
    'application': True,
}
