# -*- coding: utf-8 -*-
{
    'name': "quan_ly_tai_san",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'sequences.xml',
        'views/tai_san.xml',
        'views/vi_tri.xml',
        'views/loai_tai_san.xml',
        'views/nha_cung_cap.xml',
        'views/bo_phan.xml',
        'views/nhan_su.xml',
        'views/lich_su_su_dung.xml',
        'views/lich_su_bao_tri.xml',
        'views/khau_hao.xml',
        'views/menu.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
