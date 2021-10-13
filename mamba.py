import mammoth
import re


re_pdf = r'\.pdf$'
re_txt = r'\.txt$'
re_docx = r'\.docx$'
regex = (re.compile(re_pdf),
         re.compile(re_txt),
         re.compile(re_docx),)
         

def mamberer(file_path):
    input_file = file_path
    for reg_obj in regex:
        match = reg_obj.search(str(input_file))
         
        if match:
            if match.group() == str('.docx'):
                with open(str(input_file), "rb") as docx_file:    
                    result = mammoth.convert_to_html(docx_file)
                    html = result.value
            elif match.group() == str('.pdf'):
                 
                 html = 'I had to scrap this because pdfminer has a horrible pdf to HTML converter. Despite all the code I wrote to clean up the HTML view it still looks horrible and it is not worth the amount of time pdfminer takes to convert pdf to html. If you would like to get the little code I wrote for the HTML view so as to make some improvements on it please send me a mail. P.S Microsoft Word and txt files have good HTML views. '
            elif match.group() == str('.txt'):
                 with open (str(input_file), 'rt') as myfile:
                    html = ''
                    for line in myfile:
                      if line.strip() != "":  
                        html += f'<p>{line}</p>'
            return html        

if __name__ == "__main__":
    mamberer(file_path)

