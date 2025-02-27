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

    ma_tai_san = fields.Char("Mã Tài sản", required=True, copy=False, readonly=True, default="New")
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


    loai_tai_san_id = fields.Many2one(comodel_name='loai_tai_san', string="Loại tài sản", required=True)
    vi_tri_hien_tai_id = fields.Many2one(
        comodel_name='vi_tri',
        string="Vị trí hiện tại",
        store=True
    )
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
    lich_su_bao_tri_ids = fields.One2many(
        comodel_name='lich_su_bao_tri',
        inverse_name='tai_san_id',
        string="Lịch sử bảo trì",
        store=True
    )
    khau_hao_ids = fields.One2many(
        comodel_name='khau_hao',
        inverse_name='tai_san_id',
        string="Khấu hao",
        store=True
    )
    lich_su_di_chuyen_ids = fields.One2many(
        comodel_name='lich_su_di_chuyen',
        inverse_name='tai_san_id',
        string="Lịch sử di chuyển",
        readonly=True
    )

    @api.depends()
    def _compute_vi_tri(self):
        for asset in self:

            pass

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
                depreciation_rate = 0.1
                record.gia_tri_hien_tai = max(0, record.gia_tien_mua * (1 - depreciation_rate * years))

    @api.model
    def create(self, vals):
        if vals.get('so_serial', 'New') == 'New':
            vals['so_serial'] = self.env['ir.sequence'].next_by_code('tai.san.serial') or 'New'
        return super(TaiSan, self).create(vals)

    def action_di_chuyen_tai_san(self):
        for record in self:
            return {
                'name': 'Di chuyển tài sản',
                'type': 'ir.actions.act_window',
                'res_model': 'lich_su_di_chuyen',
                'view_mode': 'form',
                'target': 'new',
                'context': {
                    'default_tai_san_id': record.id,
                    'default_vi_tri_id': record.vi_tri_hien_tai_id.id,
                },
            }