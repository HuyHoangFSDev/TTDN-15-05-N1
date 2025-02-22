import re

from dateutil.relativedelta import relativedelta

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class LoaiTaiSan(models.Model):
    _name = 'loai_tai_san'
    _description = 'Bảng chứa thông tin tài sản'
    _rec_name = "ten_loai_tai_san"
    _order = 'ma_loai_tai_san'
    _sql_constraints = [
        ('ma_loai_tai_san_unique', 'unique(ma_loai_tai_san)', 'Mã loại tài sản phải là duy nhất!')
    ]

    ma_loai_tai_san = fields.Char("Mã Loại Tài sản", required=True)
    ten_loai_tai_san = fields.Char("Tên Loại Tài sản", required=True)
    mo_ta = fields.Text("Mô tả")
    tai_san_ids = fields.One2many(
        comodel_name='tai_san',
        inverse_name='loai_tai_san_id', string="Tài sản", required=True)

    @api.constrains('ma_loai_tai_san')
    def _check_ma_loai_tai_san_format(self):
        for record in self:
            if not re.fullmatch(r'LTS-\d{4}', record.ma_loai_tai_san):
                raise ValidationError("Mã loại tài sản phải có định dạng LTS-XXXX (ví dụ: LTS-1234)")
