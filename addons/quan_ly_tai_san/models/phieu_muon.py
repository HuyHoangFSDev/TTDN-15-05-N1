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
    ngay_muon_du_kien = fields.Date("Ngày mượn dự kiến", required=True,
                                    states={'approved': [('readonly', True)], 'done': [('readonly', True)],
                                            'cancelled': [('readonly', True)]})
    ngay_muon_thuc_te = fields.Date("Ngày mượn thực tế",
                                    states={'approved': [('readonly', True)], 'done': [('readonly', True)],
                                            'cancelled': [('readonly', True)]})
    ngay_tra_du_kien = fields.Date("Ngày trả dự kiến", required=True,
                                   states={'approved': [('readonly', True)], 'done': [('readonly', True)],
                                           'cancelled': [('readonly', True)]})
    ngay_tra_thuc_te = fields.Date("Ngày trả thực tế",
                                   states={'approved': [('readonly', True)], 'done': [('readonly', True)],
                                           'cancelled': [('readonly', True)]})
    ghi_chu = fields.Char("Ghi chú", states={'approved': [('readonly', True)], 'done': [('readonly', True)],
                                             'cancelled': [('readonly', True)]})
    nhan_vien_id = fields.Many2one(comodel_name="nhan_vien", string="Nhân sự", required=True, store=True,
                                   states={'approved': [('readonly', True)], 'done': [('readonly', True)],
                                           'cancelled': [('readonly', True)]})
    tai_san_id = fields.Many2one(
        comodel_name="tai_san",
        string="Tài sản",
        required=True,
        store=True,
        domain=[('trang_thai', '=', 'LuuTru')],
        states={
            'approved': [('readonly', True)],
            'done': [('readonly', True)],
            'cancelled': [('readonly', True)]
        }
    )
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
                self.env['lich_su_su_dung'].create({
                    'ma_lich_su_su_dung': self.env['ir.sequence'].next_by_code('lich_su_su_dung') or 'New',
                    'ngay_muon': record.ngay_muon_du_kien,
                    'ngay_tra': record.ngay_tra_du_kien,
                    'ghi_chu': record.ghi_chu,
                    'nhan_vien_id': record.nhan_vien_id.id,
                    'tai_san_id': record.tai_san_id.id,
                })
                record.state = 'approved'
                record.tai_san_id.write({
                    'trang_thai': 'Muon'
                })

    def action_done(self):
        for record in self:
            if record.state == 'approved':
                record.state = 'done'
                lich_su = self.env['lich_su_su_dung'].search([
                    ('nhan_vien_id', '=', record.nhan_vien_id.id),
                    ('tai_san_id', '=', record.tai_san_id.id),
                    ('ngay_muon', '=', record.ngay_muon_du_kien),
                    ('ngay_tra', '=', record.ngay_tra_du_kien)
                ], limit=1)
                if lich_su:
                    lich_su.write({
                        'ngay_muon': record.ngay_muon_thuc_te,
                        'ngay_tra': record.ngay_tra_thuc_te
                    })

    def action_cancel(self):
        for record in self:
            if record.state in ['draft', 'approved']:
                lich_su_su_dung = self.env['lich_su_su_dung'].search([
                    ('nhan_vien_id', '=', record.nhan_vien_id.id),
                    ('tai_san_id', '=', record.tai_san_id.id),
                    ('ngay_muon', '=', record.ngay_muon_du_kien),
                    ('ngay_tra', '=', record.ngay_tra_du_kien),
                    ('ghi_chu', '=', record.ghi_chu)
                ])
                if lich_su_su_dung:
                    lich_su_su_dung.unlink()
                record.state = 'cancelled'
                record.tai_san_id.write({
                    'trang_thai': 'LuuTru'
                })

    def action_reset_to_draft(self):
        for record in self:
            if record.state == 'cancelled':
                record.state = 'draft'
                record.tai_san_id.write({
                    'trang_thai': 'LuuTru'
                })
