import re

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class LichSuSuDung(models.Model):
    _name = 'lich_su_su_dung'
    _description = 'Bảng chứa thông tin lịch sử sử dụng'
    _order = 'ma_lich_su_su_dung'
    _sql_constraints = [
        ('ma_lich_su_su_dung_unique', 'unique(ma_lich_su_su_dung)', 'Mã lịch sử sử dụng phải là duy nhất!'),
    ]

    ma_lich_su_su_dung = fields.Char("Mã lịch sử sử dụng", required=True)
    ngay_muon = fields.Date("Ngày mượn", required=True)
    ngay_tra = fields.Date("Ngày trả", required=True)
    ghi_chu = fields.Char("Ghi chú")
    nhan_vien_id = fields.Many2one(comodel_name="nhan_vien", string= "Nhân viên",store=True)
    tai_san_id = fields.Many2one(comodel_name="tai_san", string= "Tài sản",store=True)

    @api.constrains('ma_lich_su_su_dung')
    def _check_ma_lich_su_su_dung_format(self):
        for record in self:
            if not re.fullmatch(r'LS-\d{4}', record.ma_lich_su_su_dung):
                raise ValidationError("Mã phải có định dạng LS-XXXX (ví dụ: LS-1234)")
