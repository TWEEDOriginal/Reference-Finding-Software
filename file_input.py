import re
from author_finder import author_and_year_finder
from text_scraper import references_getter
from pdf_Author_Finder import pdf_author_and_year_finder
from pdf_text_scraper import pdf_references_getter
from docx_Author_Finder import docx_author_and_year_finder
from docx_text_scraper import docx_references_getter

  
re_pdf = r'\.pdf$'
re_txt = r'\.txt$'
re_docx = r'\.docx$'
regex = (re.compile(re_pdf),
         re.compile(re_txt),
         re.compile(re_docx),)
         
 
def file_inputer():
    file_path = input('Input file path:')  #E.g r"C:\Users\OGUNTADE\Desktop\python projects\test files\new.txt"
    input_file = file_path
    reference_type = 'AandY'
    
               
    for reg_obj in regex:
        match = reg_obj.search(str(input_file))
        if match:
            if match.group() == str('.pdf'):
                author_and_year_dict = pdf_author_and_year_finder(input_file)  
                references_list = pdf_references_getter(input_file, reference_type)
            elif match.group() == str('.txt'):
                author_and_year_dict = author_and_year_finder(input_file)  
                references_list = references_getter(str(input_file), reference_type)
            elif match.group() == str('.docx'): 
                author_and_year_dict = docx_author_and_year_finder(input_file) 
                references_list = docx_references_getter(input_file, reference_type)  
            
            print(author_and_year_dict, '\n\n\n\n', references_list)
            return author_and_year_dict,references_list    
if __name__ == '__main__':
    file_inputer()  