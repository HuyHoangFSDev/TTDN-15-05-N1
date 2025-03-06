import re
from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError

class PhieuMuon(models.Model):
    _name = 'phieu_muon'
    _description = 'Phiếu mượn tài sản'
    _order = 'ma_phieu_muon'

    ma_phieu_muon = fields.Char("Mã phiếu mượn", required=True)
    ngay_muon_du_kien = fields.Datetime("Thời gian mượn dự kiến", required=True)
    ngay_muon_thuc_te = fields.Datetime("Thời gian mượn thực tế", required=False)
    ngay_tra_du_kien = fields.Datetime("Thời gian trả dự kiến", required=True)
    ngay_tra_thuc_te = fields.Datetime("Thời gian trả thực tế", required=False)
    ghi_chu = fields.Char("Ghi chú")
    nhan_vien_id = fields.Many2one(comodel_name="nhan_vien", string="Nhân sự", required=True, store=True)
    tai_san_id = fields.Many2one(
        comodel_name="tai_san",
        string="Tài sản",
        required=True,
        store=True,
        domain=[('trang_thai', '=', 'LuuTru')],
    )
    state = fields.Selection(
        [('draft', 'Nháp'), ('approved', 'Đã duyệt'), ('done', 'Hoàn thành'), ('cancelled', 'Hủy')],
        default='draft', string="Trạng thái")
    trang_thai_muon = fields.Char('Trạng thái mượn', compute='_compute_trang_thai_muon', store=True)



    @api.depends('ngay_muon_du_kien', 'ngay_muon_thuc_te', 'ngay_tra_du_kien', 'ngay_tra_thuc_te')
    def _compute_trang_thai_muon(self):
        for record in self:
            muon_do_muon = (
                record.ngay_muon_thuc_te
                and record.ngay_muon_du_kien
                and record.ngay_muon_thuc_te > record.ngay_muon_du_kien
            )
            tra_do_muon = (
                record.ngay_tra_thuc_te
                and record.ngay_tra_du_kien
                and record.ngay_tra_thuc_te > record.ngay_tra_du_kien
            )
            if muon_do_muon and tra_do_muon:
                record.trang_thai_muon = 'Mượn muộn và trả muộn'
            elif muon_do_muon:
                record.trang_thai_muon = 'Mượn muộn'
            elif tra_do_muon:
                record.trang_thai_muon = 'Trả muộn'
            elif record.ngay_muon_thuc_te and record.ngay_tra_thuc_te:
                record.trang_thai_muon = 'Đúng hạn'
            elif record.ngay_muon_thuc_te:
                record.trang_thai_muon = 'Đang mượn'
            else:
                record.trang_thai_muon = 'Chưa mượn'

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
                    'trang_thai': 'Muon',
                    'nguoi_dang_dung_id': record.nhan_vien_id.id
                })

    def action_done(self):
        for record in self:
            if record.state == 'approved':
                if not record.ngay_muon_thuc_te or not record.ngay_tra_thuc_te:
                    raise UserError('Vui lòng nhập Ngày mượn thực tế và Ngày trả thực tế trước khi hoàn thành.')
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
                record.tai_san_id.write({
                    'trang_thai': 'LuuTru',
                    'nguoi_dang_dung_id': False
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
                    'trang_thai': 'LuuTru',
                    'nguoi_dang_dung_id': False
                })

    def action_reset_to_draft(self):
        for record in self:
            if record.state == 'cancelled':
                record.state = 'draft'
                record.tai_san_id.write({
                    'trang_thai': 'LuuTru',
                    'nguoi_dang_dung_id': False
                })