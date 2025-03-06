import re

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class NhaCungCap(models.Model):
    _name = 'nha_cung_cap'
    _description = 'Bảng chứa thông tin tài sản'
    _rec_name = "ten_nha_cung_cap"
    _order = 'ma_nha_cung_cap'
    _sql_constraints = [
        ('ma_nha_cung_cap_unique', 'unique(ma_nha_cung_cap)', 'Mã nhà cung cấp phải là duy nhất!'),
    ]

    ma_nha_cung_cap = fields.Char("Mã nhà cung cấp", required=True)
    ten_nha_cung_cap = fields.Char("Tên nhà cung cấp", required=True)
    ten_nguoi_dai_dien = fields.Char("Tên người đại diện", required=True)
    so_dien_thoai = fields.Char("Số điện thoại", required=True)
    email = fields.Char("Email", required=True)
    tai_san_ids = fields.One2many(
        comodel_name='tai_san',
        inverse_name='nha_cung_cap_id', string="Tài sản", required=True)