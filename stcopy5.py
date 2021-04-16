import pickle
from pandas import DataFrame
import numpy as np
import pandas as pd
import streamlit as st
import xgboost as xgb
from xgboost import XGBClassifier,XGBRegressor
from streamlit import beta_columns
from PIL import Image
import streamlit as st
#from sklearn.externals import joblib
import sqlite3 
import pyodbc
import os
from streamlit import caching
import shutil
import datetime
from pathlib import Path
import joblib
#############################################################
#############################################################
conn2 = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                    'Server= VAIO;'
                    'Database=Blast;'
                    'Trusted_Connection=yes;')
c2 = conn2.cursor()

conn = sqlite3.connect('data.db')
c = conn.cursor()

# Security
#passlib,hashlib,bcrypt,scrypt
import hashlib
def make_hashes(password):
	return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
	if make_hashes(password) == hashed_text:
		return hashed_text
	return False

#################################################
#def create_table():
	#c2.execute('CREATE TABLE IF NOT EXISTS Blast(BBN TEXT,RT TEXT,HD INTEGER,LF INTEGER,LM INTEGER,WM INTEGER,WL INTEGER,RLW INTEGER,FE INTEGER)')
def add_data(BBN,sdt,edt,opl,opo,opd,opk,bot,bet,tyde,exdr,RT,Pos,HD,RLW,BO,B,SO,S,ST,SC,QT,QP,HN,ET,Q,PT,PQ,ISS,PSN,AL,TD,VB,WB,SP,SD,BU,FE,MU,OV,TF,Di,AEmulan,DRCT,DRCM,DRCB,FDT,FDM,FDB,OFT,OFM,OFB,RTT,RTM,RTB,LF,LM,LL,WF,WM,WL,QAnfo,QAzar,QEmulan,twbooster,thbooster,Abooster,deli,delh,delr,exwa,patt,tyci):
    c2.execute('INSERT INTO bdata2(BBN,sdt,edt,opl,opo,opd,opk,bot,bet,tyde,exdr,RT,Pos,HD,RLW,BO,B,SO,S,ST,SC,QT,QP,HN,ET,Q,PT,PQ,ISS,PSN,AL,TD,VB,WB,SP,SD,BU,FE,MU,OV,TF,Di,AEmulan,DRCT,DRCM,DRCB,FDT,FDM,FDB,OFT,OFM,OFB,RTT,RTM,RTB,LF,LM,LL,WF,WM,WL,QAnfo,QAzar,QEmulan,twbooster,thbooster,Abooster,deli,delh,delr,exwa,patt,tyci) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',(BBN,sdt,edt,opl,opo,opd,opk,bot,bet,tyde,exdr,RT,Pos,HD,RLW,BO,B,SO,S,ST,SC,QT,QP,HN,ET,Q,PT,PQ,ISS,PSN,AL,TD,VB,WB,SP,SD,BU,FE,MU,OV,TF,Di,AEmulan,DRCT,DRCM,DRCB,FDT,FDM,FDB,OFT,OFM,OFB,RTT,RTM,RTB,LF,LM,LL,WF,WM,WL,QAnfo,QAzar,QEmulan,twbooster,thbooster,Abooster,deli,delh,delr,exwa,patt,tyci))
    conn2.commit()

def add_path(p):
    c2.execute('INSERT INTO bdata2(image) VALUES (?)',(p))
    conn2.commit()
#############################################

def create_usertable():
	c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')

def add_userdata(username,password):
	c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',(username,password))
	conn.commit()

def login_user(username,password):
	c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
	data = c.fetchall()
	return data

def view_all_users():
	c.execute('SELECT * FROM userstable')
	data = c.fetchall()
	return data
#def main():
st.markdown('<style>body{background-color: rgb(159, 177, 188);}</style>',unsafe_allow_html=True)
#st.markdown('<html><style>div{background-image:linear-gradient(to right,red,blue);}</style><html>',unsafe_allow_html=True)



st.markdown("""<style>.css-1aumxhk {
background-color:rgb(110, 136, 151);
background-image: none;
color: #ffffff
}</style>""", unsafe_allow_html=True)

st.markdown("""
    <style>
    .big-font {
        font-size:37px !important;font-family:"B mitra", serif; color:rgb(47, 82, 102);text-align: center;
    }
    </style><p class="big-font">سامانه پایش عملیات آتشکاری معدن سنگ آهن چغارت</p>
    """, unsafe_allow_html=True)
#st.title("Record and Analyze Blast Operation Data")
menu = ["Home","Login","SignUp"]
choice = st.sidebar.selectbox("Menu",menu)

if choice == "Home":
    st.markdown("""
    <style>
    .big-font {
        font-size:37px !important;font-family:"B mitra", serif; color:rgb(47, 82, 102);text-align: center;
    }
    </style><p class="big-font">(امور ناریه حراست شرکت سنگ آهن مرکزی ایران)</p>
    """, unsafe_allow_html=True)
   
    #st.subheader("Explosion Monitoring Software")
    pic152 = Image.open('mine.jpg')
    st.image(pic152, use_column_width=True)
