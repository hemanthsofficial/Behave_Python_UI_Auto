import openpyxl
import os

class ExcelWriter:
    @staticmethod
    def write_to_excel(filename="FlightHotelData.xlsx", sheet_name="Flights", data=[]):
        if os.path.exists(filename):
            workbook = openpyxl.load_workbook(filename)
        else:
            workbook = openpyxl.Workbook()
            workbook.remove(workbook.active)

        if sheet_name in workbook.sheetnames:
            del workbook[sheet_name]

        sheet = workbook.create_sheet(title=sheet_name)

        for row in data:
            sheet.append(row)

        workbook.save(filename)
