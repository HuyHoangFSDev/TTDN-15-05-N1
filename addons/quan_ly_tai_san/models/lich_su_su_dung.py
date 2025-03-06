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

    ma_lich_su_su_dung = fields.Char("Mã lịch sử sử dụng", required=True, copy=False, readonly=True, default="New")
    ngay_muon = fields.Datetime("Thời gian mượn", required=True)
    ngay_tra = fields.Datetime("Thời gian trả", required=True)
    ghi_chu = fields.Char("Ghi chú")
    nhan_vien_id = fields.Many2one(comodel_name="nhan_vien", string="Nhân sự", store=True)
    tai_san_id = fields.Many2one(comodel_name="tai_san", string="Tài sản", store=True)

    @api.model
    def create(self, vals):
        if vals.get('ma_lich_su_su_dung', 'New') == 'New':
            vals['ma_lich_su_su_dung'] = self.env['ir.sequence'].next_by_code('lich_su_su_dung') or 'New'
        return super(LichSuSuDung, self).create(vals)
