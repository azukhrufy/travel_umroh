# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit =  ['res.partner','mail.thread']
    _name = 'res.partner'
    _description = 'Model untuk pendaftaran jamaah umroh'
    
    # membuat field tambahan untuk melengkapi field customer
    # bertujuan untuk mengkustom beberapa field agar dapat mengakomodir pendaftaran jamaah
    no_identitas = fields.Char(string='No.KTP')
    father_name = fields.Char(string="Nama Ayah")
    mother_name = fields.Char(string="Nama Ibu")
    place_of_birth = fields.Char(string='Tempat Lahir')
    date_of_birth = fields.Date(string='Tanggal Lahir')
    
    pass_no = fields.Char(string='Passport Number')
    name = fields.Char(string='Name in Passport')
    tgl_dibuat = fields.Date(string='Date Issued')
    masa_berlaku = fields.Date(string='Date of Expiry')
    
    
    # scan document 
    ktp_scan = fields.Binary(string='Scan KTP')
    passport_scan = fields.Binary(string='Scan Passport')
    antigen_scan = fields.Binary(string='Scan Antigen Test')
    
    blood_type = fields.Selection([
        ('a', 'A'),
        ('ab', 'AB'),
        ('b', 'B'),
        ('o', 'O')
    ], string='Golongan Darah')
    gender = fields.Selection([
        ('pria', 'Pria'),
        ('wanita', 'Wanita')
    ], string='Jenis Kelamin')
    marital_status = fields.Selection([
        ('belum', 'Single'),
        ('menikah', 'Menikah'),
        ('cerai', 'Cerai'),
    ], string='Status Pernikahan')
    
    clothes_size = fields.Selection([
        ('s', 'S'),
        ('m', 'M'),
        ('l', 'L'),
        ('xl', 'XL'),
    ], string='Ukuran Baju')
    
    education = fields.Selection([
        ('sd', 'SD'),
        ('smp', 'SMP'),
        ('sma', 'SMA'),
        ('diploma', 'Diploma'),
        ('sarjana', 'Sarjana'),
        ('magister', 'Magister'),
    ], string='Pendidikan Terakhir')
    
    # untuk nambah field is airlines or is hotels
    
    is_airlines = fields.Boolean(string='Airlines')
    is_hotel = fields.Boolean(string='Hotel')
    
    
    
