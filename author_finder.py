import re


def author_and_year_finder(txt_file):
    et_al = r'''  
    (?P<Author_name>[A-Z]\w+),?\s{1,2}  
    et\s{1,2}al\.?,?\s{1,2}
         \(?
    (?P<year>[12]\d{3})[a-z]?\s?
        \)
    '''
    one_author_ref = r''' 
            (?P<Author_name>[A-Z]\w+),?\s{1,2}
            (and|&)?\s{0,2}
            (?(2)(?P<second_author>[A-Z]\w+)|),?\s{0,2}
                \(?
                (?P<year>[12]\d{3})[a-z]?\s?
                \)
                '''
    # don't forget jointly authored can have intial before author name
    # for numerous try one author ref| etal ; and so on, hope you get.

    numerous_ref = r'''
            (?P<Author_name>[A-Z]\w+),?\s{1,2}
            (and|&)?\s{0,2}
            (?(2)(?P<second_author>[A-Z]\w+)|),?\s{0,2}
                (?P<year>[12]\d{3})[a-z]?\s?
                ;
    '''
    numerous_et_al = r'''
        (?P<Author_name>[A-Z]\w+),?\s{1,2}  
        et\s{1,2}al\.?,?\s{1,2}
        (?P<year>[12]\d{3})[a-z]?\s?
            ;
    '''
                #BIBLIOGRAPHY
    et_al_bib = r'''(?P<Author_name>[A-Z]\w+),? ([A-Z]\.?,?[ ]?){,3}(([A-Z]\.?,?[ ]?){,3}([A-Z]\w+),? ([A-Z]\.?,?[ ]?){,3}){1,5}(and|,) {1,2}([A-Z]\.?,?[ ]?){,3}([A-Z]\w+),? ([A-Z]\.?,?[ ]?){,3}\((?P<year>[12]\d{3})[a-z]?[ ]?\)''' 
    
    one_author_bib = r'''(?P<Author_name>[A-Z]\w+),? ([A-Z]\.?,?[ ]?){,3}(and|,)?[ ]?(?(3)([A-Z]\.?,?[ ]?){,3}(?P<second_author>[A-Z]\w+),?[ ]?([A-Z]\.?,?[ ]?){,3}|)\((?P<year>[12]\d{3})[a-z]?\s?\)'''


    one_author_list = []            
    one_author_bib_list = []
    et_al_list = []
    et_al_bib_list = []
    correct = []
    incorrect = []
    incorrectBib = []
    correctBib = []
    mode = 'references'
    re_modeswitch = re.compile('(References(\.?)|REFERENCES(\.?)|Bibliography(\.?)|BIBLIOGRAPHY(\.?)|Reference(s?)\sList(\.?)|REFERENCE(S?)\sLIST(\.?)|Works\sCited(\.?)|WORKS\sCITED(\.?))$')
    
    re_single_reference = re.compile(one_author_ref, re.X|re.S)
    re_single_bib = re.compile(one_author_bib)
    re_et_al = re.compile(et_al, re.X|re.S) 
    re_et_al_bib = re.compile(et_al_bib)
    re_num_ref = re.compile(numerous_ref, re.X|re.S)
    re_num_et_al = re.compile(numerous_et_al, re.X|re.S)
    with open (str(txt_file), 'rt') as myfile:
        for line in myfile:
                line = line.rstrip()
                if line != "":
                    m = re_modeswitch.search(line)
                    
                    if m:  
                      mode='bibliography'
                      continue 
                    
                    if mode=='references':
                        matches = re_single_reference.finditer(line)  
                        et_als = re_et_al.finditer(line)
                        num_refs = re_num_ref.finditer(line)
                        num_et_als = re_num_et_al.finditer(line)
                        if matches:
                                for match in matches:
                                    if match.groupdict() not in one_author_list:
                                        one_author_list.append(match.groupdict())
                        if et_als:
                                for match in et_als:
                                    if match.groupdict() not in et_al_list:
                                        et_al_list.append(match.groupdict())
                        if num_refs:
                                for match in num_refs:
                                    if match.groupdict() not in one_author_list:
                                        one_author_list.append(match.groupdict())
                        if num_et_als:
                                for match in num_et_als:
                                    if match.groupdict() not in et_al_list:
                                        et_al_list.append(match.groupdict())                                            
                    elif mode=='bibliography':   
                        matches = re_single_bib.finditer(line) 
                        et_al_bibs = re_et_al_bib.finditer(line) 
                        if matches:
                            for match in matches:
                                    if match.groupdict() not in one_author_bib_list:
                                        one_author_bib_list.append(match.groupdict())
                        if et_al_bibs:
                            for match in et_al_bibs:
                                    if match.groupdict() not in et_al_bib_list:
                                        et_al_bib_list.append(match.groupdict())        

    for i in one_author_list:
        x = i['Author_name']
        y = i['year']
        z = i['second_author']
        if i in one_author_bib_list:
            correct.append(i)
           
        else:
            incorrect.append(i)
    for i in et_al_list:  
        x = i['Author_name']
        y = i['year'] 
        if i in et_al_bib_list:
              correct.append(i)
        else:  
              incorrect.append(i)  
    for i in one_author_bib_list:
        x = i['Author_name']
        y = i['year']
        z = i['second_author']
        for l in one_author_list:
            if y == l['year']:
                if z != None: 
                    if x == l['Author_name'] or x== l['second_author']:
                        correctBib.append(i) 
                    elif z== l['Author_name'] or z== l['second_author']:
                        correctBib.append(i)  
                elif z == None:
                    if x == l['Author_name'] or x== l['second_author']:
                            correctBib.append(i)                
    for i in one_author_bib_list:
        if i not in correctBib: 
             incorrectBib.append(i)              	

    for i in et_al_bib_list: 
        if i not in et_al_list:    
            incorrectBib.append(i)	 		                
                                        
    new_dict = {}
    new_dict['one_author_list'] = one_author_list
    new_dict['et_al_list'] = et_al_list
    new_dict['one_author_bib_list'] = one_author_bib_list
    new_dict['et_al_bib_list'] = et_al_bib_list
    new_dict['correct'] = correct
    new_dict['incorrect'] = incorrect
    new_dict['incorrectBib'] = incorrectBib
    return new_dict        
 