elif choice == "Login":
    #st.subheader("Login Section")
    username = st.sidebar.text_input("User Name")
    password = st.sidebar.text_input("Password",type='password')
    if st.sidebar.checkbox("Login"):
        # if password == '12345':
        create_usertable()
        hashed_pswd = make_hashes(password)

        result = login_user(username,check_hashes(password,hashed_pswd))
        
        if result:
            #st.success("Logged In as {}".format(username))
            #st.header("Goharzamin Iron Ore Mine CIBB")
            pages = ["Home", "Input Blast Data","Edit Blast Data","Prediction"]
            page = st.sidebar.radio("Menu Bar", options=pages)
            #st.title(page)
            if page == "Input Blast Data":
                #st.subheader("متغیرها را وارد کنید")
                st.markdown("""
                <style>
                .big-font {
                    font-size:40px !important;font-family:"B mitra", serif; color: rgb(47, 82, 102);text-align: center;
                }
                </style><p class="big-font">فرم ورودی داده ها</p>
                """, unsafe_allow_html=True)
                col64, col65,col66=st.beta_columns(3)
                with col64:
                    BBN = st.text_input('شماره بلوک انفجاری') 
                with col65:
                    today = datetime.date.today()
                    sdt = st.date_input("تاریخ شروع حفاری",value=today)
                with col66:
                    edt = st.date_input("تاریخ اتمام حفاری")
                col67, col68,col69,col70=st.beta_columns(4)
                with col67:
                    opl = st.text_input('نماینده پیمانکار') 
                with col68:
                    opo = st.text_input("نماینده کارفرما")
                with col69:
                    opd = st.text_input("نماینده دستگاه نظارت")
                with col70:
                    opk = st.text_input("سرپرست استخراج")
                col67, col68,col69,col70=st.beta_columns(4)
                with col67:
                    bot = st.number_input('تراز فعلی بلوک') 
                with col68:
                    bet = st.number_input("تراز نهایی بلوک")
                with col69:
                    tyde = st.text_input("کد و نوع دستگاه حفاری")
                with col70:
                    exdr = st.number_input("اضافه حفاری")

                col1, col2,col3,col4 =st.beta_columns(4)
                with col1:
                    STONE=['Magnetite', 'Hematite', 'Soil', 'Waste Rock', 'Cong-Waste Rock',
                    'Conglomerate', 'magn-Waste Rock', 'Soil-Cong', 'Soil-Waste Rock',
                    'So-Co-Waste Rock']
                    RT=st.selectbox('نوع سنگ',STONE)
                with col2:
                    Posi=['شمال', 'جنوب', 'غرب', 'شرق', 'شمال غرب',
                    'شمال شرق', 'جنوب غرب', 'جنوب شرق']
                    Pos = st.selectbox('موقعیت:',Posi)
                with col3:
                    HD=st.selectbox('قطر چال',(8.5,10.5,6.5,7.5))
                with col4:
                    RLW = st.number_input("نسبت طول به عرض بلوک")
                col5, col6,col7,col8 =st.beta_columns(4)

                with col5:
                    BO = st.number_input("بردن (بار سنگ) طراحی")
                with col6:
                    B = st.number_input("بردن عملیاتی")
                with col7:
                    SO = st.number_input("اسپیسینگ طراحی")
                with col8:
                    S = st.number_input("اسپیسینگ عملیاتی")

                col9, col10,col11,col12 =st.beta_columns(4)

                with col9:
                    ST = st.number_input("طول انسداد ", step= 0.1)
                with col10:
                    SC = st.number_input("خرج ویژه")
                with col11:
                    QT = st.number_input("مواد منفجره مصرفی در بلوک ",step=1.0)
                with col12:
                    QP = st.number_input("پرایمر مصرفی در بلوک ")
                    
                col13, col14,col15,col16 =st.beta_columns(4)

                with col13:
                    HN = st.number_input("تعداد چال در بلوک",step=1.0)
                with col14:
                    EETT=['Heavy ANFO', 'ANFO/AZAR', 'ANFO/EMULLAN', 'EMULAN', 'ANFO']
                    ET = st.selectbox("نوع ماده منفجره اصلی",EETT)
                with col15:
                    Q = st.number_input("مقدار ماده منفجره در یک چال")
                with col16:
                    PPTT =['EMULAN 30mm', 'EMULAN 35mm', 'EMULAN 40mm', 'EMULAN 65mm',
                     'EMULAN 90mm','booster Ib','booster(1/2)b','booster 2P','booster 3P']
                    PT = st.selectbox("نوع تقویت کننده انفجاری",PPTT)

                col17, col18,col19,col20 =st.beta_columns(4)

                with col17:
                    PQ = st.number_input("مقدار تقویت کننده در یک چال")
                with col18:
                    IISS = ['Nonel PHC','Nonel PMS','Cortex','Nonel\Cortex']
                    ISS = st.selectbox("سیستم انفجاری",IISS)
                with col19:
                    PSNN = ['Bottom','bottom\Middle']
                    PSN = st.selectbox("محل استقرار پرایمر",PSNN)
                with col20:
                    AL = st.number_input("عمق میانگین چال‌ها",step=0.1)     

                col21, col22,col23,col24 =st.beta_columns(4)

                with col21:
                    TD = st.number_input("حفاری کل بلوک",step=0.1)
                with col22:
                    VB = st.number_input("حجم سنگ بلوک")
                with col23:
                    WB = st.number_input("تناژ سنگ بلوک")
                with col24:
                    SP = st.number_input("پرایمر ویژه")

                col25, col26,col27,col28 =st.beta_columns(4)

                with col25:
                    SD = st.number_input("حفاری ویژه")
                with col26:
                    BU = st.number_input("بولدر و ناکنی")
                with col27:
                    FE = st.number_input("کارایی خردشدگی")
                with col28:
                    MMUU = ['TYPE 1','TYPE 2','TYPE 3','TYPE 4','TYPE 5','TYPE 6','TYPE 7']
                    MU = st.selectbox("وضعیت کپه سنگ خرد شده",MMUU)

                col29, col30,col31,col32 =st.beta_columns(4)

                with col29:
                    OOVV = ['TYPE 1','TYPE 2','TYPE 3','TYPE 4','TYPE 5','TYPE 6','TYPE 7','TYPE 8']
                    OV = st.selectbox("شرایط شکستگی ناخواسته",OOVV)
                with col30:
                    TTFF= ['TYPE 1','TYPE 2','TYPE 3','TYPE 4','TYPE 5']
                    TF = st.selectbox("وضعیت کف پله و پاشنه",TTFF)
                with col31:
                    DDii = ['N','Y','M']
                    Di = st.selectbox("شرایط ترقیق",DDii)
                with col32:
                    AEmulan = st.number_input("امولایت کارتریجی کل پترن(کیلوگرم)",step=1.0)

                col33, col34,col35 =st.beta_columns(3)

                with col33:
                    D1 = ['Integrated','Block','Crushed']
                    DRCT = st.selectbox("شرایط توده سنگی(1/3 بالایی)",D1)
                with col34:
                    D2 = ['Integrated','Block','Crushed']
                    DRCM = st.selectbox("شرایط توده سنگی(1/3 میانی)",D2)
                with col35:
                    D3 = ['Integrated','Block','Crushed']
                    DRCB = st.selectbox("شرایط توده سنگی(1/3 پایینی)",D3)

                col36,col37,col38=st.beta_columns(3)

                with col36:
                    D4 = ['M1','L1']
                    FDT = st.selectbox("فاصله داری شکستگی ها(1/3 بالایی)",D4)
                with col37:
                    D5 = ['M1','L1']
                    FDM = st.selectbox("فاصله داری شکستگی ها(1/3 میانی)",D5)
                with col38:
                    D6 = ['M1','L1']
                    FDB = st.selectbox("فاصله داری شکستگی ها(1/3 پایینی)",D6)

                col39, col40,col41 =st.beta_columns(3)

                with col39:
                    V1 = ['No layer','Horizontal','Sloping inwards','Sloping outwards']
                    OFT = st.selectbox("جهت داری شکستگی ها(1/3 بالایی)",V1)
                with col40:
                    V2 = ['No layer','Horizontal','Sloping inwards','Sloping outwards']
                    OFM = st.selectbox("جهت داری شکستگی ها(1/3 میانی)",V2)
                with col41:
                    V3 = ['No layer','Horizontal','Sloping inwards','Sloping outwards']
                    OFB = st.selectbox("جهت داری شکستگی ها(1/3 پایینی)",V3)
                
                col45, col46,col47 =st.beta_columns(3)

                with col45:
                    W1 = ['Soft Ore','Hard Ore','Soil','Soft Waste','Conglomerate']
                    RTT = st.selectbox("جنس بلوک انفجاری(1/3 بالایی)",W1)
                with col46:
                    W2 = ['Soft Ore','Hard Ore','Soil','Soft Waste','Conglomerate']
                    RTM = st.selectbox("جنس بلوک انفجاری(1/3 میانی)",W2)
                with col47:
                    W3 = ['Soft Ore','Hard Ore','Soil','Soft Waste','Conglomerate']
                    RTB = st.selectbox("جنس بلوک انفجاری(1/3 پایینی)",W3)
            
                col48, col49,col50 =st.beta_columns(3)

                with col48:
                    LF = st.number_input("میانگین عمق چال‌ها-ردیف اول")
                with col49:
                    LM = st.number_input("میانگین عمق چال‌ها-ردیف میانی")
                with col50:
                    LL = st.number_input("میانگین عمق چال‌ها-ردیف آخر")
                
                col51, col52,col53 =st.beta_columns(3)

                with col51:
                    WF = st.number_input(" عمق آب به عمق چال-ردیف اول")
                with col52:
                    WM = st.number_input("عمق آب به عمق چال-ردیف میانی")
                with col53:
                    WL = st.number_input("عمق آب به عمق چال-ردیف آخر")

                col54, col55,col56 =st.beta_columns(3)

                with col54:
                    QAnfo = st.number_input("میزان آنفو مصرفی بلوک (کیلو گرم)")
                with col55:
                    QAzar = st.number_input("میزان پودر آذر مصرفی بلوک (کیلو گرم)")
                with col56:
                    QEmulan = st.number_input("میزان امولایت مصرفی بلوک (کیلو گرم)")

                col57, col58,col59 =st.beta_columns(3)

                with col57:
                    twbooster = st.number_input("تعداد بوستر مصرفی 2 پوندی")
                with col58:
                    thbooster = st.number_input("تعداد بوستر مصرفی 3 پوندی")
                with col59:
                    Abooster = st.number_input("بوستر مصرفی کل پترن (کیلو گرم)")
                col71, col72,col73,=st.beta_columns(3)
                with col71:
                    deli = st.number_input("تاخیر چاشنی درون چال")
                with col72:
                    delh = st.number_input("تاخیر سطحی بین چالها")
                with col73:
                    delr = st.number_input("تاخیر سطحی بین ردیفی")

                col74,col75,col76=st.beta_columns(3)
                with col74:
                    exwa = st.text_input('روش انفجار') 
                with col75:
                    patt = st.text_input("الگوی انفجار")
                with col76:
                    tyci = st.text_input('نوع مداربندی') 
                


                pic = st.file_uploader("بارگذاری عکس بلوک انفجاری", type="jpg")
              
                if st.button("ثبت بلوک انفجاری"):
                    add_data(BBN,sdt,edt,opl,opo,opd,opk,bot,bet,tyde,exdr,RT,Pos,HD,RLW,BO,B,SO,S,ST,SC,QT,QP,HN,ET,Q,PT,PQ,ISS,PSN,AL,TD,VB,WB,SP,SD,BU,FE,MU,OV,TF,Di,AEmulan,DRCT,DRCM,DRCB,FDT,FDM,FDB,OFB,OFM,OFB,RTT,RTM,RTB,LF,LM,LL,WF,WM,WL,QAnfo,QAzar,QEmulan,twbooster,thbooster,Abooster,deli,delh,delr,exwa,patt,tyci)
                    t = open(pic.name, "wb")
                    t.write(pic.read())
                    t.close()
                    b = '.jpg'
                    os.rename(pic.name,BBN+b)
                    source = BBN+b
                    destination = "demo"
                    new_path = shutil.move(source, destination)
                    p = os.path.abspath(source)
                    add_path(p)
                    st.success("You have successfully added Blast")

                sql_query = pd.read_sql_query('SELECT * FROM Blast.dbo.bdata2',conn2)
                st.write("DATABASE")
                st.write(sql_query)
                #st.sidebar.header("Goharzamin Iron Ore Mine CIBB")
                
            elif  page == "Home":
                    #st.write("شرکت بهینه راهبرد انفجار")
                    pic1 = Image.open('blasting-pic.jpg')
                    st.image(pic1, use_column_width=True)
            elif  page == "Prediction":
                st.sidebar.header("متغیرها را وارد کنید")

                def user_input_features():
                    LF = st.sidebar.slider("میانگین عمق چال‌ها در ردیف اول", 0.00, 20.00, 0.00)
                    LM = st.sidebar.slider("میانگین عمق چال‌ها در ردیف‌های میانی", 0.00, 20.00, 0.0)
                    WM = st.sidebar.slider("نسبت عمق آب به عمق چال ردیف‌های میانی", 0.00, 1.00, 0.00)
                    WL = st.sidebar.slider("نسبت عمق آب به عمق چال ردیف آخر", 0.00, 1.00, 0.00)
                    RLW = st.sidebar.slider("نسبت طول به عرض بلوک  انفجاری", 0.00, 25.00, 0.00)

                    data = {
                            'LF':LF,
                            'LM':LM,
                            'WM':WM,
                            'WL':WL,
                            'RLW':RLW,
                    }

                    return pd.DataFrame(data, index=[0])    

                df = user_input_features()
                # Main
                st.header("***Mine to Mill Optimization Projecte***")
                #st.subheader(" پیش بینی کارایی خردایش ")
                st.write("\n")
                st.write("\n")
                st.write("متغیرهای ورودی کاربر:")
                st.write(df)

                with open("xgboost.pkl", "rb") as f:
                    mdl = joblib.load(f)   
                predictions = mdl.predict(df)[0]

                st.write("\n")
                st.write("\n")
                st.subheader("پیش بینی بر اساس مدل : XgBoost")
                st.write(f"The predicted Fragmentation is: {(predictions)}")

                with open("xgbBU.pkl", "rb") as f:
                    mdl = joblib.load(f)   
                predbu = mdl.predict(df)[0]
                st.write(f"The predicted Bulder is: {(predbu)}")
                st.write("\n")       
                with open("xgbTF.pkl", "rb") as f:
                    mdl = joblib.load(f)   
                predTF = mdl.predict(df)[0]
                st.write(f"The predicted TF is: {(predTF)}")
                if predTF == "type 1":
                    st.markdown("""
                                <style>
                                .big-font {
                                    font-size:25px !important;font-family:"B mitra", serif;
                                }
                                </style> <p class="big-font">عدم نیاز به تسطیح؛ نبود پاشنه؛ نبود قوزک و ناهمواری های کف</p>
                                """, unsafe_allow_html=True)
                    #st.write("عدم نیاز به تسطیح؛ نبود پاشنه؛ نبود قوزک و ناهمواری های کف")
                elif predTF == "type 2":
                    st.markdown("""
                                <style>
                                .big-font {
                                    font-size:25px !important;font-family:"B mitra", serif;
                                }
                                </style> <p class="big-font">نیاز به بلدوزرکاری کم؛نیاز به چکش کاری کم؛نبود پاشنه؛قوزک و ناهمواری های کم در کف پله؛کارایی خوب بارکننده جهت بارگیری از کف پله</p>
                                """, unsafe_allow_html=True)
                    #st.write('نیاز به بلدوزرکاری کم؛ - نیاز به چکش¬کاری کم؛- نبود پاشنه؛  قوزک و ناهمواری های کم در کف پله؛ - کارایی خوب بارکننده جهت بارگیری از کف پله')
                elif predTF == "type 3":
                    st.markdown("""
                                <style>
                                .big-font {
                                    font-size:25px !important;font-family:"B mitra", serif;
                                }
                                </style> <p class="big-font">نیاز به بلدوزرکاری کم؛ نیاز به چکش کاری متوسط؛ وجود پاشنه کوچک در برخی نقاط بلوک؛قوزک و ناهمواری های کم در کف؛ کارایی خوب بارکننده جهت بارگیری از کف</p>
                                """, unsafe_allow_html=True)
                    #st.write('نیاز به بلدوزرکاری کم؛ نیاز به چکش کاری متوسط؛ وجود پاشنه کوچک در برخی نقاط بلوک؛قوزک و ناهمواری¬های کم در کف؛ کارایی خوب بارکننده جهت بارگیری از کف')
                elif predTF == 'type 4':
                    st.markdown("""
                                <style>
                                .big-font {
                                    font-size:25px !important;font-family:"B mitra", serif;
                                }
                                </style> <p class="big-font">بلدوزرکاری متوسط؛نیاز به چکش کاری زیاد؛وجود پاشنه در برخی از نقاط؛وجود قوزک کم و  ناهمواری کم زمین؛کارایی متوسط بارکننده جهت بارگیری از کف</p>
                                """, unsafe_allow_html=True)
                    #st.write('بلدوزرکاری متوسط؛نیاز به چکش کاری زیاد؛وجود پاشنه در برخی از نقاط؛وجود قوزک کم و  ناهمواری کم زمین؛کارایی متوسط بارکننده جهت بارگیری از کف') 
                else:
                    st.markdown("""
                                <style>
                                .big-font {
                                    font-size:25px !important;font-family:"B mitra", serif;
                                }
                                </style> <p class="big-font">نیاز به بلدوزرکاری متوسط؛نیاز به چکش کاری زیاد؛وجود قوزک زیاد و شرایط ناهموار زمین؛وجود پاشنه نیازمند حفاری مجدد و کارایی بد بارکننده جهت بارگیری از کف</p>
                                """, unsafe_allow_html=True)
                    #t.write("نیاز به بلدوزرکاری متوسط؛نیاز به چکش کاری زیاد؛وجود قوزک زیاد و شرایط ناهموار زمین؛وجود پاشنه نیازمند حفاری مجدد و کارایی بد بارکننده جهت بارگیری از کف")       

                with open("xgbOV.pkl", "rb") as f:
                    mdl = joblib.load(f)   
                predOV = mdl.predict(df)[0]
                st.write(f"The predicted OV is: {(predOV)}")
                if predOV == "type 1":
                    st.markdown("""
                                <style>
                                .big-font {
                                    font-size:25px !important;font-family:"B mitra", serif;
                                }
                                </style> <p class="big-font">وجود دیواره های صاف وبا شیب مناسب (تقریبا80)-عدم نیاز به لق گیری-محل استقرار دستگاه حفاری مناسب با ایمنی بالا -نبود ترک و شکستگی سطحی بلوک -عدم نیاز به بلدوزرکاری"</p>
                                """, unsafe_allow_html=True)
                    #st.write("وجود دیواره های صاف وبا شیب مناسب (تقریبا80)-عدم نیاز به لق گیری-محل استقرار دستگاه حفاری مناسب با ایمنی بالا -نبود ترک و شکستگی سطحی بلوک -عدم نیاز به بلدوزرکاری")
                elif predOV == "type 2":
                    st.markdown("""
                                <style>
                                .big-font {
                                    font-size:25px !important;font-family:"B mitra", serif;
                                }
                                </style> <p class="big-font">وجود دیواره های صاف وبا شیب مناسب (تقریبا80)- نیاز به لق گیری کم دیواره-محل استقرار دستگاه حفاری مناسب با ایمنی بالا -نبود ترک و شکستگی  در سطح بلوک - نیاز به بلدوزرکاری کم</p>
                                """, unsafe_allow_html=True)
                    #st.write('وجود دیواره های صاف وبا شیب مناسب (تقریبا80)- نیاز به لق گیری کم دیواره-محل استقرار دستگاه حفاری مناسب با ایمنی بالا -نبود ترک و شکستگی  در سطح بلوک - نیاز به بلدوزرکاری کم')
                elif predOV == "type 3":
                    st.markdown("""
                                <style>
                                .big-font {
                                    font-size:25px !important;font-family:"B mitra", serif;
                                }
                                </style> <p class="big-font">وجود دیواره های صاف وبا شیب مناسب (تقریبا80)-نیاز به لق گیری متوسط دیواره-محل استقرار دستگاه حفاری نسبتا مناسب با ایمنی متوسط -نبود ترک و شکستگی در سطح بلوک- عدم نیاز به بلدوزرکاری</p>
                                """, unsafe_allow_html=True)
                    #st.write('وجود دیواره های صاف وبا شیب مناسب (تقریبا80)-نیاز به لق گیری متوسط دیواره-محل استقرار دستگاه حفاری نسبتا مناسب با ایمنی متوسط -نبود ترک و شکستگی در سطح بلوک- عدم نیاز به بلدوزرکاری')
                elif predOV == 'type 4':
                    st.markdown("""
                                <style>
                                .big-font {
                                    font-size:25px !important;font-family:"B mitra", serif;
                                }
                                </style> <p class="big-font">وجود دیواره های صاف وبا شیب مناسب (تقریبا80)-نیاز به لق گیری کم دیواره-محل استقرار دستگاه حفاری نسبتا مناسب با ایمنی متوسط-وجود ترک و شکستگی کم در سطح بلوک -نیاز به بلدوزرکاری کم</p>
                                """, unsafe_allow_html=True)
                    #st.write('وجود دیواره های صاف وبا شیب مناسب (تقریبا80)-نیاز به لق گیری کم دیواره-محل استقرار دستگاه حفاری نسبتا مناسب با ایمنی متوسط-وجود ترک و شکستگی کم در سطح بلوک -نیاز به بلدوزرکاری کم')
                elif predOV == 'type 5':
                    st.markdown("""
                                <style>
                                .big-font {
                                    font-size:25px !important;font-family:"B mitra", serif;
                                }
                                </style> <p class="big-font">وجود دیواره های صاف وبا شیب مناسب (تقریبا80)-نیاز به لق گیری متوسط دیواره-محل استقرار دستگاه حفاری نسبتا  مناسب با ایمنی متوسط -وجود ترک و شکستگی کم در سطح بلوک -نیاز به بلدوزرکاری کم</p>
                                """, unsafe_allow_html=True)
                    #st.write('وجود دیواره های صاف وبا شیب مناسب (تقریبا80)-نیاز به لق گیری متوسط دیواره-محل استقرار دستگاه حفاری نسبتا  مناسب با ایمنی متوسط -وجود ترک و شکستگی کم در سطح بلوک -نیاز به بلدوزرکاری کم')
                elif predOV == 'type 6':
                    st.markdown("""
                                <style>
                                .big-font {
                                    font-size:25px !important;font-family:"B mitra", serif;
                                }
                                </style> <p class="big-font">وجود دیواره های صاف وبا شیب مناسب (تقریبا80)-نیاز به لق گیری زیاد دیواره-محل استقرار دستگاه حفاری نا مناسب با ایمنی کم-وجود ترک و شکستگی زیاد در سطح بلوک-نیاز به بلدوزرکاری زیاد</p>
                                """, unsafe_allow_html=True)
                    #st.write('وجود دیواره های صاف وبا شیب مناسب (تقریبا80)-نیاز به لق گیری زیاد دیواره-محل استقرار دستگاه حفاری نا مناسب با ایمنی کم   -وجود ترک و شکستگی زیاد در سطح بلوک-نیاز به بلدوزرکاری زیاد')
                elif predOV == 'type 7':
                    st.markdown("""
                                <style>
                                .big-font {
                                    font-size:25px !important;font-family:"B mitra", serif;
                                }
                                </style> <p class="big-font">محل استقرار دستگاه حفاری نسبتا مناسب با ایمنی متوسط-نبود ترک و شکستگی  در سطح بلوک-عدم نیاز به بلدوزرکاری-وجود دیواره با شکم دادگی بدلیل شرایط بد، جنس زمین- نیاز به لق گیری متوسط</p>
                                """, unsafe_allow_html=True)
                    #st.write("*-محل استقرار دستگاه حفاری نسبتا مناسب با ایمنی متوسط  -نبود ترک و شکستگی  در سطح بلوک  - عدم نیاز به بلدوزرکاری")       
                    #st.write("-وجود دیواره با شکم دادگی بدلیل شرایط بد جنس زمین - نیاز به لق گیری متوسط")       
                else:
                    st.markdown("""
                                <style>
                                .big-font {
                                    font-size:25px !important;font-family:"B mitra", serif;
                                }
                                </style> <p class="big-font">وجود دیواره  با شیب ملایم (55 تا 70) بدلیل وجود گسل -نیاز به لق گیری زیاد-محل استقرار دستگاه حفاری نا مناسب ایمنی کم-وجود ترک و شکستگی زیاد در سطح بلوک -نیاز به بلدوزرکاری زیاد</p>
                                """, unsafe_allow_html=True)
                    #st.write("محل استقرار دستگاه حفاری نا مناسب ایمنی کم   -وجود ترک و شکستگی زیاد در سطح بلوک -نیاز به بلدوزرکاری زیاد")       
                    #st.write("وجود دیواره  با شیب ملایم (55 تا 70) بدلیل وجود گسل -نیاز به لق گیری زیاد ")       

                with open("xgbMU.pkl", "rb") as f:
                    mdl = joblib.load(f)   
                predMU= mdl.predict(df)[0]
                st.write(f"The predicted MU is: {(predMU)}")

                if predMU == "type 1":
                    st.markdown("""
                                <style>
                                .big-font {
                                    font-size:25px !important;font-family:"B mitra", serif;
                                }
                                </style> <p class="big-font">مساحت خیلی زیاد پاک سازی؛ایمنی مناسب بارگیری؛ استقرار آسان دستگاه‌های بارکننده؛ قفل شدگی ندارد؛ کارایی خوب بارکننده کوچک در باطله و خاک؛ کارایی خوب بارکننده متوسط در سنگ آهن</p>
                                """, unsafe_allow_html=True)
                    pic1 = Image.open('1.jpg')
                    st.image(pic1, use_column_width=True)
                    #st.write('مساحت خیلی زیاد پاک سازی؛ایمنی مناسب بارگیری؛ استقرار آسان دستگاه‌های بارکننده؛ قفل شدگی ندارد؛ کارایی خوب بارکننده کوچک در باطله و خاک؛ کارایی خوب بارکننده متوسط در سنگ آهن')
                elif predMU =="type 2":
                    st.markdown("""
                                <style>
                                .big-font {
                                    font-size:25px !important;font-family:"B mitra", serif;
                                }
                                </style> <p class="big-font">مساحت کم پاک سازی؛ ایمنی متوسط بارگیری؛ استقرار سخت دستگاه‌ بارکننده؛ احتمال قفل شدگی زیاد بار؛  نیاز به بلدوزر برای کم کردن ارتفاع بار (پایین نشاندن ارتفاع بار)؛ کارایی بد بارکننده‌ ها؛</p>
                                """, unsafe_allow_html=True)
                    pic2 == Image.open('2.jpg')
                    st.image(pic2, use_column_width=True)
                    #st.write('مساحت کم پاک سازی؛ ایمنی متوسط بارگیری؛ استقرار سخت دستگاه‌ بارکننده؛ احتمال قفل شدگی زیاد بار؛  نیاز به بلدوزر برای کم کردن ارتفاع بار (پایین نشاندن ارتفاع بار)؛ کارایی بد بارکننده‌ ها؛ ') 

                elif predMU == "type 3":
                    st.markdown("""
                                <style>
                                .big-font {
                                    font-size:25px !important;font-family:"B mitra", serif;
                                }
                                </style> <p class="big-font">استقرار سخت دستگاه‌ بارکننده؛ احتمال قفل¬شدگی زیاد بار؛ نیاز به بلدوزر برای کم کردن ارتفاع بار (پایین نشاندن ارتفاع بار)؛ کارایی بد بارکننده‌ ها؛- مساحت کم پاک سازی؛ ایمنی بد بارگیری؛</p>
                                """, unsafe_allow_html=True)
                    pic3 = Image.open('3.jpg')
                    st.image(pic3, use_column_width=True)
                    #st.write('استقرار سخت دستگاه‌ بارکننده؛ احتمال قفل¬شدگی زیاد بار؛ نیاز به بلدوزر برای کم کردن ارتفاع بار (پایین نشاندن ارتفاع بار)؛ کارایی بد بارکننده‌ ها؛- مساحت کم پاک سازی؛ ایمنی بد بارگیری؛')
                elif predMU == 'type 4':
                    st.markdown("""
                                <style>
                                .big-font {
                                    font-size:25px !important;font-family:"B mitra", serif;
                                }
                                </style> <p class="big-font">مساحت زیاد پاک سازی؛ ایمنی خوب بارگیری؛استقرار آسان دستگاه‌ بارکننده؛ قفل شدگی ندارد؛ کارایی خوب بارکننده‌؛</p>
                                """, unsafe_allow_html=True)
                    pic4 = Image.open('4.jpg')
                    st.image(pic4, use_column_width=True)
                    #st.write('مساحت زیاد پاک سازی؛ ایمنی خوب بارگیری؛استقرار آسان دستگاه‌ بارکننده؛ قفل شدگی ندارد؛ کارایی خوب بارکننده‌ متوسط؛ ')
                elif predMU == 'type 5':
                    st.markdown("""
                                <style>
                                .big-font {
                                    font-size:25px !important;font-family:"B mitra", serif;
                                }
                                </style> <p class="big-font">مساحت متوسط پاک سازی؛ایمنی خوب بارگیری؛استقرار نسبتا آسان دستگاه‌ بارکننده؛احتمال قفل شدگی متوسط بار؛کارایی خوب بارکننده‌ ؛ </p>
                                """, unsafe_allow_html=True)
                    pic4 = Image.open('5.jpg')
                    st.image(pic4, use_column_width=True)
                    #st.write('مساحت متوسط پاک سازی؛ - ایمنی خوب بارگیری؛ - استقرار نسبتا آسان دستگاه‌ بارکننده؛    - احتمال قفل شدگی متوسط بار؛ - کارایی خوب بارکننده‌ متوسط؛ ')

                elif predMU == 'type 6':
                    st.markdown("""
                                <style>
                                .big-font {
                                    font-size:25px !important;font-family:"B mitra", serif;
                                }
                                </style> <p class="big-font">مساحت متوسط پاک سازی؛ایمنی متوسط بارگیری؛ استقرار نسبتا آسان دستگاه‌ بارکننده؛احتمال قفل¬شدگی متوسط بار؛ نیاز به بلدوزر برای کم کردن ارتفاع بار(پایین نشاندن ارتفاع بار) ؛کارایی متوسط بارکننده‌؛</p>
                                """, unsafe_allow_html=True)
                    pic4 = Image.open('6.jpg')
                    st.image(pic4, use_column_width=True)
                    #st.write('مساحت متوسط پاک سازی؛ ایمنی متوسط بارگیری؛ استقرار نسبتا آسان دستگاه‌ بارکننده؛    احتمال قفل¬شدگی متوسط بار؛ نیاز به بلدوزر برای کم کردن ارتفاع بار(پایین نشاندن ارتفاع بار) ؛کارایی متوسط بارکننده‌ متوسط؛')

                else:
                    st.markdown("""
                                <style>
                                .big-font {
                                    font-size:25px !important;font-family:"B mitra", serif;
                                }
                                </style> <p class="big-font">مساحت زیاد پاک سازی؛ایمنی خوب بارگیری؛استقرار آسان دستگاه‌ بارکننده؛احتمال قفل شدگی کم بار؛کارایی خوب بارکننده‌؛</p>
                                """, unsafe_allow_html=True)
                    pic5 = Image.open('7.jpg')
                    st.image(pic5, use_column_width=True)
                    #st.write('مساحت زیاد پاک سازی؛ایمنی خوب بارگیری؛استقرار آسان دستگاه‌ بارکننده؛   احتمال قفل شدگی کم بار؛کارایی خوب بارکننده‌ متوسط؛')

            elif  page == "Edit Blast Data":
                    st.markdown("""
                                <style>
                                .big-font {
                                    font-size:25px !important;font-family:"B mitra", serif;
                                }
                                </style> <p class="big-font">اصلاح و ویرایش داده ها</p>
                                """, unsafe_allow_html=True)
                    #St.write("Edit Blast Data")
                    #BBNe = st.text_input('شماره بلوک انفجاری')
                    
                    var=['RT','BBN','HD','LF','LM','WM','WL','RLW','FE']
                    kk=st.selectbox('متغیر را برای تغییر مقدار انتخاب کنید:',var)
                    if kk == 'RT':
                        def UP_DATE(i,j):
                            c2.execute('UPDATE bdata2 SET RT =? WHERE BBN =? ',(i,j))
                            conn2.commit()
                        m = st.text_input(':شماره بلوک انفجاری')
                        STONE=['Magnetite', 'Hematite', 'Soil', 'Waste Rock', 'Cong-Waste Rock',
                        'Conglomerate', 'magn-Waste Rock', 'Soil-Cong', 'Soil-Waste Rock',
                        'So-Co-Waste Rock']
                        k = st.selectbox('New Rock Type:',STONE)   
                        if st.button("UPDATE row"):
                            UP_DATE(k,m)
                            st.success("You have successfully Update Blast")                         
                            script =("""SELECT * FROM Blast.dbo.bdata2""")
                            c2.execute(script)
                            ql_query = pd.read_sql_query(script,conn2)
                            st.write(ql_query)                 
                    elif kk == 'HD':
                        def UP_DATE(i,j):
                            c2.execute('UPDATE bdata2 SET HD =? WHERE BBN =? ',(i,j))
                            conn2.commit()
                        m = st.text_input(':شماره بلوک انفجاری')
                        k = st.radio('New Hole Diameter:',( 8.5, 10.5, 6.5, 7.5))
                        UP_DATE(k,m)
                    elif kk == 'LF':
                        def UP_DATE(i,j):
                            c2.execute('UPDATE bdata2 SET LF =? WHERE BBN =? ',(i,j))
                            conn2.commit()
                        m = st.text_input(':شماره بلوک انفجاری')
                        k = st.slider("New LF", 0, 20, 0)
                        UP_DATE(k,m)
                    elif kk == 'LM':
                        def UP_DATE(i,j):
                            c2.execute('UPDATE bdata2 SET LM =? WHERE BBN =? ',(i,j))
                            conn2.commit()
                        m = st.text_input(':شماره بلوک انفجاری')
                        k = st.slider("New LM", 0, 20, 0)
                        UP_DATE(k,m)
                    elif kk == 'WM':
                        def UP_DATE(i,j):
                            c2.execute('UPDATE bdata2 SET WM =? WHERE BBN =? ',(i,j))
                            conn2.commit()
                        m = st.text_input(':شماره بلوک انفجاری')
                        k = st.slider("New WM", 0.0, 1.0, 0.0)
                        UP_DATE(k,m)
                    elif kk == 'WL':
                        def UP_DATE(i,j):
                            c2.execute('UPDATE bdata2 SET WL =? WHERE BBN =? ',(i,j))
                            conn2.commit()
                        m = st.text_input(':شماره بلوک انفجاری')
                        k = st.slider("New WL", 0.0, 1.0, 0.0)
                        UP_DATE(k,m)
                    elif kk == 'RLW':
                        def UP_DATE(i,j):
                            c2.execute('UPDATE bdata2 SET RLW =? WHERE BBN =? ',(i,j))
                            conn2.commit()
                        m = st.text_input(':شماره بلوک انفجاری')
                        k = st.slider("New RLW", 0, 25, 0)
                        UP_DATE(k,m)
                    elif kk == 'FE':
                        def UP_DATE(i,j):
                            c2.execute('UPDATE bdata2 SET FE =? WHERE BBN =? ',(i,j))
                            conn2.commit()
                        m = st.text_input(':شماره بلوک انفجاری')
                        k = st.slider("New FE", 0.0, 1.0, 0.0)
                        UP_DATE(k,m)
                    
                    elif kk == 'BBN':
                        def UP_DATE(i,j):
                            c2.execute('UPDATE bdata2 SET BBN =? WHERE id =? ',(i,j))
                            conn2.commit()
                        m = st.text_input(':Block ID')
                        k = st.text_input(':شماره جدید بلوک انفجاری')
                        UP_DATE(k,m)
            else:
                st.warning("Incorrect Username/Password")

elif choice == "SignUp":
    st.subheader("Create New Account")
    new_user = st.text_input("Username")
    new_password = st.text_input("Password",type='password')

    if st.button("Signup"):
        create_usertable()
        add_userdata(new_user,make_hashes(new_password))
        st.success("You have successfully created a valid Account")
        st.info("Go to Login Menu to login")

#if __name__ == '__main__':
    #main()

#############################################################
#############################################################

