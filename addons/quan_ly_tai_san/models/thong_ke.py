from odoo import models, fields, api


class ThongKeTaiSan(models.Model):
    _name = 'thong_ke'
    _description = 'Thống kê tài sản'
    _auto = False  # Model ảo, không tạo bảng trong DB

    tai_san_id = fields.Many2one('tai_san', string="Tài sản", readonly=True)
    trang_thai = fields.Selection(related='tai_san_id.trang_thai', string="Trạng thái", readonly=True)
    loai_tai_san_id = fields.Many2one(related='tai_san_id.loai_tai_san_id', string="Loại tài sản", readonly=True)
    vi_tri_hien_tai_id = fields.Many2one(related='tai_san_id.vi_tri_hien_tai_id', string="Vị trí hiện tại", readonly=True)
    nha_cung_cap_id = fields.Many2one(related='tai_san_id.nha_cung_cap_id', string="Nhà cung cấp", readonly=True)
    gia_tien_mua = fields.Float(related='tai_san_id.gia_tien_mua', string="Giá mua", readonly=True)
    gia_tri_hien_tai = fields.Float(related='tai_san_id.gia_tri_hien_tai', string="Giá trị hiện tại", readonly=True)
    ngay_mua = fields.Datetime(related='tai_san_id.ngay_mua', string="Ngày mua", readonly=True)
    ngay_het_han_bao_hanh = fields.Date(related='tai_san_id.ngay_het_han_bao_hanh', string="Ngày hết bảo hành", readonly=True)
    ngay_thanh_ly = fields.Date(related='tai_san_id.thanh_ly_id.ngay_thanh_ly', string="Ngày thanh lý", readonly=True)
    gia_tri_thanh_ly = fields.Float(related='tai_san_id.thanh_ly_id.gia_tri_thanh_ly', string="Giá trị thanh lý", readonly=True)
    so_lan_su_dung = fields.Integer(string="Số lần sử dụng", compute='_compute_so_lan_su_dung', readonly=True)
    so_lan_bao_tri = fields.Integer(string="Số lần bảo trì", compute='_compute_so_lan_bao_tri', readonly=True)
    tong_chi_phi_bao_tri = fields.Float(string="Tổng chi phí bảo trì", compute='_compute_tong_chi_phi_bao_tri', readonly=True)

    @api.depends('tai_san_id')
    def _compute_so_lan_su_dung(self):
        for record in self:
            record.so_lan_su_dung = len(record.tai_san_id.lich_su_su_dung_ids)

    @api.depends('tai_san_id')
    def _compute_so_lan_bao_tri(self):
        for record in self:
            record.so_lan_bao_tri = len(record.tai_san_id.lich_su_bao_tri_ids)

    @api.depends('tai_san_id')
    def _compute_tong_chi_phi_bao_tri(self):
        for record in self:
            record.tong_chi_phi_bao_tri = sum(record.tai_san_id.lich_su_bao_tri_ids.mapped('chi_phi'))

    @api.model
    def init(self):
        self._cr.execute("""
            CREATE OR REPLACE VIEW thong_ke_tai_san AS (
                SELECT 
                    ts.id AS id,
                    ts.id AS tai_san_id,
                    ts.trang_thai,
                    ts.loai_tai_san_id,
                    ts.vi_tri_hien_tai_id,
                    ts.nha_cung_cap_id,
                    ts.gia_tien_mua,
                    ts.gia_tri_hien_tai,
                    ts.ngay_mua,
                    ts.ngay_het_han_bao_hanh,
                    tl.ngay_thanh_ly,
                    tl.gia_tri_thanh_ly
                FROM tai_san ts
                LEFT JOIN thanh_ly tl ON ts.thanh_ly_id = tl.id
            )
        """)