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

    ma_khau_hao = fields.Char("Mã khấu hao", required=True, copy=False, readonly=True, default="New")
    ngay_khau_hao = fields.Date("Ngày khấu hao", required=True)
    gia_tri_khau_hao = fields.Integer("Giá trị khấu hao", required=True)
    ghi_chu = fields.Char("Ghi chú")
    tai_san_id = fields.Many2one(comodel_name="tai_san", string="Tài sản", store=True, required=True)

    @api.model
    def create(self, vals):
        if vals.get('ma_khau_hao', 'New') == 'New':
            vals['ma_khau_hao'] = self.env['ir.sequence'].next_by_code('khau_hao') or 'New'

        tai_san = self.env['tai_san'].browse(vals.get('tai_san_id'))
        if tai_san:
            gia_tri_hien_tai = tai_san.gia_tri_hien_tai or tai_san.gia_tien_mua or 0
            gia_tri_khau_hao = vals.get('gia_tri_khau_hao', 0)

            if gia_tri_khau_hao > gia_tri_hien_tai:
                raise ValidationError("Giá trị khấu hao không thể lớn hơn giá trị hiện tại của tài sản!")

            tai_san.write({'gia_tri_hien_tai': gia_tri_hien_tai - gia_tri_khau_hao})

        return super(KhauHao, self).create(vals)

    @api.constrains('gia_tri_khau_hao', 'tai_san_id')
    def _check_gia_tri_khau_hao(self):
        for record in self:
            if record.gia_tri_khau_hao <= 0:
                raise ValidationError("Giá trị khấu hao phải lớn hơn 0!")
            if record.tai_san_id:
                gia_tri_hien_tai = record.tai_san_id.gia_tri_hien_tai or record.tai_san_id.gia_tien_mua or 0
                if record.gia_tri_khau_hao > gia_tri_hien_tai:
                    raise ValidationError("Giá trị khấu hao không thể lớn hơn giá trị hiện tại của tài sản!")