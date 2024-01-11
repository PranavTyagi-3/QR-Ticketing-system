# from flask import Flask, render_template
# import qrcode
# from PIL import Image, ImageDraw, ImageFont
# import openpyxl

# app = Flask(__name__)

def generate_tickets():
    base_image_path = "static/Ticket_Templates/"
    base_image = Image.open(base_image_path)

    font_size = 35
    font = ImageFont.truetype("arialbd.ttf", font_size)

    excel_file_path = "data.xlsx"  
    data_names = {}

    workbook = openpyxl.load_workbook(excel_file_path)
    sheet = workbook.active

    for row in sheet.iter_rows(values_only=True):
        reg_number, name = row
        data_names[reg_number] = name

    for reg_number, name in data_names.items():
        qr = qrcode.QRCode(
            version=2,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=10,
            border=1,
        )
        qr.add_data(reg_number)
        qr.make(fit=True)
        qr_image = qr.make_image(fill_color="black", back_color="white")
        qr_image = qr_image.resize((400, 400))

        final_image = base_image.copy()
        final_image.paste(qr_image, (final_image.width - qr_image.width - 200, final_image.height - qr_image.height - 30))

        draw = ImageDraw.Draw(final_image)
        name_position = (160, final_image.height - 275)
        reg_number_position = (160, final_image.height - 220)

        draw.text(name_position, name, fill=(255, 255, 255), font=font)
        draw.text(reg_number_position, reg_number, fill=(255, 255, 255), font=font)

        output_path = fr"Generated_Tickets/{reg_number}.png"
        final_image.save(output_path)

    print("Tickets generated with bolded name and registration number!")

# # Define a Flask route for ticket generation
# @app.route('/generate_tickets')
# def generate_tickets_route():
#     generate_tickets()
#     return "Tickets generated with bolded name and registration number!"

# if __name__ == '__main__':
#     app.run(debug=True)