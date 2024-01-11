# from flask import Flask, render_template
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import os
import pandas as pd
from fpdf import FPDF

# app = Flask(__name__)

def send_certificates(excel_file_path,):
    # Gmail SMTP server settings
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = 'vitronixvitb@gmail.com'
    smtp_password = 'xeysguoyoktavebj'  # Generate an app password from your Google Account settings

    # Input Excel file path
    # excel_file_path = 'static/data/data.xlsx'  # Replace with your actual Excel file path
    try:
        # Read data from Excel into a DataFrame
        df = pd.read_excel(excel_file_path)

        # Convert DataFrame to dictionary
        recipient_data = dict(zip(df['email'], df['filename']))

        er = []

        # Connect to the Gmail SMTP server and send the emails
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)

        for to_email, pdf_filename in recipient_data.items():
            msg = MIMEMultipart()
            msg['From'] = smtp_username
            msg['To'] = to_email
            msg['Subject'] = 'Certificate for Your Participation in "EDGETRONIX" Event'

            body = """
            Dear Participant,
            ...
            """

            msg.attach(MIMEText(body, 'plain'))
            try:
                pdf_path = os.path.join('<FLASK_APP_PATH>/static/certificates', pdf_filename + '.pdf')  # Update the path accordingly

                # Create a PDF certificate
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", size=12)
                pdf.cell(200, 10, txt=f"Certificate for {pdf_filename}", ln=True, align='C')
                pdf.output(pdf_path)

                with open(pdf_path, 'rb') as pdf_file:
                    pdf_attachment = MIMEApplication(pdf_file.read(), _subtype="pdf")
                    pdf_attachment.add_header('content-disposition', 'attachment', filename=pdf_filename + '.pdf')
                    msg.attach(pdf_attachment)

                server.sendmail(smtp_username, to_email, msg.as_string())
                print(f"Email sent to {to_email} successfully!")
            except Exception as e:
                print(e)
                er.append(pdf_filename)

        # Generate a text file to track emails sent
        with open('static/email_status.txt', 'w') as status_file:  # Update the path accordingly
            for email, pdf_filename in recipient_data.items():
                status = "True" if pdf_filename not in er else "False"
                status_file.write(f"{pdf_filename}: {status}\n")

        server.quit()
    except Exception as e:
        print("Error:", str(e))

# Flask route for sending certificates
# @app.route('/send_certificates')
# def send_certificates_route():
#     send_certificates()
#     return "Certificates sent successfully!"

# if __name__ == '__main__':
#     app.run(debug=True)
