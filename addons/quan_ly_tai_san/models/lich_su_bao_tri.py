import re

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class LichSuBaoTri(models.Model):
    _name = 'lich_su_bao_tri'
    _description = 'Bảng chứa thông tin lịch sử bảo trì'
    _order = 'ma_lich_su_bao_tri'
    _sql_constraints = [
        ('ma_lich_su_bao_tri_unique', 'unique(ma_lich_su_bao_tri)', 'Mã lịch sử bảo trì phải là duy nhất!'),
    ]

    ma_lich_su_bao_tri = fields.Char("Mã lịch sử bảo trì", required=True)
    ngay_bao_tri = fields.Date("Ngày bảo trì", required=True)
    ngay_tra = fields.Date("Ngày trả", required=True)
    chi_phi = fields.Integer("Chi phi", required=True)
    ghi_chu = fields.Char("Ghi chú")
    tai_san_id = fields.Many2one(comodel_name="tai_san", string= "Tài sản",store=True)

    @api.constrains('ma_lich_su_bao_tri')
    def _check_ma_lich_su_bao_tri_format(self):
        for record in self:
            if not re.fullmatch(r'LSBT-\d{4}', record.ma_lich_su_bao_tri):
                raise ValidationError("Mã phải có định dạng LSBT-XXXX (ví dụ: LSBT-1234)")

    @api.model
    def create(self, vals):
        if vals.get('ma_lich_su_bao_tri', 'New') == 'New':
            vals['ma_lich_su_bao_tri'] = self.env['ir.sequence'].next_by_code('lich_su_bao_tri') or 'New'
        return super(LichSuBaoTri, self).create(vals)