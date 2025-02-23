import re

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class NhanVien(models.Model):
    _name = 'nhan_vien'
    _description = 'Bảng chứa thông tin tài sản'
    _rec_name = "ten_nhan_vien"
    _order = 'ma_nhan_vien'
    _sql_constraints = [
        ('ma_nhan_vien_unique', 'unique(ma_nhan_vien)', 'Mã nhân viên phải là duy nhất!'),
    ]

    ma_nhan_vien = fields.Char("Mã nhân viên", required=True)
    ten_nhan_vien = fields.Char("Tên nhân viên", required=True)
    ngay_sinh = fields.Date("Ngày sinh")
    email = fields.Char("Email")
    so_dien_thoai = fields.Char("Số điện thoại")
    dia_chi = fields.Char("Địa chỉ")
    phong_ban_id = fields.Many2one(comodel_name="phong_ban", string="Phòng Ban", store=True)
    lich_su_su_dung_ids = fields.One2many(comodel_name="lich_su_su_dung", inverse_name="nhan_vien_id",
                                          string="Lịch sử sử dụng", store=True)

    @api.constrains('ma_nhan_vien')
    def _check_ma_nhan_vien_format(self):
        for record in self:
            if not re.fullmatch(r'NV-\d{4}', record.ma_nhan_vien):
                raise ValidationError("Mã nhân viên phải có định dạng NV-XXXX (ví dụ: NV-1234)")

    @api.constrains('email')
    def _check_email_format(self):
        for record in self:
            if record.email:
                if not re.fullmatch(r"^\S+@\S+\.\S+$", record.email):
                    raise ValidationError("Định dạng email không hợp lệ!")

    @api.constrains('so_dien_thoai')
    def _check_so_dien_thoai_format(self):
        for record in self:
            if record.so_dien_thoai:
                if not re.fullmatch(r'^\+?\d{9,15}$', record.so_dien_thoai):
                    raise ValidationError(
                        "Số điện thoại không hợp lệ! Vui lòng nhập số từ 9 đến 15 chữ số, có thể bắt đầu bằng +.")

    @api.constrains('ngay_sinh')
    def _check_ngay_sinh(self):
        for record in self:
            if record.ngay_sinh and record.ngay_sinh > fields.Date.today():
                raise ValidationError("Ngày sinh không thể là ngày trong tương lai!")
