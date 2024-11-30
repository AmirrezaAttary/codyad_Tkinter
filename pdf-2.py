import jinja2
import pdfkit
from datetime import datetime


id = 1590
garanti = 'بلی'
tarikh = "1402/05/16"
date = "20:00:15"
name_input = "امیررضا"
system_name = "دیجتال"
typee = "LCD"
model = "mod-15"
seriyal = "64651"
tel = 9159526624
addres = "مسکن مهر خیابان مهر19 ساختمان ساسان واحد 16"
moshkel = "روشن نمیشود"

context = {'id':id,
           'garanti':garanti,
           'tarikh':tarikh,
           'date':date,
           'name_input':name_input,
           'system_name':system_name,
           'typee':typee,
           'model':model,
           'seriyal':seriyal,
           'tel':tel,
           'addres':addres,
           'moshkel':moshkel
}

temp_loder = jinja2.FileSystemLoader('./')

temp_env = jinja2.Environment(loader=temp_loder)

temp = temp_env.get_template('atar.html')
output_text = temp.render(context)

# Replace with your path
config = pdfkit.configuration(wkhtmltopdf = r"C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe")

css = "div.css"

pdfkit.from_string(output_text,f'sefaresh_{id}.pdf',options={"encoding":'UTF-8'},configuration=config,css=css)