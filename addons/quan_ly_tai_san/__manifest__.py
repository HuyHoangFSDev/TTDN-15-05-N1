# -*- coding: utf-8 -*-
{
    'name': "Quản lý tài sản",

    'summary': "Quản lý tài sản, lịch sử sử dụng và khấu hao",

    'description': """
        Module quản lý tài sản trong doanh nghiệp, bao gồm:
        - Thông tin tài sản (tai_san, loai_tai_san, vi_tri, nha_cung_cap)
        - Lịch sử sử dụng (lich_su_su_dung)
        - Lịch sử bảo trì (lich_su_bao_tri)
        - Khấu hao tài sản (khau_hao)
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    'category': 'Human Resources/Assets',
    'version': '0.1',

    # Các module cần thiết để module này hoạt động
    'depends': ['base', 'nhan_su'],

    # Các file dữ liệu luôn được tải
    'data': [
        'security/ir.model.access.csv',
        'sequences.xml',
        'views/tai_san.xml',
        'views/phieu_muon.xml',
        'views/phieu_bao_tri.xml',
        'views/vi_tri.xml',
        'views/loai_tai_san.xml',
        'views/nha_cung_cap.xml',
        'views/lich_su_su_dung.xml',
        'views/lich_su_bao_tri.xml',
        'views/lich_su_di_chuyen.xml',
        'views/khau_hao.xml',
        'views/menu.xml',
    ],

    # Các file demo chỉ tải khi chạy ở chế độ demo
    'demo': [
        'demo/demo.xml',
    ],

    # Tài sản (CSS, JS) được tải vào giao diện backend
    'assets': {
        'web.assets_backend': [
            'quan_ly_tai_san/static/src/css/tai_san.css',
        ],
    },

    # Đảm bảo module có thể cài đặt
    'installable': True,
    'application': True,  # Nếu muốn module hiển thị như một ứng dụng trong Apps
}