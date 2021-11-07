# import libraries
import streamlit as st
import nltk
from nltk.tokenize import sent_tokenize
nltk.download('punkt')
import re
import pandas as pd
from readability import Readability

# table of content
class Toc:
    def __init__(self):
        self._items = []
        self._placeholder = None
    
    def title(self, text):
        self._markdown(text, "h1")

    def header(self, text):
        self._markdown(text, "h2", " " * 2)

    def subheader(self, text):
        self._markdown(text, "h3", " " * 4)

    def placeholder(self, sidebar=True):
        self._placeholder = st.sidebar.empty() if sidebar else st.empty()

    def generate(self):
        if self._placeholder:
            self._placeholder.markdown("\n".join(self._items), unsafe_allow_html=True)
    
    def _markdown(self, text, level, space=""):
        key = "-".join(text.split()).lower()
        st.markdown(f"<{level} id='{key}'>{text}</{level}>", unsafe_allow_html=True)
        self._items.append(f"{space}* <a href='#{key}'>{text}</a>")

# hide menu bar
st.markdown(""" <style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style> """, unsafe_allow_html=True)

# set up layout
padding = 1
st.markdown(f""" <style>
    .reportview-container .main .block-container{{
        padding-top: {padding}rem;
        padding-right: {padding}rem;
        padding-left: {padding}rem;
        padding-bottom: {padding}rem;
    }} </style> """, unsafe_allow_html=True)

# set up title
st.title("Flesch-Kincaid Readability Test")
st.write('\n')

# set up sidebar
st.sidebar.header("Table of Content")
toc = Toc()
toc.placeholder()

# calculate single text
toc.header('Flesch Kincaid Calculator')

# input text
TextBox = st.text_area('Enter text to check the readability', height=200)

# run the test
test = st.button("Calculate Readability")
if test:
    r = Readability(TextBox)
    fk = r.flesch_kincaid()
    statis = r.statistics()
    word = list(statis.items())[1][1]
    sentence = list(statis.items())[2][1]
    syllable = r.syll_count()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Flesh-Kincaid Score", round(fk.score, 1))
    col2.metric("Total of Words", word)
    col3.metric("Total of Sentences", sentence)
    col4.metric("Total Syllables", syllable)
st.write('\n')
st.write('\n')

# upload file
toc.header("Upload csv file")
file_upload = st.file_uploader("", type=["csv"])
if file_upload is not None:
    data = pd.read_csv(file_upload, encoding='unicode_escape')
    st.write(data)
    name = file_upload.name.replace('.csv', '')
    name = name+"_fk_score.csv"

# run the program
result = st.button("Run")
if result:
    st.write("Be patient, need to wait 1 to 2 minutes :smile:")
    df = data.iloc[:, 0]
    df.apply(str)
    list_data = df.tolist()

    # clean data
    new_content = []
    for string in list_data:
        new_string = string.replace("\n", " ")
        new_string2 = new_string.replace("\xa0", "")
        new_string3 = new_string2.replace("\'", "")
        new_string4 = re.sub(r'www\S+', '', new_string3)
        new_string5 = new_string4.replace("Â", "")
        new_string6 = new_string5.replace("\x9d", "")
        new_string7 = new_string6.replace("â€", "")
        new_string8 = new_string7.replace("â€œ", "")
        new_string9 = new_string8.replace("œ", "")
        new_string11 = re.sub(' +', ' ', new_string9).strip()
        new_string12 = new_string11.replace(". . .", "")
        new_string13 = re.sub(r'http\S+', '', new_string12)
        new_string14 = re.sub(r'[-+]?\d*\.\d+|\d+', '10', new_string13)
        new_content.append(new_string14)

    # Flesch-Kincaid Score
    list_fk_score = []
    for i in range(len(new_content)):
        r = Readability(new_content[i])
        fk = r.flesch_kincaid()
        list_fk_score.append(fk.score)

    # create new dataframe
    final_df = pd.DataFrame(
        {'Data': list_data,
        'Flesch Kincaid Score': list_fk_score,
        })
    
    # download labelled file
    st.write("Below is the Flesch Kincaid Score file, click button to download.")
    csv = final_df.to_csv(index=False)
    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name=name,
        mime='text/csv',
    )
    
st.write('\n')

toc.generate()
