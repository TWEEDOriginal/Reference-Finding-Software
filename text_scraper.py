import re



#Numerals Method
def references_getter(txt_file, reference_type):
        square_bracket = r'''
                ([^\[\.]+)
                (\[\d+\])
                ([\w\s,';"!:()#%/$+-]*)
                (\.)   
        
            '''
        regex_for_bracket = r'''
            ([\w\s,';"!:()#%/$+-]+)
                (\(\d+\)|\((\d+,)+\d+\))
                ([\w\s,';"!:()#%/$+-]*)
                (\.)  
            '''     
        opcito = r'''
            ([\w\s,';"!:()#%$+/-]+)
            (\(op.cit.\)|\(loc.cit.\))
            ([\w\s,';"!:()#%/$+-]*)
                (\.) 
        '''       
            # how to put superscript. 
        #Author and year Method 
        two_authors_reg = r'''
            ([\w\s,';"!:()#%$+/-]*)
              \(?
            (?P<Author_name>[A-Z]\w+),?\s{1,2}
            (and|&)?\s{0,2}
            (?(3)(?P<second_author>[A-Z]\w+)|),?\s{0,2}
                \(?
                (?P<year>[12]\d{3})[a-z]?\s?
                \)
            ([\w\s,';"!:()#%/$+-]*)
            (\.)
        '''           
        et_al = r'''
            ([\w\s,';"!:()#%$+/-]*)
            \(?
            (?P<Author_name>[A-Z]\w+),?\s{1,2}  
             et\s{1,2}al\.?,?\s{1,2}
            \(?
            (?P<year>[12]\d{3})[a-z]?\s?
            \)
            ([\w\s,';"!:()#%/$+-]*)
            (\.)
            '''
        numerous_references = r'''
           ([\w\s,';"!:()#%$+/-]*)
            \(
            (?P<references>([A-Z][\w\s,]+[12]\d{3}[a-z]?;\s?)+)
            (?P<last_reference>[A-Z][\w\s,]+[12]\d{3}[a-z]?\s?)
            \)
            ([\w\s,';"!:()#%/$+-]*)
            (\.)
            '''    
           
        #put all regexes in a list, then loop through them with the text. or not because this might be time consuming. #'references','last_reference'

        re_modeswitch = re.compile('(References(\.?)|REFERENCES(\.?)|Bibliography(\.?)|BIBLIOGRAPHY(\.?)|Reference(s?)\sList(\.?)|REFERENCE(S?)\sLIST(\.?)|Works\sCited(\.?)|WORKS\sCITED(\.?))$')      
        
        re_numerals =(re.compile(square_bracket,re.X|re.S),
                      re.compile(regex_for_bracket,re.X|re.S),
                      re.compile(opcito,re.X|re.S),
             
        )
        re_references = (re.compile(two_authors_reg,re.X|re.S),
                         re.compile(et_al,re.X|re.S),
                         re.compile(numerous_references,re.X|re.S),
        )
        
        SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
        SUP = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")
        l = 'h2so4'.translate(SUP)
        references_list =[]
         #python text_scraper.py
        mode = 'references'
        reference_type = str(reference_type)
        paragraph_num = 0  
        with open (str(txt_file), 'rt') as myfile:
            for line in myfile:
                paragraph_num += 1
                line = line.strip()
                if line != "":
                    m = re_modeswitch.search(line)
                    if m:  
                        mode='bibliography'
                        continue 
                    if mode=='references' and reference_type == 'AandY':   
                        for reg_obj in re_references:
                            matches = reg_obj.finditer(line)
                            if matches:
                                for match in matches:
                                    sentence = match.group()
                                    sentence = sentence.strip()
                                    if sentence not in references_list:
                                                references_list.append(sentence)        
                    if mode=='references' and reference_type == 'numerals':   
                        for reg_obj in re_numerals:
                            matches = reg_obj.finditer(line)
                            if matches:
                                for match in matches:
                                    sentence = match.group()
                                    sentence = sentence.strip()
                                    if sentence not in references_list:
                                                references_list.append(sentence)        
                    

        return references_list 
