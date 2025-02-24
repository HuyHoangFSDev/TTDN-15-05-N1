import re

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class BoPhan(models.Model):
    _name = 'bo_phan'
    _description = 'Bảng chứa thông tin tài sản'
    _rec_name = "ten_bo_phan"
    _order = 'ma_bo_phan'
    _sql_constraints = [
        ('ma_bo_phan_unique', 'unique(ma_bo_phan)', 'Mã bộ phận phải là duy nhất!'),
    ]

    ma_bo_phan = fields.Char("Mã bộ phận", required=True)
    ten_bo_phan = fields.Char("Tên bộ phận", required=True)
    mo_ta = fields.Char("Mô tả")
    nhan_su_ids = fields.One2many(comodel_name="nhan_su", inverse_name="bo_phan_id", string= "Nhân viên",store=True)

    @api.constrains('ma_bo_phan')
    def _check_ma_bo_phan_format(self):
        for record in self:
            if not re.fullmatch(r'BP-\d{4}', record.ma_bo_phan):
                raise ValidationError("Mã bộ phận phải có định dạng BP-XXXX (ví dụ: BP-1234)")
