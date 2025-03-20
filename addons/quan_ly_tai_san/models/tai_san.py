import re
from dateutil.relativedelta import relativedelta
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class TaiSan(models.Model):
    _name = 'tai_san'
    _description = 'Bảng chứa thông tin tài sản'
    _order = 'ma_tai_san'
    _rec_name = 'ten_tai_san'
    _sql_constraints = [
        ('ma_tai_san_unique', 'unique(ma_tai_san)', 'Mã tài sản phải là duy nhất!')
    ]

    ma_tai_san = fields.Char(
        "Mã Tài sản", required=True, copy=False, default="New",
    )
    so_serial = fields.Char(
        "Serial", required=True, copy=False, default="New",
    )

    ten_tai_san = fields.Char(
        "Tên Tài sản", required=True,
    )

    ngay_mua = fields.Datetime(
        "Ngày mua",
    )

    ngay_het_han_bao_hanh = fields.Date(
        "Ngày hết hạn bảo hành",
    )

    gia_tien_mua = fields.Float(
        "Giá tiền mua", digits=(16, 2),
    )

    gia_tri_hien_tai = fields.Float(
        "Giá trị hiện tại", digits=(16, 2),
    )

    TRANG_THAI = [
        ("CatGiu", "Lưu trữ"),
        ("Muon", "Mượn"),
        ("BaoTri", "Bảo trì"),
    ]

    trang_thai = fields.Selection(
        TRANG_THAI, string="Trạng thái", default="CatGiu", tracking=True
    )

    loai_tai_san_id = fields.Many2one(
        comodel_name='loai_tai_san', string="Loại tài sản", required=True,
    )

    vi_tri_hien_tai_id = fields.Many2one(
        comodel_name='vi_tri', string="Vị trí hiện tại", store=True,
    )

    nha_cung_cap_id = fields.Many2one(
        comodel_name='nha_cung_cap', string="Nhà cung cấp", store=True,
    )

    lich_su_su_dung_ids = fields.One2many(
        comodel_name='lich_su_su_dung', inverse_name='tai_san_id',
        string="Lịch sử sử dụng", store=True,
    )

    lich_su_bao_tri_ids = fields.One2many(
        comodel_name='lich_su_bao_tri', inverse_name='tai_san_id',
        string="Lịch sử bảo trì", store=True,
    )

    khau_hao_ids = fields.One2many(
        comodel_name='khau_hao', inverse_name='tai_san_id',
        string="Khấu hao", store=True,
    )

    lich_su_dieu_chuyen_ids = fields.One2many(
        comodel_name='lich_su_dieu_chuyen', inverse_name='tai_san_id',
        string="Lịch sử điều chuyển",
    )

    nguoi_su_dung_id = fields.Many2one(comodel_name="nhan_vien", string="Người đang sử dụng", store=True)


    thanh_ly_id = fields.Many2one(
        comodel_name='thanh_ly',
        string="Phiếu thanh lý",
    )

    def action_dieu_chuyen_tai_san(self):
        for record in self:
            return {
                'name': 'điều chuyển tài sản',
                'type': 'ir.actions.act_window',
                'res_model': 'lich_su_dieu_chuyen',
                'view_mode': 'form',
                'target': 'new',
                'context': {
                    'default_tai_san_id': record.id,
                    'default_vi_tri_id': record.vi_tri_hien_tai_id.id,
                },
            }
