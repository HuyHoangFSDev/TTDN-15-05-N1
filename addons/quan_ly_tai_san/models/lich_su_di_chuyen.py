from odoo import models, fields, api

class LichSuDiChuyen(models.Model):
    _name = 'lich_su_di_chuyen'
    _description = 'Lịch sử điều chuyển tài sản'
    _order = 'ngay_di_chuyen desc'

    tai_san_id = fields.Many2one(
        comodel_name='tai_san',
        string="Tài sản",
        required=True,
        ondelete='cascade'
    )
    vi_tri_id = fields.Many2one(
        comodel_name='vi_tri',
        string="Vị trí",
        required=True
    )
    ngay_di_chuyen = fields.Date(
        "Ngày điều chuyển",
        default=fields.Date.context_today,
        required=True
    )
    ghi_chu = fields.Char("Ghi chú")

    @api.model
    def create(self, vals):
        tai_san = self.env['tai_san'].browse(vals['tai_san_id'])
        tai_san.write({'vi_tri_hien_tai_id': vals['vi_tri_id']})
        return super(LichSuDiChuyen, self).create(vals)