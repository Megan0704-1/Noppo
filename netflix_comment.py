from datetime import datetime
import streamlit as st
import pandas as pd
from google.cloud import firestore

df = firestore.Client.from_service_account_json(
    './netflix-comment-system-firebase-adminsdk-hq5cn-9c691199bd.json')

st.sidebar.title('Netflixm原創影劇評論檢索系統')
top10 = st.sidebar.selectbox(
    '十大熱門影劇', ('魷魚遊戲', '欲罷不能', '摩登家庭', '魔鬼神探'))
search_query = st.sidebar.text_input('輸入想找的劇')

if search_query == '':
    st.title(top10)
    query = top10
else:
    st.title(search_query)
    query = search_query

doc_ref = df.collection('Comments').document(query)
pos_comment = []
for doc in doc_ref.collection('comment').stream():
    dt = doc.to_dict()
    pos_comment.append((dt['content'], dt['date'].date()))

neg_comment = []
for doc in doc_ref.collection('neg_comment').stream():
    dt = doc.to_dict()
    neg_comment.append((dt['content'], dt['date'].date()))

st.image('https://i1.wp.com/waynesan.com/wp-content/uploads/2021/09/%E9%AD%B7%E9%AD%9A%E9%81%8A%E6%88%B2-Squid-Game-1.jpg?w=1280&ssl=1')

introduction = doc_ref.get().get('introduction')
st.header('介紹')
st.write(introduction)

scores = []
for doc in doc_ref.collection('scores').stream():
    dt = doc.to_dict()
    if dt['source'] == '爛番茄':
        scores.append((dt['source'], dt['score'], dt['audienceScore']))
    else:
        scores.append((dt['source'], dt['score']))

st.header('知名網站評分')
ss = st.columns(3)
for i in range(3):
    if scores[i][0] == '爛番茄':
        ss[i].subheader(scores[i][0])
        ss[i].subheader('影評 - ' + str(scores[i][1]) + '/10')
        ss[i].subheader('觀眾 - ' + str(scores[i][2]) + '/10')
    else:
        ss[i].subheader(scores[i][0])
        ss[i].subheader(str(scores[i][1]) + '/10')

st.header('臉書網友這樣說')
col1, col2 = st.columns(2)

col1.subheader('喜歡的人認為')
for c in pos_comment:
    col1.write('---')
    col1.write(c[0])
    col1.write(f'給分 {8}')
    col1.write(c[1])

col2.subheader('不喜歡的人認為')
for c in neg_comment:
    col2.write('---')
    col2.write(c[0])
    col2.write(f'給分 {9}')
    col2.write(c[1])

st.header('迪卡網友這樣說')
col1, col2 = st.columns(2)

col1.subheader('喜歡的人認為')
for c in pos_comment:
    col1.write('---')
    col1.write(c[0])
    col1.write(f'給分 {8}')
    col1.write(c[1])

col2.subheader('不喜歡的人認為')
for c in neg_comment:
    col2.write('---')
    col2.write(c[0])
    col2.write(f'給分 {9}')
    col2.write(c[1])

st.header(f'綜合分數: {8.5}')
