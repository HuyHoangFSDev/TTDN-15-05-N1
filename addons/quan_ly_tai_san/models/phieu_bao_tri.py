import re
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class PhieuBaoTri(models.Model):
    _name = 'phieu_bao_tri'
    _description = 'Phiếu bảo trì tài sản'
    _order = 'ma_phieu_bao_tri'
    _states = {
        'draft': 'Nháp',
        'approved': 'Đã duyệt',
        'done': 'Hoàn thành',
        'cancelled': 'Hủy',
    }

    ma_phieu_bao_tri = fields.Char("Mã phiếu bảo trì", required=True, copy=False, readonly=True, default="New",
                                   states={'draft': [('readonly', False)]})
    ngay_bao_tri = fields.Date("Ngày bảo trì", required=True,
                               states={'approved': [('readonly', True)], 'done': [('readonly', True)],
                                       'cancelled': [('readonly', True)]})
    ngay_tra = fields.Date("Ngày trả", required=True,
                           states={'approved': [('readonly', True)], 'done': [('readonly', True)],
                                   'cancelled': [('readonly', True)]})
    chi_phi = fields.Integer("Chi phí", required=True,
                             states={'approved': [('readonly', True)], 'done': [('readonly', True)],
                                     'cancelled': [('readonly', True)]})
    ghi_chu = fields.Char("Ghi chú", states={'approved': [('readonly', True)], 'done': [('readonly', True)],
                                             'cancelled': [('readonly', True)]})
    tai_san_id = fields.Many2one(comodel_name="tai_san", string="Tài sản", required=True, store=True,
                                 states={'approved': [('readonly', True)], 'done': [('readonly', True)],
                                         'cancelled': [('readonly', True)]})
    state = fields.Selection(
        [('draft', 'Nháp'), ('approved', 'Đã duyệt'), ('done', 'Hoàn thành'), ('cancelled', 'Hủy')],
        default='draft', string="Trạng thái")

    @api.constrains('ma_phieu_bao_tri')
    def _check_ma_phieu_bao_tri_format(self):
        for record in self:
            if not re.fullmatch(r'PB-\d{4}', record.ma_phieu_bao_tri):
                raise ValidationError("Mã phải có định dạng PB-XXXX (ví dụ: PB-1234)")

    @api.model
    def create(self, vals):
        if vals.get('ma_phieu_bao_tri', 'New') == 'New':
            vals['ma_phieu_bao_tri'] = self.env['ir.sequence'].next_by_code('phieu_bao_tri') or 'New'
        return super(PhieuBaoTri, self).create(vals)

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
                record.state = 'done'

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
