import re
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class PhieuMuon(models.Model):
    _name = 'phieu_muon'
    _description = 'Phiếu mượn tài sản'
    _order = 'ma_phieu_muon'
    _states = {
        'draft': 'Nháp',
        'approved': 'Đã duyệt',
        'done': 'Hoàn thành',
        'cancelled': 'Hủy',
    }

    ma_phieu_muon = fields.Char("Mã phiếu mượn", required=True, copy=False, readonly=True, default="New",
                                states={'draft': [('readonly', False)]})
    ngay_muon = fields.Date("Ngày mượn", required=True,
                            states={'approved': [('readonly', True)], 'done': [('readonly', True)],
                                    'cancelled': [('readonly', True)]})
    ngay_tra = fields.Date("Ngày trả", required=True,
                           states={'approved': [('readonly', True)], 'done': [('readonly', True)],
                                   'cancelled': [('readonly', True)]})
    ghi_chu = fields.Char("Ghi chú", states={'approved': [('readonly', True)], 'done': [('readonly', True)],
                                             'cancelled': [('readonly', True)]})
    nhan_vien_id = fields.Many2one(comodel_name="nhan_vien", string="Nhân sự", required=True, store=True,
                                   states={'approved': [('readonly', True)], 'done': [('readonly', True)],
                                           'cancelled': [('readonly', True)]})
    tai_san_id = fields.Many2one(comodel_name="tai_san", string="Tài sản", required=True, store=True,
                                 states={'approved': [('readonly', True)], 'done': [('readonly', True)],
                                         'cancelled': [('readonly', True)]})
    state = fields.Selection(
        [('draft', 'Nháp'), ('approved', 'Đã duyệt'), ('done', 'Hoàn thành'), ('cancelled', 'Hủy')], default='draft',
        string="Trạng thái")

    @api.constrains('ma_phieu_muon')
    def _check_ma_phieu_muon_format(self):
        for record in self:
            if not re.fullmatch(r'PM-\d{4}', record.ma_phieu_muon):
                raise ValidationError("Mã phải có định dạng PM-XXXX (ví dụ: PM-1234)")

    @api.model
    def create(self, vals):
        if vals.get('ma_phieu_muon', 'New') == 'New':
            vals['ma_phieu_muon'] = self.env['ir.sequence'].next_by_code('phieu_muon') or 'New'
        return super(PhieuMuon, self).create(vals)

    def action_approve(self):
        for record in self:
            if record.state == 'draft':
                # Tạo bản ghi lịch sử sử dụng khi duyệt
                self.env['lich_su_su_dung'].create({
                    'ma_lich_su_su_dung': self.env['ir.sequence'].next_by_code('lich_su_su_dung') or 'New',
                    'ngay_muon': record.ngay_muon,
                    'ngay_tra': record.ngay_tra,
                    'ghi_chu': record.ghi_chu,
                    'nhan_vien_id': record.nhan_vien_id.id,
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
                lich_su_su_dung = self.env['lich_su_su_dung'].search([
                    ('nhan_vien_id', '=', record.nhan_vien_id.id),
                    ('tai_san_id', '=', record.tai_san_id.id),
                    ('ngay_muon', '=', record.ngay_muon),
                    ('ngay_tra', '=', record.ngay_tra),
                    ('ghi_chu', '=', record.ghi_chu)
                ])
                if lich_su_su_dung:
                    lich_su_su_dung.unlink()
                record.state = 'cancelled'

    def action_reset_to_draft(self):
        for record in self:
            if record.state in ['approved', 'cancelled']:
                record.state = 'draft'