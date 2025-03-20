{
    'name': "Quản lý tài sản",

    'summary': "",

    'description': "",

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    'category': 'Human Resources/Assets',
    'version': '0.1',

    'depends': ['base', 'nhan_su'],

    'data': [
        'security/ir.model.access.csv',
        'views/tai_san.xml',
        'views/phieu_muon.xml',
        'views/phieu_bao_tri.xml',
        'views/vi_tri.xml',
        'views/loai_tai_san.xml',
        'views/nha_cung_cap.xml',
        'views/lich_su_su_dung.xml',
        'views/lich_su_bao_tri.xml',
        'views/lich_su_dieu_chuyen.xml',
        'views/phieu_dieu_chuyen.xml',
        'views/khau_hao.xml',
        'views/thanh_ly.xml',
        'views/menu.xml',
    ],

    'demo': [
        'demo/demo.xml',
    ],

    'installable': True,
    'application': True,
}
