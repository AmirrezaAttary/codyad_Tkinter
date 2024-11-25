# from persiantools.jdatetime import JalaliDate
# import datetime

# print(JalaliDate.today())

# miladi = JalaliDate(1396,7,1).to_gregorian()

# print(miladi)

# import sqlite3
# data_person_name = [('amirrr','attary')]

# con = sqlite3.connect("pz.db")



# c = con.cursor()

# c.execute('''create table if not exists q1_person_name
#                  (name_id INTEGER PRIMARY KEY,
#                   first_name varchar(20) NOT NULL,
#                   last_name varchar(20) NOT NULL)''')
# c.executemany('INSERT INTO q1_person_name(first_name, last_name) VALUES (?,?)', data_person_name)
# a= [59849,416513,4896451]
# for j in a:
#     c.execute(f'DELETE FROM paziresh WHERE tel = "{j}"')
    
# list_person_name = []
# for row in c.execute('SELECT tel FROM paziresh '):
#     a = list(row)
#     list_person_name.append(a)
# # print(list_person_name)
# for i in list_person_name:
#     a= int(i[0])
#     print(a)
# b = a[0]
# b=int(b)
# print(b)
# con.commit()
# con.close()

# import sqlite3

# conn = sqlite3.connect('memo.db')
# cursor = conn.cursor()

# a=cursor.execute("SELECT name_id FROM q1_person_name ORDER BY name_id DESC LIMIT 1")
# last_id = cursor.lastrowid
# print(a)

# conn.commit()
# cursor.close()
# conn.close()

# import sqlite3 
# import io 
# conn = sqlite3.connect('pz.db') 

# # Open() function 
# with io.open('backupdatabase_dumpp.sql', 'w' ,encoding='utf-8') as p: 
		
# 	# iterdump() function 
# 	for line in conn.iterdump(): 
		
# 		p.write('%s\n' % line) 
	
# print(' Backup performed successfully!') 
# print(' Data Saved as backupdatabase_dump.sql') 

# conn.close() 


# for row in c.execute('SELECT * FROM paziresh '):
#     print(row)

# con.commit()
# con.close()

# from win32printing import Printer

# font = {
#     "height": 8,
# }
# with Printer(linegap=1) as printer:
#     printer.text("title1", font_config=font)
#     printer.text("title2", font_config=font)
#     printer.text("title3", font_config=font)
#     printer.text("title4", font_config=font)
#     printer.new_page()
#     printer.text("title5", font_config=font)
#     printer.text("title6", font_config=font)
#     printer.text("title7", font_config=font)
#     printer.text("title8", font_config=font)


# importing modules 
# importing modules 


# from reportlab.pdfgen import canvas 
# from reportlab.pdfbase.ttfonts import TTFont 
# from reportlab.pdfbase import pdfmetrics 
# from reportlab.lib import colors 

# # initializing variables with values 
# fileName = 'sample.pdf'
# documentTitle = 'sample'
# title = 'Technology'
# subTitle = 'The largest thing now!!'
# textLines = [ 
# 	'Technology makes us aware of', 
# 	'the world around us.', 
# ] 
# image = 'image.jpg'

# # creating a pdf object 
# pdf = canvas.Canvas(fileName) 

# # setting the title of the document 
# pdf.setTitle(documentTitle) 

# # registering a external font in python 
# pdfmetrics.registerFont( 
# 	TTFont('abc', 'SakBunderan.ttf') 
# ) 

# # creating the title by setting it's font 
# # and putting it on the canvas 
# pdf.setFont('abc', 36) 
# pdf.drawCentredString(300, 770, title) 

# # creating the subtitle by setting it's font, 
# # colour and putting it on the canvas 
# pdf.setFillColorRGB(0, 0, 255) 
# pdf.setFont("Courier-Bold", 24) 
# pdf.drawCentredString(290, 720, subTitle) 

# # drawing a line 
# pdf.line(30, 710, 550, 710) 

# # creating a multiline text using 
# # textline and for loop 
# text = pdf.beginText(40, 680) 
# text.setFont("Courier", 18) 
# text.setFillColor(colors.red) 
# for line in textLines: 
# 	text.textLine(line) 
# pdf.drawText(text) 

# # drawing a image at the 
# # specified (x.y) position 
# pdf.drawInlineImage(image, 130, 400) 

# # saving the pdf 
# pdf.save() 


from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch

def create_pdf_reportlab(filename, text):
    c = canvas.Canvas(filename, pagesize=letter)
    c.drawString(100, 750, text)  # x, y coordinates (in points)
    c.save()

# Example usage
create_pdf_reportlab("my_report.pdf", "Hello, this is a <P> PDF created with ReportLab!")


#More advanced example with formatting
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph, SimpleDocTemplate

def create_formatted_pdf(filename, text):
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    style = styles['Normal']
    para = Paragraph(text, style)
    doc.build([para])

create_formatted_pdf("my_formatted_report.pdf", """This is  a <b>formatted</b> PDF.  
                     It uses <font color='red'>colored</font> 
                     text.""")


# from reportlab.pdfgen import canvas
# from reportlab.lib.pagesizes import letter
# from PyPDF2 import PdfReader, PdfWriter, PdfMerger

# def add_text_to_pdf_indirect(input_pdf, output_pdf, text, x, y):
#   # Create a temporary PDF with the text using ReportLab
#   temp_pdf = "temp.pdf"
#   c = canvas.Canvas(temp_pdf, pagesize=letter)
#   c.drawString(x, y, text)  # x, y in points
#   c.save()

#   # Merge PDFs using PyPDF2
#   merger = PdfMerger()
#   merger.append(input_pdf)
#   merger.append(temp_pdf)
#   merger.write(output_pdf)
#   merger.close()
#   #Clean up the temporary file
#   import os
#   os.remove(temp_pdf)

# #Example usage
# add_text_to_pdf_indirect("my_report.pdf", "my_document_with_text.pdf", "Added Text", 100,100)




