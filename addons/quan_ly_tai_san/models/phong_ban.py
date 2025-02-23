import re

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class PhongBan(models.Model):
    _name = 'phong_ban'
    _description = 'Bảng chứa thông tin tài sản'
    _rec_name = "ten_phong_ban"
    _order = 'ma_phong_ban'
    _sql_constraints = [
        ('ma_phong_ban_unique', 'unique(ma_phong_ban)', 'Mã vị trí phải là duy nhất!'),
    ]

    ma_phong_ban = fields.Char("Mã vị trí", required=True)
    ten_phong_ban = fields.Char("Tên vị trí", required=True)
    mo_ta = fields.Char("Mô tả")
    nhan_vien_ids = fields.One2many(comodel_name="nhan_vien", inverse_name="phong_ban_id", string= "Nhân viên",store=True)

    @api.constrains('ma_phong_ban')
    def _check_ma_phong_ban_format(self):
        for record in self:
            if not re.fullmatch(r'PB-\d{4}', record.ma_phong_ban):
                raise ValidationError("Mã phòng ban phải có định dạng PB-XXXX (ví dụ: PB-1234)")