class PaketPerjalanan(models.Model):
    
    _name = 'paket.perjalanan'
    _inherit = 'mail.thread'
    _description = 'Paket Perjalanan untuk informasi seputar paket perjalanan yang ditawarkan'
    
    # membuat field yang dibutuhkan dalam penamaan paket perjalanan
    name = fields.Char(string='Reference', readonly=True, default='/')
    product_id = fields.Many2one('product.product', string='Product', required=True)
    package_id = fields.Many2one('product.template', string='Paket', required=True)
    
    bom_id = fields.Many2one('mrp.bom', string='Nomenclature')
    
    tgl_berangkat = fields.Date(string='Departure Date', required=True)
    tgl_pulang = fields.Date(string='Return Date', required=True)
    quota = fields.Integer(string='Quota' ,)
    quota_progress = fields.Float(string='Quota Progress', compute='_taken_seats')
    note = fields.Text(string='Notes')
    remaining_seats = fields.Integer(string='Remaining Seats', compute='_remaining_seats')
    total = fields.Float(string='Total', compute='_total')
    
    # list of one2many fields, please use _line on the name of field
    hotel_line = fields.One2many('paket.hotel.line', 'paket_perjalanan_id', string='List Hotel')
    pesawat_line = fields.One2many('paket.pesawat.line', 'paket_perjalanan_id', string='Daftar Pesawat')
    acara_line = fields.One2many('paket.acara.line', 'paket_perjalanan_id', string='List Kegiatan')
    peserta_line = fields.One2many('paket.peserta.line', 'paket_perjalanan_id', string='Daftar Peserta')
    package_line = fields.One2many('hpp.line', 'package_id', string='Hpp line')
    
    # field untuk mengatur state pra / pasca approval
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirmed'),
        ('done','Done')
    ], string='Status', readonly=True, copy=False, default='draft', track_visibility='onchange')
    
    @api.multi
    def update_jamaah(self):
        order_ids = self.env['sale.order'].search([('paket_perjalanan_id', '=', self.id), ('state', 'not in', ('draft', 'cancel'))])
        if order_ids:
            self.peserta_line.unlink()
            for o in order_ids:
                for x in o.passport_line:
                    self.peserta_line.create({
                        'paket_perjalanan_id': self.id,
                        'no_identitas': x.partner_id.no_identitas,
                        'date_of_birth': x.partner_id.date_of_birth,
                        'place_of_birth': x.partner_id.place_of_birth,
                        'pass_no': x.partner_id.pass_no,
                        'masa_berlaku': x.partner_id.masa_berlaku,
                        'tgl_dibuat': x.partner_id.tgl_dibuat,
                        'partner_id': x.partner_id.id,
                        'name': x.name,
                        'order_id': o.id,
                        'gender': x.partner_id.gender,
                        'tipe_kamar': x.tipe_kamar,
                    })
    
    @api.onchange('package_id')
    def onchange_package_id(self):
        if self.package_id:
            lines = [(5, 0, 0)]
            # for rec in self:
            for line in self.package_id.bom_ids.bom_line_ids:
                vals = {
                    'product_id': line.product_id,
                    'product_qty': line.product_qty,
                }
                lines.append([0,0,vals])
            self.package_line = lines
            
    @api.depends('package_line')
    def _total(self):
        if self.package_line:
            self.total = 0
            for r in self.package_line:
                self.total = self.total + r.subtotal
                    
    @api.depends('quota','peserta_line')
    def _remaining_seats(self):
        if self.quota:
            for r in self:
                if not r.peserta_line:
                    self.remaining_seats = r.quota
                else:
                    self.remaining_seats = r.quota - len(r.peserta_line)

    
    @api.multi
    def action_confirm(self):
        self.write({'state': 'confirm'})
        
    
    @api.multi
    def action_done(self):
        self.write({'state': 'done'})
    
    
    # sequence auto numbering u/ mengisi field (reference name)
    @api.model
    def create(self,vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('paket.perjalanan')
        return super(PaketPerjalanan, self).create(vals)
    
    # membuat nama display dari field name dan product
    @api.multi 
    def name_get(self):
        return [(this.id, this.name + "#" + " " + this.product_id.partner_ref) for this in self]
    
    @api.depends('quota','peserta_line')
    def _taken_seats(self):
        for r in self:
            if not r.quota:
                r.quota_progress = 0.0
            else:
                r.quota_progress = 100.0 * len(r.peserta_line) / r.quota
                
    @api.multi
    def cetak_jamaah_xlsx(self):
        return self.env.ref("nti_travel_umroh.cetak_jamaah_xls").report_action(self)
                



# untuk mencatat semua hotel yang digunakan selama program
class PaketHotelLine(models.Model):
    _name = 'paket.hotel.line'
    _inherit = 'mail.thread'
    _description = 'Paket Hotel Line'
    
    paket_perjalanan_id = fields.Many2one('paket.perjalanan', string='Paket Perjalanan')
    partner_id = fields.Many2one('res.partner', string='Hotel', domain=[
        ("is_hotel", "=", True),
    ], required=True)
    tgl_awal = fields.Date(string='Start Date', required=True)
    tgl_akhir = fields.Date(string='End Date', required=True)
    kota = fields.Char(string='City', related='partner_id.city', readonly=True)


# untuk mencatat semua pesawat yang digunakan
class PaketPesawatLine(models.Model):
    _name = 'paket.pesawat.line'
    _inherit = 'mail.thread'
    _description = 'Paket Pesawat Line'

    paket_perjalanan_id = fields.Many2one('paket.perjalanan', string='Paket Perjalanan', ondelete='cascade')
    partner_id = fields.Many2one('res.partner', string='Airlines', domain=[
        ("is_airlines", "=", True),
    ], required=True)
    tgl_berangkat = fields.Date(string='Departure Date', required=True)
    kota_asal = fields.Char(string='Departure City', required=True)
    kota_tujuan = fields.Char('Arrival City', required=True)
    

# untuk mencatat semua jadwal pada saat pelaksanaan paket umroh
class PaketAcaraLine(models.Model):
    _name = 'paket.acara.line'
    _inherit = 'mail.thread'
    _description = 'Paket Acara Line'
    
    paket_perjalanan_id = fields.Many2one('paket.perjalanan', string='Paket Perjalanan', ondelete='cascade')
    name = fields.Char(string='Name', required=True)
    tgl = fields.Date(string='Date', required=True)
    

# untuk mencatat semua peserta umroh
class PaketPesertaLine(models.Model):
    _name = 'paket.peserta.line'
    _inherit = 'mail.thread'
    _description = 'Paket Peserta Line'
    
    paket_perjalanan_id = fields.Many2one('paket.perjalanan', string='Paket Perjalanan', ondelete='cascade')
    
    partner_id = fields.Many2one('res.partner', domain=[
        ("customer", "=", True),
    ], string='Jamaah')
    
    name = fields.Char(string='Name in Passport')
    
    order_id = fields.Many2one('sale.order', string='Sales Orders')
    gender = fields.Selection([('pria', 'Pria'),
        ('wanita', 'Wanita')], string='Gender')
    tipe_kamar = fields.Selection([('d', 'Double'), ('t', 'Triple'), ('q', 'Quad')], string='Room Type')
    
    # field dari res partner
    pass_no = fields.Char(string='Passport Number')
    no_identitas = fields.Char(string='No.KTP')
    place_of_birth = fields.Char(string='Tempat Lahir')
    date_of_birth = fields.Date(string='Tanggal Lahir')
    tgl_dibuat = fields.Date(string='Date Issued')
    masa_berlaku = fields.Date(string='Date of Expiry')
    
class HppLine(models.Model):
    _name = 'hpp.line'
    _description = 'Hpp Line'
    
    
    package_id = fields.Many2one('paket.perjalanan',string='Paket Perjalanan', ondelete='cascade')
    product_id = fields.Many2one('product.product',string='List Product', ondelete='cascade')
    product_qty = fields.Float(string='Product Qty')
    
    
    product_price = fields.Float(string='Price')
    subtotal = fields.Float(string='Subtotal')
    total = fields.Float(string='Total')
    
    @api.onchange('product_price', 'product_qty', 'total')
    def onchange_subtotal(self):
        if self.product_price:
            self.subtotal = self.product_price * self.product_qty
            self.total = self.subtotal + self.total
        
        



class SaleOrder(models.Model):
    _inherit = ['sale.order','mail.thread']
    _name = 'sale.order'
    _description = 'Sale Order'
    
    
    # custom field yang diperlukan untuk mengakomodasi travel umroh
    
    # menampilkan paket perjalanan yang telah di confirm
    paket_perjalanan_id = fields.Many2one('paket.perjalanan', string='Paket Perjalanan', domain=[
        ("state", "=", 'confirm'),
    ],)
    
    dokumen_line = fields.One2many('sale.dokumen.line', 'order_id', string='Dokumen Line')
    passport_line = fields.One2many('sale.passport.line', 'order_id', string='Passport Line')
    
    @api.onchange('paket_perjalanan_id')
    def set_order_line(self):
        res = {}
        if self.paket_perjalanan_id:
            pp = self.paket_perjalanan_id
            
            # nilai order di set otomatis dari method on change product_id_change()
            order = self.env['sale.order'].new({
                'partner_id' : self.partner_id.id,
                'pricelist_id' : self.pricelist_id.id,
                'date_order' : self.date_order
            })
            
            line = self.env['sale.order.line'].new({'product_id' : pp.product_id.id, 'order_id' : order.id})
            line.product_id_change()
            vals = line._convert_to_write({name : line[name] for name in line._cache})
            res['value'] = {'order_line' : [vals]}
        return res


class SaleDokumenLine(models.Model):
    _name = 'sale.dokumen.line'
    _inherit = 'mail.thread'
    _description = 'Sale Dokumen Line'
    
    order_id = fields.Many2one('sale.order', string='Sales Order', ondelete='cascade')
    name = fields.Char(string='Name', required=True)
    photo = fields.Binary(string='Photo', required=True)
    

class SalePassportLine(models.Model):
    _name = 'sale.passport.line'
    _inherit = 'mail.thread'
    _description = 'Sale Passport Line'
    
    order_id = fields.Many2one('sale.order', string='Sales Orders', ondelete='cascade')
    partner_id = fields.Many2one('res.partner', string='Jamaah', required=True, domain=[
        ("customer", "=", True),
    ],)
    
    # bagian personal jamaah 
    no_identitas = fields.Char(string='No KTP', related="partner_id.no_identitas", readonly=True)
    date_of_birth = fields.Date(string='Tanggal Lahir', related="partner_id.date_of_birth", readonly=True)    
    place_of_birth = fields.Char(string='Tempat Lahir', related="partner_id.place_of_birth", readonly=True)
    
    
    # bagian passport jamaah 
    pass_no = fields.Char(string='Passport Number', required=True, related="partner_id.pass_no", readonly=True)
    name = fields.Char(string='Name in Passport', related="partner_id.name", readonly=True)
    masa_berlaku = fields.Date(string='Date of Expiry', required=True, related="partner_id.masa_berlaku", readonly=True)
    tipe_kamar = fields.Selection([
        ('d', 'Double'),
        ('t', 'Triple'),
        ('q', 'Quad'),
    ], string='Room Type')
    photo = fields.Binary(string='Photo', required=True)
    


