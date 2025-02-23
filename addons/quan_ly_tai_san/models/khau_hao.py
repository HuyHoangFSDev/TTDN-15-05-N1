import re

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class KhauHao(models.Model):
    _name = 'khau_hao'
    _description = 'Bảng chứa thông tin khấu hao'
    _order = 'ma_khau_hao'
    _sql_constraints = [
        ('ma_khau_hao_unique', 'unique(ma_khau_hao)', 'Mã khấu hao phải là duy nhất!'),
    ]

    ma_khau_hao = fields.Char("Mã khấu hao", required=True)
    phuong_phap_khau_hao = fields.Char("Phương pháp khấu hao", required=True)
    ngay_khau_hao = fields.Date("Ngày khấu hao", required=True)
    gia_tri_khau_hao = fields.Integer("Giá trị khấu hao", required=True)
    gia_tri_con_lai = fields.Integer("Giá trị còn lại", required=True)
    ghi_chu = fields.Char("Ghi chú")
    tai_san_id = fields.Many2one(comodel_name="tai_san", string="Tài sản", store=True)

    @api.constrains('ma_khau_hao')
    def _check_ma_khau_hao_format(self):
        for record in self:
            if not re.fullmatch(r'KH-\d{4}', record.ma_khau_hao):
                raise ValidationError("Mã phải có định dạng KH-XXXX (ví dụ: KH-1234)")
