import pandas as pd 
from datetime import datetime
from streamlit_gsheets import GSheetsConnection
import streamlit as st
import tim
import datetime as dt
from datetime import datetime, date
from google.oauth2.service_account import Credentials
from oauth2client.service_account import ServiceAccountCredentials
import gspread

st.cache_data.clear()
st.cache_resource.clear()

st.set_page_config(
     page_title= 'ACTIVITIES REVIEW STATUS'
)
# st.write('BEING UPDATED, WILL RETURN AFTER THE NEW BUDGETS')
# st.stop()
st.markdown("<h4><b>CHECK REVIEW STATUS OF PAPER WORK</b></h4>", unsafe_allow_html=True)

total= 0
district = ''
cluster = ''
Intention = st.radio('**HOW MAY I HELP YOU?**', options=['MARK REVIEWED PAPER WORK', 'CHECK REVIEW STATUS'], index=None)
file = r'PLANNED.csv'
df = pd.read_csv(file)

if Intention:
    pass
else:
    st.stop()
if 'sear' not in st.session_state:
     st.session_state.sear = False

if Intention == 'MARK REVIEWED PAPER WORK':
    coln, colm = st.columns([1,2])
    clusters  = df['CLUSTER'].unique()
    cluster = st.radio("**Choose a cluster:**", clusters,horizontal=True, index=None)
    if not cluster:
         st.stop()
    else:
         pass
    c = 'HOW MANY DO YOU HAVE?'
    coln, colm = st.columns([1,2])
    total = coln.number_input(label=f'**{c}**', value=None, max_value=15, min_value=1,step=1, format="%d")
    if total:
         pass
    else:
         st.stop()
         
    ids = []
    if total:
        if int(total)==1:     
            col1, col2,col3 = st.columns(3)
            m = 'IN PUT PAPER WORK ID'
            idea = col1.number_input(label=f'**{m}**', value=None, max_value=None, min_value=None,step=1, format="%d")
            if not idea:
                 st.stop()
            ids.append(idea)
            col2.write('')
            col2.write('')
            search = col2.button('**SEARCH ID**')
        else:
            col1, col2,col3 = st.columns(3)
            m = 'IN PUT PAPER WORK IDS'      
            for each in range(int(total)):
                col1, col2,col3 = st.columns(3)
                every = each+1
                id = col1.number_input(label=f'**{m} for paper work {every}**', value=None,key=each, max_value=None, min_value=None,step=1, format="%d")
                ids.append(id)
                if not id:
                     st.stop()
                else:
                     pass           
            col2.write('')
            col2.write('')
            col2.write('')
            search = col2.button('**SEARCH IDs**')
            if search:
                st.session_state.preview_clicke = Truees

            if st.session_state.sear:
                  try:
                       conn = st.connection('gsheets', type=GSheetsConnection)
                       exist1 = conn.read(worksheet= 'DONE', usecols=list(range(12)),ttl=5)
                       exist2 = conn.read(worksheet= 'PAID', usecols=list(range(2)),ttl=5)
                       existing1= exist1.dropna(how='all')
                       existing2= exist2.dropna(how='all')
                  except:
                       st.write("POOR INTERNET, COULDN'T CONNECT TO THE GOOGLE SHEETS")
                       st.write('Get better internet and try again')
                       st.stop()
            if st.session_state.sear:
                   review = existing1[existing1['CLUSTER'] == cluster].copy()
                   review['ID'] = pd.to_numeric(review['ID'], errors='coerce')
                   @st.cache_data
                   def finder ():
                        idx = []
                        idx = [int(i) for i in ids]
                        dfsee = review[review['ID'].isin(idx)].copy()
                        return dfsee
                   dfa = finder() 
                   if dfa.shape[0] == 0:
                        st.warning("**ID(s) NOT FOUND**")
                        st.stop()
                   else:
                        pass
                   st.write('**FIRST CHECK THEM BEFORE SUBMISSION**')
                   dfa = dfa[['DISTRICT', 'FACILITY', 'ACTIVITY', 'ID','AMOUNT']].copy()
                   dfu = dfa.copy()
                   dfa.index = pd.Index(range(1, len(dfa) + 1))
                   st.write(dfa)
                   a = dfa.shape[0]
                   b = len(ids)
                   if a == b:
                        pass
                   elif b>a:
                        ad = dfa['ID'].tolist()
                        abc = ids
                        ab = set(abc) - set(ad)
                        leg = len(list(ab))
                        abs = [str(i) for i in ab]
                        ab = ','.join(list(abs))
                        if leg ==1:
                             st.warning(f'**UNIQUE ID {ab} WAS NOT FOUND**')   
                        elif leg > 1:
                             st.warning(f'**THESE UNIQUE ID WERE NOT FOUND: {ab}**')
                             proc = st.radio('**DO YOU WANT TO PROCEED TO SUBMIT WITHOUT THEM**', options= ['YES', 'NO'], horizontal=True, index=None)
                             if not proc:
                                  st.stop()
                             elif proc == 'NO':
                                  st.write('**REFRESH TO SEARCH AGAIN OR REMOVE IT FROM THE LIST ABOVE**')
                                  st.stop
                             else:
                                  st.session_state.sear = True
                        else:
                            st.session_state.sear = True
                   submit = st.button('**SUBMIT**')  
                   if not submit:
                       st.stop()
                   else:
                       st.session_state.sear = True
                   if st.session_state.sear:
                      #st.write(st.session_state.sear)
                      secrets = st.secrets["connections"]["gsheets"]
                      credentials_info = {
                                 "type": secrets["type"],
                                 "project_id": secrets["project_id"],
                                 "private_key_id": secrets["private_key_id"],
                                 "private_key": secrets["private_key"],
                                 "client_email": secrets["client_email"],
                                 "client_id": secrets["client_id"],
                                 "auth_uri": secrets["auth_uri"],
                                 "token_uri": secrets["token_uri"],
                                 "auth_provider_x509_cert_url": secrets["auth_provider_x509_cert_url"],
                                 "client_x509_cert_url": secrets["client_x509_cert_url"]
                             }
                                 
                      try:
                             # Define the scopes needed for your application
                             scopes = ["https://www.googleapis.com/auth/spreadsheets",
                                     "https://www.googleapis.com/auth/drive"]
                             
                              
                             credentials = Credentials.from_service_account_info(credentials_info, scopes=scopes)
                                 
                                 # Authorize and access Google Sheets
                             client = gspread.authorize(credentials)
                                 
                                 # Open the Google Sheet by URL
                             spreadsheetu = " https://docs.google.com/spreadsheets/d/1IgIltX9_2yvppb4YYoebRyyYwCqYZng62h0cRYPmAdE"     
                             spreadsheet = client.open_by_url(spreadsheetu)
                      except Exception as e:   
                             st.write(f"CHECK: {e}")
                             st.write(traceback.format_exc())
                             st.write("COULDN'T CONNECT TO GOOGLE SHEET, TRY AGAIN")
                             st.stop()
                      try:
                         st. write('SUBMITING')
                         sheet1 = spreadsheet.worksheet("PAID")
                         rows_to_append = dfu.values.tolist()
                         sheet1.append_rows(rows_to_append, value_input_option='RAW')
                         st.success('Your data above has been submitted')
                         st.write('RELOADING PAGE')
                         time.sleep(3)
                         st.markdown("""
                         <meta http-equiv="refresh" content="0">
                              """, unsafe_allow_html=True)
          
                      except:
                         st.write("Couldn't submit, poor network") 
                 
