from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ThanhLy(models.Model):
    _name = 'thanh_ly'
    _description = 'Quản lý thanh lý tài sản'
    _order = 'ma_thanh_ly desc'
    _sql_constraints = [
        ('ma_thanh_ly_unique', 'unique(ma_thanh_ly)', 'Mã thanh lý phải là duy nhất!')
    ]

    ma_thanh_ly = fields.Char(
        string="Mã thanh lý",
        copy=False,
        default="New",
    )

    ngay_thanh_ly = fields.Date(
        string="Ngày thanh lý",
        required=True,
        default=fields.Date.context_today,
    )

    tai_san_id = fields.Many2one(
        comodel_name='tai_san',
        string="Tài sản",
        required=True,
    )

    gia_tri_thanh_ly = fields.Float(
        string="Giá trị thanh lý",
        digits=(16, 2),
        required=True,
    )

    TRANG_THAI = [
        ('draft', 'Nháp'),
        ('confirmed', 'Đã xác nhận'),
        ('done', 'Hoàn thành'),
        ('cancelled', 'Đã hủy'),
    ]

    trang_thai = fields.Selection(
        selection=TRANG_THAI,
        string="Trạng thái",
        default='draft',
        required=True,
        tracking=True
    )

    ly_do = fields.Text(
        string="Lý do thanh lý",
    )

    nguoi_xu_ly_id = fields.Many2one(
        comodel_name='nhan_vien',
        string="Người xử lý",
        required=True,
    )


    @api.constrains('tai_san_id')
    def _check_tai_san_thanh_ly(self):
        for record in self:
            if record.tai_san_id.thanh_ly_id and record.tai_san_id.thanh_ly_id != record:
                raise ValidationError(f"Tài sản {record.tai_san_id.ten_tai_san} đã có phiếu thanh lý khác!")

    def action_confirm(self):
        self.ensure_one()
        if self.trang_thai == 'draft':
            self.trang_thai = 'confirmed'
        else:
            raise ValidationError("Chỉ có thể xác nhận phiếu ở trạng thái Nháp!")

    def action_done(self):
        self.ensure_one()
        if self.trang_thai != 'confirmed':
            raise ValidationError("Phiếu cần được xác nhận trước khi hoàn thành!")
        self.tai_san_id.trang_thai = 'DaThanhLy'
        self.trang_thai = 'done'

    def action_cancel(self):
        self.ensure_one()
        if self.trang_thai in ('draft', 'confirmed'):
            self.trang_thai = 'cancelled'
            self.tai_san_id.thanh_ly_id = False
            self.tai_san_id.trang_thai = 'LuuTru'
        else:
            raise ValidationError("Không thể hủy phiếu đã hoàn thành!")

    @api.constrains('tai_san_id', 'trang_thai')
    def _check_tai_san_trang_thai(self):
        for record in self:
            if record.trang_thai == 'done' and record.tai_san_id.trang_thai not in ('Hong', 'LuuTru'):
                raise ValidationError("Chỉ có thể thanh lý tài sản ở trạng thái 'Hỏng' hoặc 'Lưu trữ'!")
            if record.trang_thai == 'confirmed' and record.tai_san_id.trang_thai in ('Muon', 'BaoTri'):
                raise ValidationError("Không thể thanh lý tài sản đang được mượn hoặc bảo trì!")