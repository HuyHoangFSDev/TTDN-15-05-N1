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

    ma_tai_san = fields.Char("Mã Tài sản", required=True)
    ten_tai_san = fields.Char("Tên Tài sản", required=True)
    so_serial = fields.Char("Số serial", required=True, copy=False, readonly=True, default="New")
    ngay_mua = fields.Date("Ngày mua")
    ngay_het_han_bao_hanh = fields.Date("Ngày hết hạn bảo hành")
    gia_tien_mua = fields.Float("Giá tiền mua", digits=(16, 2))
    gia_tri_hien_tai = fields.Float("Giá trị hiện tại", digits=(16, 2))

    TRANG_THAI = [
        ("Muon", "Mượn"),
        ("BaoTri", "Bảo trì"),
        ("LuuTru", "Lưu trữ"),
        ("Hong", "Hỏng"),
    ]

    trang_thai = fields.Selection(TRANG_THAI, string="Trạng thái", default="LuuTru", tracking=True)

    ## Quan hệ các bảng
    loai_tai_san_id = fields.Many2one(comodel_name='loai_tai_san', string="Loại tài sản", required=True)
    vi_tri_id = fields.Many2one('vi_tri', string="Vị trí", compute='_compute_vi_tri', store=True)
    nha_cung_cap_id = fields.Many2one(
        comodel_name='nha_cung_cap',
        string="Nhà cung cấp",
        store=True
    )
    lich_su_su_dung_ids = fields.One2many(
        comodel_name='lich_su_su_dung',
        inverse_name='tai_san_id',
        string="Lịch sử sử dụng",
        store=True
    )

    @api.depends()
    def _compute_vi_tri(self):
        for asset in self:
            vi_tri = self.env['vi_tri'].search([('tai_san_id', '=', asset.id)], limit=1)
            asset.vi_tri_id = vi_tri.id if vi_tri else False

    @api.constrains('ngay_mua', 'ngay_het_han_bao_hanh')
    def _check_dates(self):
        for record in self:
            if record.ngay_mua and record.ngay_het_han_bao_hanh:
                if record.ngay_het_han_bao_hanh < record.ngay_mua:
                    raise ValidationError("Ngày hết hạn bảo hành phải lớn hơn hoặc bằng ngày mua!")

    @api.constrains('ma_tai_san')
    def _check_ma_tai_san_format(self):
        for record in self:
            if not re.fullmatch(r'TS-\d{4}', record.ma_tai_san):
                raise ValidationError("Mã tài sản phải có định dạng TS-XXXX (ví dụ: TS-1234)")

    @api.depends_context("date")
    @api.depends('gia_tien_mua', 'ngay_mua')
    def _compute_gia_tri_hien_tai(self):
        for record in self:
            if record.ngay_mua:
                if record.ngay_mua > fields.Date.today():
                    raise ValidationError("Ngày mua không thể lớn hơn ngày hiện tại!")

                years = relativedelta(fields.Date.today(), record.ngay_mua).years
                depreciation_rate = 0.1  # 10% mỗi năm
                record.gia_tri_hien_tai = max(0, record.gia_tien_mua * (1 - depreciation_rate * years))

    @api.model
    def create(self, vals):
        if vals.get('so_serial', 'New') == 'New':
            vals['so_serial'] = self.env['ir.sequence'].next_by_code('tai.san.serial') or 'New'
        return super(TaiSan, self).create(vals)
