import re
import time
# from odoo.report import report_sxw
from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.tools.misc import xlwt
from xlsxwriter.utility import xl_range
from xlsxwriter.utility import xl_rowcol_to_cell


class JamaahXlsx(models.AbstractModel):
    _name = 'report.nti_travel_umroh.cetak_jamaah_xls'
    _inherit = 'report.report_xlsx.abstract'
                    
    iter_x = 1
    iter_y = 2
    temp = []
    count = 1

    def __init__(self, pool, cr):
        self.temp = []

    def generate_xlsx_report(self, workbook, data, lines):

        format1 = workbook.add_format({
            'font_size': 11, 'align': "vcenter", 'bold': True, 'bg_color': '#fbf1b4', 'border': 1})
        format2 = workbook.add_format(
            {'font_size': 11, 'align': "vcenter", 'bold': True, 'bg_color': '#ffd39b', 'border': 1})
            
        sheet = workbook.add_worksheet( "Report Jamaah")
        sheet.set_column('A:Z', 20)
        sheet.write(2, 0, "No.", format1)
        sheet.write(2, 1, "KTP No.", format1)
        sheet.write(2, 2, "Passport Name", format1)
        sheet.write(2, 3, "Place of Birth", format1)
        sheet.write(2, 4, "Birth of Date", format1)
        sheet.write(2, 5, "Gender", format1)
        sheet.write(2, 6, "Passport No.", format1)
        sheet.write(2, 7, "Date Issued", format1)
        sheet.write(2, 8, "Date of Expiry", format1)
        sheet.write(2, 9, "Immigration", format1)
        sheet.write(2, 10, "Age", format1)
        sheet.write(2, 11, "Roomtype", format1)
        sheet.write(2, 12, "Pilgrim Mahram", format1)
        sheet.write(2, 13, "Agent", format1)

        for obj in lines:
            
            for person in obj.peserta_line :
            
                self.iter_y += 1
                self.temp.append(person.no_identitas)
                self.temp.append(person.name)
                self.temp.append(person.place_of_birth)
                self.temp.append(person.date_of_birth.strftime("%d/%b/%Y"))
                self.temp.append(self.forgender(person.gender))
                self.temp.append(person.pass_no)
                self.temp.append(person.tgl_dibuat.strftime("%d/%b/%Y"))
                self.temp.append(person.masa_berlaku.strftime("%d/%b/%Y"))
                

                sheet.write(self.iter_y, self.iter_x - 1, self.count)
                for datareport in self.temp:
                    sheet.write(self.iter_y, self.iter_x, datareport)

                    self.iter_x += 1
                self.count += 1
                self.temp = []
                self.iter_x = 1

        self.count = 1
        self.generate_hotelline_report(sheet, self.iter_x, self.iter_y, lines, format2)
        
        self.count = 1
        self.generate_airline_report(sheet, self.iter_x, self.iter_y, lines, format2)
            

    def generate_hotelline_report(self, sheets, iteration_x, iteration_y, lines, formatxls):
        iteration_y += 2
        sheets.write(iteration_y, 0, "No.", formatxls)
        sheets.write(iteration_y, 1, "Hotel Name", formatxls)
        sheets.write(iteration_y, 2, "Check In", formatxls)
        sheets.write(iteration_y, 3, "Check Out", formatxls)
        sheets.write(iteration_y, 4, "City", formatxls)

        for obj in lines:
            
            for hotel in obj.hotel_line:
                iteration_y += 1
                self.temp.append(hotel.partner_id.commercial_company_name)
                self.temp.append(hotel.tgl_awal.strftime("%d/%b/%Y"))
                self.temp.append(hotel.tgl_akhir.strftime("%d/%b/%Y"))
                self.temp.append(hotel.kota)
                sheets.write(iteration_y, iteration_x - 1, self.count)

                for datareport in self.temp:
                    sheets.write(iteration_y, iteration_x, datareport)
                    iteration_x += 1
                self.count += 0
                self.temp = []
                iteration_x = 1
                
        

    def generate_airline_report(self, sheets, iteration_x, iteration_y, lines, formatxls):
        iteration_y += 2
        iteration_x += 7

        sheets.write(iteration_y, 7, "No.", formatxls)
        sheets.write(iteration_y, 8, "Airline Name", formatxls)
        sheets.write(iteration_y, 9, "Departure Date", formatxls)
        sheets.write(iteration_y, 10, "Departure City", formatxls)
        sheets.write(iteration_y, 11, "Arrival City", formatxls)
        for obj in lines:
            
            for airline in obj.pesawat_line:

                iteration_y += 1
                self.temp.append(airline.partner_id.commercial_company_name)
                self.temp.append(airline.tgl_berangkat.strftime("%d/%b/%Y"))
                self.temp.append(airline.kota_asal)
                self.temp.append(airline.kota_tujuan)

                sheets.write(iteration_y, iteration_x - 1, self.count)

                for datareport in self.temp:
                    sheets.write(iteration_y, iteration_x, datareport)
                    iteration_x += 1
                    
                self.count += 1
                self.temp = []
                iteration_x = 8


    def forgender(self, line):
        if line == "m":
            return "Male"
        else:
            return "Female"

    # def format_nulls(self, line):
    #     if not line:
    #         return ""
    #     elif line is int and line == 0:
    #         return "-"
    #     else:
    #         return line

    # def forroomtype(self, line):
    #     if line == "d":
    #         return "Double"
    #     if line == "t":
    #         return "Triple"
    #     if line == "q":
    #         return "Quad"
    #     else: return "Single"
