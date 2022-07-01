import streamlit as st
import pandas as pd
import numpy as np
import tabula
from tabula import convert_into
from PIL import Image
import telebot
from telethon.sync import TelegramClient
from telethon.tl.types import InputPeerUser, InputPeerChannel
from telethon import TelegramClient, sync, events
import telesender

import asyncio
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

def driver(uploaded_file):
    tabula.convert_into(uploaded_file, "temporary.csv", output_format="csv", pages='all')
    df = pd.read_csv('temporary.csv')
    i = df[((df.Htno == 'Htno') &( df.Subcode == 'Subcode') & (df.Subname == 'Subname') & (df.Grade == 'Grade') & (df.Credits == 'Credits'))].index
    df.drop(i,inplace=True)

    df.reset_index(inplace=True)
    del df['index']
    subjects = df['Subname'].unique()
    htno = df['Htno'].unique()
    sub_code = df['Subcode'].unique()
    sub_dict = dict(zip(sub_code,subjects))
    grade_count = df['Grade'].value_counts().to_dict()
    
    grade_dict = {'O':10,'A':9,'B':8,'C':7,'D':6,'F':-1}

    df['GradePt'] = (df['Grade'].map(grade_dict).fillna(0))
    df['GradePt'] = df['GradePt'].astype(float)
    df = df.replace(to_replace ="-",
                    value ="0")
    df['Credits'] = df['Credits'].astype(float)
    df['CreditsMul'] = df.Credits * df.GradePt
    
    stud_sgpa_dict= {}
    stud_percentage_dict= {}

    ranks_df = pd.DataFrame()
    ranks_df['Rollno'] = df['Htno'].unique()

    for i in htno:
        stud_df = df[df['Htno']==i]
        stud_df.head(10)
        sem_total_crdits = stud_df['Credits'].sum()
        stud_total_crdits = stud_df['CreditsMul'].sum()
        stud_sgpa = round(stud_total_crdits/sem_total_crdits,4)
        stud_sem_percentage = (stud_sgpa*10)-7.5
        stud_sgpa_dict.update({i:stud_sgpa})
        stud_percentage_dict.update({i:stud_sem_percentage})


    stud_sgpa = pd.DataFrame([stud_sgpa_dict])
    stud_sgpa_df = stud_sgpa.T
    stud_percentage = pd.DataFrame([stud_percentage_dict]) 
    stud_percentage_df = stud_percentage.T

    ranks_df = pd.concat([stud_sgpa_df,stud_percentage_df],axis=1,sort=True)
    ranks_df.columns = ['Sgpa','Percentage']
    ranks_df = ranks_df.sort_values(by=['Sgpa'], ascending=False)
    ranks_df.reset_index(inplace=True)
    ranks_df.rename(columns = {'index':'Rollno'}, inplace = True)
    ranks_df.index+=1
    ranks_df['Rank'] = ranks_df.index
    
    class_topper_roll = ranks_df.iloc[0]['Rollno']
    
    avg_sgpa = round(ranks_df['Sgpa'].mean(),4)
    avg_percentage = round(ranks_df['Percentage'].mean(),4)
    
    avg_subject_grade_dict = {}
    for subject in subjects:
        single_subject = df.loc[df['Subname']==subject]
        single_subject = single_subject['Grade'].value_counts().to_dict()
        avg_grade = max(single_subject, key= lambda x: single_subject[x])
        avg_subject_grade_dict.update({subject:avg_grade})

    st.text('')
    st.text('')
    roll = str(st.text_input('Enter Your Roll Number: '))
    if roll:
        stud_df = df[df['Htno']==roll]
        temp_stud_df = df[df['Htno']==class_topper_roll]
        sem_total_credits = temp_stud_df['Credits'].sum()
        stud_total_credits = stud_df['CreditsMul'].sum()
        stud_sgpa = round(stud_total_credits/sem_total_credits,4)
        stud_sem_percentage = (stud_sgpa*10)-7.5
            
        temp_rank_df = ranks_df.loc[ranks_df['Rollno']==roll]
        stdu_rank = temp_rank_df['Rank'].tolist()
        stdu_rank = stdu_rank[0]
            

        stud_df = stud_df.drop(['Htno', 'Subcode','Credits','GradePt','CreditsMul'], axis = 1)
        stud_df_dict = stud_df.to_dict()
        message = ''
        st.header("Your Grades in this Semester: ")
        for i in stud_df_dict['Subname'].keys():
            temp_msg=''
            message += str(stud_df_dict['Subname'].get(i)+' --> '+stud_df_dict['Grade'].get(i))+'\n'
            temp_msg = str(stud_df_dict['Subname'].get(i)+' --> '+stud_df_dict['Grade'].get(i))
            st.text(temp_msg)
        message+= '\n'+'**Your Total Credits = '+str(stud_total_credits )+'**'+'\n'+'Semester Total Credits = '+str(sem_total_credits)
        message+= '\n\n'+'**Your SGPA is '+str(stud_sgpa)+'**'+'\n'+'Average SGPA in class is '+str(avg_sgpa)
        message+= '\n\n'+'**Your Semester percentage is '+str(stud_sem_percentage)+'%'+'**'+'\n'+'Average Semester percentage in class is '+str(avg_percentage)+'%'
        message+= '\n\n'+f'**You secured {stdu_rank} Rank in the class'+'**'
        
        st.header('Your Total Credits = '+str(stud_total_credits ))    
        st.subheader('Semester Total Credits = '+str(sem_total_credits))
        st.text('')
        st.header('Your SGPA is '+str(stud_sgpa))    
        st.subheader('Average SGPA in class is '+str(avg_sgpa))
        st.text('')
        st.header('Your Semester percentage is '+str(stud_sem_percentage)+'%')    
        st.subheader('Average Semester percentage in class is '+str(avg_percentage)+'%')
        st.text('')
        st.header(f'You secured {stdu_rank} Rank in the class')
        
        st.text('')
        st.text('')
        st.subheader("Want to send your marks as message ?")
        col1,col2 = st.columns(2)
    
        with col1:
            st.text('')
            user_name = str(st.text_input("Enter your Telegrame username without @: "))
            st.warning('Telegram usernames are case sensitive, you can find your username in telegram setting -> username')
            st.info("Note for Privacy Concern: No User Data will be stored in the server, it is deleted immediatley after prorgam terimination")
            sender = st.button('Send via telegram')
            if sender:
                telesender.telesendmsg(message,user_name)
                st.success('Message sent')

        with col2:
            st.text('')
            user_name = (st.text_input('Enter Your Whatsapp Number: '))
            st.warning('Enter your whatsapp number WITHOUT the country code i.e +91')
            st.info("Note for Privacy Concern: No User Data will be stored in the server, it is deleted immediatley after prorgam terimination")
            sender = st.button('Send via Whatsapp')
            if sender:
                try:
                    st.error("Functionality is still under bug fixing please try again later")
                except:
                    st.warning("An error occured, please try again")        
        
        
        st.text('')
        st.subheader('Basic Stats:')
        st.text('')
        st.write('Average Grades in each subject: ');
        for subject in avg_subject_grade_dict.keys():
            temp_text=''
            temp_text+= str(subject+' --> '+str(avg_subject_grade_dict.get(subject)))
            st.text(temp_text)
    

def main():
    st.set_page_config(layout="wide")
    col1,col2 = st.columns((1,5))
    with col1:
        image = Image.open('Vignan_logo.png')
        st.image(image)
    with col2:
        st.markdown("<h1> Vignan's Institute of<span style = 'display: block;'> Information Technology</span> </h1>",unsafe_allow_html=True)
        st.caption("Re-accredited by NAAC with 'A++' Grade & NBA")
    st.subheader('Welcome to Sem Grade Analysis')
    st.markdown("<p><TT>Designed and Developed by <a style='text-decoration:none;color:red' target='_blank' href='https://github.com/sasivatsal7122'>Team - Elite</a></TT></p>", unsafe_allow_html=True)
    #st.caption("20L31A5413 , Department of AI&DS")
    uploaded_file = st.sidebar.file_uploader("Upload Results PDF: ")
    if uploaded_file:
        driver(uploaded_file)
    

if __name__=='__main__':
    main()