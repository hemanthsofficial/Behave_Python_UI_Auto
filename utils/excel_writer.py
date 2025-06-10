import openpyxl
import os

from utils.logger import get_logger
logger = get_logger(__name__)


class ExcelWriter:
    @staticmethod
    def write_to_excel(filename="FlightHotelData.xlsx", sheet_name="Flights", data=[]):
        try:
            logger.info(f"Writing to Excel: {filename}, Sheet: {sheet_name}")
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
            logger.info(f"Excel saved successfully: {filename}")
        except Exception as e:
            logger.error(f"Failed to write to Excel file: {e}", exc_info=True)
            raise
