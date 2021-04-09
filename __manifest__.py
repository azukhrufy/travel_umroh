# -*- coding: utf-8 -*-
{
    'name': "Aplikasi Travel Umroh NTI",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Ananda Zukhruf Awalwi",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','mail','contacts','product','sale','stock','report_xlsx'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/mainmenu/layananumroh.xml',
        'views/mainmenu/custinvoice.xml',
        'views/mainmenu/register.xml',
        'views/mainmenu/salesorders.xml',
        'views/mainmenu/tourpackages.xml',
        'report/surat_jalan.xml',
        'report/tagihan_jamaah.xml',
        'report/tagihanjamaah.xml',
        'report/deliveryorder.xml',
        'report/cetakjamaah.xml',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application': True,
}