else:
    clusters  = df['CLUSTER'].unique()
    cluster = st.radio("**Choose a cluster:**", clusters,horizontal=True, index=None)
    if cluster:
        try:
             conn = st.connection('gsheets', type=GSheetsConnection)
             exist1 = conn.read(worksheet= 'DONE', usecols=list(range(12)),ttl=5)
             exist2 = conn.read(worksheet= 'PAID', usecols=list(range(2)),ttl=5)
             existing1= exist1.dropna(how='all')
             existing2= exist2.dropna(how='all')
        except:
             st.write("POOR INTERNET, COULDN'T CONNECT TO THE GOOGLE SHEETS")
             st.write('Get better internet and try again')
             st.stop()
        sent = existing1[existing1['CLUSTER'] == cluster].copy()
        sent['ID'] =sent['ID'].astype(int)
        existing2['PAID'] =existing2['PAID'].astype(int)
        unpaid = sent[~sent['ID'].isin(existing2['PAID'])].copy()
        a = unpaid.shape[0]
        if int(a) == 0:
            st.write('**NO PAPER WORK PENDING**')
            st.stop()
        else:
            unpaid = unpaid[['DISTRICT', 'FACILITY', 'ACTIVITY', 'ID','AMOUNT']]
            st. markdown(f'YOU HAVE NOT REVIEWED {a} PAPER WORK(S)')
            with st.expander('CLICK HERE TO VIEW THEM'):
                st.write(unpaid)
    else:
        st.stop()





