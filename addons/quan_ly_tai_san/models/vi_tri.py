import re

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ViTri(models.Model):
    _name = 'vi_tri'
    _description = 'Bảng chứa thông tin tài sản'
    _rec_name = "ten_vi_tri"
    _order = 'ma_vi_tri'
    _sql_constraints = [
        ('ma_vi_tri_unique', 'unique(ma_vi_tri)', 'Mã vị trí phải là duy nhất!'),
        ('tai_san_unique', 'unique(tai_san_id)', 'Mỗi tài sản chỉ có một vị trí!')
    ]

    ma_vi_tri = fields.Char("Mã vị trí", required=True)
    ten_vi_tri = fields.Char("Tên vị trí", required=True)
    tai_san_id = fields.Many2one(
        comodel_name='tai_san',
        inverse_name='vi_tri_id', string="Tài sản", required=True)

    @api.constrains('ma_vi_tri')
    def _check_ma_vi_tri_format(self):
        for record in self:
            if not re.fullmatch(r'VT-\d{4}', record.ma_vi_tri):
                raise ValidationError("Mã vị trí phải có định dạng VT-XXXX (ví dụ: VT-1234)")

    def write(self, vals):
        res = super(ViTri, self).write(vals)
        for rec in self:
            if rec.tai_san_id:
                rec.tai_san_id._compute_vi_tri()
        return res