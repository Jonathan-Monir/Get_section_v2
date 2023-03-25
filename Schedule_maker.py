import PyPDF2
import os
import pandas as pd
import streamlit as st
import base64

st.set_page_config(page_title="Gadwali", page_icon=open("lantern.png", "rb").read())
st.image(open("ramadan (1).png", "rb").read(), width=40)
st.write("<div style='position:fixed;bottom:10px;right:10px;'>By Jonathan Mamdouh</div>", 
         unsafe_allow_html=True)
def get_name(section_list):
    section_names = list()
    for i in section_list:
        count_num = 0
        sep = ".* "
        section_name = i.split(".pdf")[0]
        # print(section_name)
        section_name = section_name.split(" ")[-1]
        
        
        for m in i:
            if m.isdigit() or m==",":
                if count_num == 0:
                    section_name= section_name + sep + m
                    count_num +=1
                else: 
                    section_name= section_name + m
        section_name+= "\\b"
        # print(emp_str) 
        section_names.append(section_name)
    return section_names

def make_schedule(section_names):
    all_sections = list()
    print("hereeee", section_names)
    for word in section_names:
        if len(word) > 0:
            for i in df.columns:
                df[i] = df[i].str.replace("\n","")
                section= df.loc[df[i].str.contains(word,case=False)][["Day","Place",i]]
                # print(section)
                if section.empty:
                    _=0
                else:
                    all_sections.append(section)
        else:
            _=0
    return all_sections

def between(num1,num2,num3):
    if num1 >= num2 and num1 <=num3:
        return True

def or_sec(rakam_el_gloos):
    
    if between(rakam_el_gloos,1,32):
        rkm_el_section=1
    elif between(rakam_el_gloos,33,64):
        rkm_el_section=2
    elif between(rakam_el_gloos,65,96):
        rkm_el_section=3
    elif between(rakam_el_gloos,97,128):
        rkm_el_section=4
    elif between(rakam_el_gloos,129,160):
        rkm_el_section=5
    elif between(rakam_el_gloos,161,192):
        rkm_el_section=6
    else:
        return False
    return rkm_el_section

def linear_alg_sec(rakam_el_gloos):
    
    if between(rakam_el_gloos,1,31):
        rkm_el_section=1
    elif between(rakam_el_gloos,32,62):
        rkm_el_section=2
    elif between(rakam_el_gloos,63,93):
        rkm_el_section=3
    elif between(rakam_el_gloos,94,124):
        rkm_el_section=4
    elif between(rakam_el_gloos,125,155):
        rkm_el_section=5
    elif between(rakam_el_gloos,156,186):
        rkm_el_section=6
    else:
        return False
    return rkm_el_section

df = pd.read_excel("SHCEDULE.xlsx")
df["Day"].fillna(method="ffill",inplace=True)
df = df.fillna('')

files = [f for f in os.listdir('.') if os.path.isfile(f)]
container = st.empty()
name = st.text_input("Enter your name:")
if st.button("Submit"):
    if not name:
        st.error("Please enter your name")
    else:
        print("***********************************")
        print(name)
        st.success(f"Hello {name}")
        st.write("This may take 1 or 2 minutes...")
        all_sections = list()

        if not name:
            st.write("Please enter a name")

        else:
            
            for file in files:
                    if file.endswith(".pdf"):
                        container.markdown("<span style='color:gray'>searching in "+ file.strip(".pdf")+" section..</span>", unsafe_allow_html=True)
                        
                        count_got=0
                        pdf_file = open(file, 'rb')    

                        # creating a pdf reader object
                        pdf_reader = PyPDF2.PdfReader(pdf_file)


                        # extracting text from page


                        count_names=0
                        for el_saf7a in pdf_reader.pages:
                            text = el_saf7a.extract_text()
                            text = text.split('\n')
                            gadwal_el_sacation = list()
                            for i in text:
                                if name in i:
                                    if count_names == 0:
                                        _=0
                                    count_names += 1
                                    
                                    rkm_gloos = i.split(" ")[0]
                                    rkm_gloos = int(rkm_gloos)
                                    
                            if count_names == 1:
                                    text = pdf_reader.pages[0].extract_text().split('\n')
                                    for i in text:
                                        if "Sec " in i:
                                            gadwal_el_sacation.append(i)
                                            
                                    gadwal_el_sacation = ''.join(gadwal_el_sacation)
                                    each_Sec = gadwal_el_sacation.split("Sec")

                                    for i in each_Sec[1:]:
                                        range_arkam_elGloos = i.split(" ")[3:5]
                                        range_arkam_elGloos = [int(i) for i in range_arkam_elGloos]
                                        
                                        if file == "Operation research.pdf" and between(rkm_gloos,1,192):
                                            rkm_el_section=or_sec(rkm_gloos)
                                            if count_got==0:
                                                
                                                section_text = f"section: {rkm_el_section} in {file.strip('.')}"
                                                
                                                
                                                all_sections.append(section_text)
                                            count_got +=1
                                        elif file == "Linear Algebra.pdf" and between(rkm_gloos,1,186):
                                            rkm_el_section=linear_alg_sec(rkm_gloos)
                                            if count_got==0:
                                                section_text = f"section: {rkm_el_section} in {file.strip('.')}"
                                                
                                                all_sections.append(section_text)
                                                
                                            count_got +=1
                                        elif rkm_gloos >= range_arkam_elGloos[0] and rkm_gloos <= range_arkam_elGloos[1]:
                                            if count_got==0:
                                                rkm_el_section = i.split(" ")[1]
                                                section_text = f"section: {rkm_el_section} in {file.strip('.')}"
                                                
                                                all_sections.append(section_text)
                                                _=0
                                                
                                            count_got +=1
                                            
                        if count_names >1: 
                            st.error("more than one name found ")
                        elif count_names==0:
                            st.error("no name found in {}".format(file.strip(".pdf")))
                        
                        pdf_file.close()


            datasets=make_schedule(get_name(all_sections))
            try:
                combined_dataset = pd.concat(datasets)
                
                
                combined_dataset = combined_dataset.T
                first_column = combined_dataset.columns[0]
                combined_dataset = combined_dataset.sort_index(axis=1, level=0)
                combined_dataset = combined_dataset.sort_index(axis=1)
                combined_dataset = combined_dataset.T

                combined_dataset = combined_dataset.set_index(['Day', 'Place'])

                combined_dataset = combined_dataset.loc[pd.Categorical(combined_dataset.index.get_level_values('Day'),
                                        categories=['Saturday', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
                                        ordered=True)]

                combined_dataset.drop_duplicates(inplace=True)
                combined_dataset.fillna('',inplace=True)
                st.dataframe(combined_dataset)
                
                csv = combined_dataset.to_csv()
                b64 = base64.b64encode(csv.encode()).decode()
                href = f'<a href="data:file/csv;base64,{b64}" download="data.csv">Download CSV file</a>'
                st.markdown(href, unsafe_allow_html=True)
            except ValueError:
                print("error name")
            