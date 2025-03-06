import re

from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError

class PhieuBaoTri(models.Model):
    _name = 'phieu_bao_tri'
    _description = 'Phiếu bảo trì tài sản'
    _order = 'ma_phieu_bao_tri'

    ma_phieu_bao_tri = fields.Char("Mã phiếu bảo trì", required=True)
    ngay_bao_tri = fields.Datetime("Ngày bảo trì dự kiến", required=True)
    ngay_bao_tri_thuc_te = fields.Datetime("Ngày bảo trì thực tế", required=False)
    ngay_tra = fields.Datetime("Ngày trả dự kiến", required=True)
    ngay_tra_thuc_te = fields.Datetime("Ngày trả thực tế", required=False)
    chi_phi = fields.Integer("Chi phí", required=True)
    ghi_chu = fields.Char("Ghi chú")
    tai_san_id = fields.Many2one(comodel_name="tai_san", string="Tài sản", required=True, store=True)
    state = fields.Selection(
        [('draft', 'Nháp'), ('approved', 'Đã duyệt'), ('done', 'Hoàn thành'), ('cancelled', 'Hủy')],
        default='draft', string="Trạng thái")

    def action_approve(self):
        for record in self:
            if record.state == 'draft':
                self.env['lich_su_bao_tri'].create({
                    'ma_lich_su_bao_tri': self.env['ir.sequence'].next_by_code('lich_su_bao_tri') or 'New',
                    'ngay_bao_tri': record.ngay_bao_tri,
                    'ngay_tra': record.ngay_tra,
                    'chi_phi': record.chi_phi,
                    'ghi_chu': record.ghi_chu,
                    'tai_san_id': record.tai_san_id.id,
                })
                record.state = 'approved'

    def action_done(self):
        for record in self:
            if record.state == 'approved':
                if not all([record.ngay_bao_tri_thuc_te, record.ngay_tra_thuc_te, record.chi_phi]):
                    raise UserError(_('Vui lòng nhập đầy đủ Ngày bảo trì thực tế, Ngày trả thực tế và Chi phí trước khi hoàn thành.'))
                record.state = 'done'
                lich_su = self.env['lich_su_bao_tri'].search([
                    ('tai_san_id', '=', record.tai_san_id.id),
                    ('ngay_bao_tri', '=', record.ngay_bao_tri),
                    ('ngay_tra', '=', record.ngay_tra),
                    ('chi_phi', '=', record.chi_phi),
                    ('ghi_chu', '=', record.ghi_chu)
                ], limit=1)
                if lich_su:
                    lich_su.write({
                        'ngay_bao_tri': record.ngay_bao_tri_thuc_te,
                        'ngay_tra': record.ngay_tra_thuc_te
                    })

    def action_cancel(self):
        for record in self:
            if record.state in ['draft', 'approved']:
                lich_su_bao_tri = self.env['lich_su_bao_tri'].search([
                    ('tai_san_id', '=', record.tai_san_id.id),
                    ('ngay_bao_tri', '=', record.ngay_bao_tri),
                    ('ngay_tra', '=', record.ngay_tra),
                    ('chi_phi', '=', record.chi_phi),
                    ('ghi_chu', '=', record.ghi_chu)
                ])
                if lich_su_bao_tri:
                    lich_su_bao_tri.unlink()
                record.state = 'cancelled'

    def action_reset_to_draft(self):
        for record in self:
            if record.state in ['approved', 'cancelled']:
                record.state = 'draft'
