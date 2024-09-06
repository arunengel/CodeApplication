import xlsxwriter
import json
import os
from django.conf import settings
import re

class ExcelService():
    def __init__(self):
        pass


    def create_excel(self, extracted_data, out_directory):
        print(repr(extracted_data))

        # Remove markdown formatting and clean the string
        cleaned_data = extracted_data.replace('```json\n', '').replace('\n```', '').replace('\x00', '').strip()

        print(cleaned_data)

        data = json.loads(cleaned_data)

        # Ensure the output directory exists
        os.makedirs(out_directory, exist_ok=True)

        # Construct the full file path
        file_path = os.path.join(out_directory, "Times.xlsx")

        output_path = os.path.join(settings.MEDIA_ROOT, 'processed', 'Transformed_Timesheet.xlsx')

        workbook = xlsxwriter.Workbook(file_path)

        workingHours = data['Times']
        name = data['Name']

        # To store the row index for each customer sheet
        customer_row_indices = {}


        for entry in workingHours:
            customer = entry['Customer']
    
            # Check if the customer already has a worksheet, if not, create it
            if customer not in customer_row_indices:
                cleanedCustomerName = re.sub(r'[\[\]\:\*\?\/\\]', '', customer) # Excel Worksheet names are not allowed to contain some characters
                if(len(cleanedCustomerName) > 31):
                    cleanedCustomerName = cleanedCustomerName[:31]
                worksheet = workbook.add_worksheet(cleanedCustomerName)
                # Write the header for the new worksheet
                worksheet.write(0, 0, "#")
                worksheet.write(0, 1, "Name")
                worksheet.write(0, 2, "Datum")
                worksheet.write(0, 3, "Stunden")
                worksheet.write(0, 4, "Notizen")
                # Start at row 1 for data entries (row 0 is for the header)
                customer_row_indices[customer] = 1
            else:
                worksheet = workbook.get_worksheet_by_name(cleanedCustomerName)
            
            # Get the current row index for the customer
            row = customer_row_indices[customer]
            
            # Write the data to the worksheet
            worksheet.write(row, 0, row)  # Or use a different unique identifier instead of row
            worksheet.write(row, 1, name)
            worksheet.write(row, 2, entry["Date"])
            worksheet.write(row, 3, entry["Hours"])
            worksheet.write(row, 4, entry["Notes"])
            
            # Increment the row index for this customer
            customer_row_indices[customer] += 1

        workbook.close()
        return file_path
        
""""
        customers = []
        for index, entry in enumerate(workingHours):
            if entry['Customer'] not in customers:
                customers = customers.append(entry['Customer'])
                worksheet = workbook.add_worksheet(entry['Customer'])
            worksheet.write(index+1, 0, index)
            worksheet.write(index+1, 1, name)
            worksheet.write(index+1, 2, entry["Date"])
            worksheet.write(index+1, 3, entry["Hours"])

        workbook.close()
        return file_path




        for index, entry in enumerate(workingHours):
            worksheet.write(index+1, 0, index)
            worksheet.write(index+1, 1, name)
            worksheet.write(index+1, 2, entry["Date"])
            worksheet.write(index+1, 3, entry["Hours"])
"""
                            
