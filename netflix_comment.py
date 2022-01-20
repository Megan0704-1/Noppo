from datetime import datetime
import streamlit as st
import pandas as pd
from google.cloud import firestore

df = firestore.Client.from_service_account_json(
    './netflix-comment-system-firebase-adminsdk-hq5cn-9c691199bd.json')

st.sidebar.title('Netflixm原創影劇評論檢索系統')
drama_list = [d.id for d in df.collection('Comments').get()]
radio = st.sidebar.radio('選擇模式', ('選單', '搜尋'))
if radio == '選單':
    selection = st.sidebar.selectbox(
        '所有影劇列表', drama_list, drama_list.index('魷魚遊戲'))
    st.title(selection)
    query = selection
else:
    search_query = st.sidebar.text_input('輸入想找的劇')
    st.title(search_query)
    query = search_query

if query not in drama_list:
    st.write('Not found')
else:
    # Data Preparation

    try:
        drama_df = pd.read_csv('./drama_complete_df.csv', index_col='name')
        drama_df['related_fb_post'] = drama_df['related_fb_post'].apply(
            lambda x: str(x)[1:-1].split(', ') if x != '[]' else [])
        comments_df = pd.read_csv(
            '../Comments_from_fb.csv', index_col='comment_id')
        img_url = drama_df.loc[query]['img']
        introduction = drama_df.loc[query]['info']
        scores = {'豆瓣': drama_df.loc[query]['douban'], 'IMDb': drama_df.loc[query]['imdb'], '爛番茄': (
            drama_df.loc[query]['rt_tm'], drama_df.loc[query]['rt_ad'])}
        all_comment = []
        for c_id in drama_df.loc[query]['related_fb_post']:
            comment = comments_df.loc[int(c_id)]
            cm_dt = dict()
            try:
                cm_dt['time'] = comment['comment_time']
                cm_dt['text'] = comment['comment_text']
                cm_dt['sentiment'] = round(comment['sentiment']*10, 2)
                all_comment.append(cm_dt)
            except Exception as err:
                print(err)
    except Exception as e:
        print(e)
        doc_ref = df.collection('Comments').document(query)
        img_url = doc_ref.get().get('img')
        introduction = doc_ref.get().get('info')
        scores = {'豆瓣': 'None', 'IMDb': 'None', '爛番茄': 'None'}
        for doc in doc_ref.collection('scores').stream():
            dt = doc.to_dict()
            scores[dt['source']] = (dt['tomatometer'], dt['audience']
                                    ) if dt['source'] == '爛番茄' else dt['score']
        print('Scores loaded')
        all_comment = []
        for doc in doc_ref.collection('related_posts').stream():
            post_id = doc.to_dict()['post_id']
            for comment in df.collection('Posts').document(str(post_id)).collection('comments').stream():
                cm_dt = dict()
                comment = comment.to_dict()
                try:
                    cm_dt['time'] = comment['time']
                    cm_dt['text'] = comment['text']
                    cm_dt['sentiment'] = comment['sentiment']
                    all_comment.append(cm_dt)
                except Exception as err:
                    continue
        print('comments loaded')

    # UI rendering
    if img_url != 'None':
        st.image(img_url, width=400)
    st.header('介紹')
    st.write(introduction)

    st.header('知名網站評分')
    ss = st.columns(3)
    source = ['豆瓣', 'IMDb', '爛番茄']
    for i in range(3):
        if i == 2:
            ss[i].subheader(source[i])
            ss[i].subheader('影評 - ' + str(scores[source[i]][0]))
            ss[i].subheader('觀眾 - ' + str(scores[source[i]][1]))
        else:
            ss[i].subheader(source[i])
            ss[i].subheader(str(scores[source[i]]) + '/10')

    pos_comment = [cm for cm in all_comment if 9 > cm['sentiment'] >= 5]
    neg_comment = [cm for cm in all_comment if 2 < cm['sentiment'] < 5]
    pos_comment.sort(key=lambda x: float(x['sentiment']), reverse=True)
    neg_comment.sort(key=lambda x: float(x['sentiment']))

    st.header('臉書網友這樣說')
    col1, col2 = st.columns(2)

    col1.subheader('喜歡的人認為')
    pc = pos_comment[:10] if len(pos_comment) > 10 else pos_comment
    for c in pc:
        sent = c['sentiment']
        col1.write('---')
        col1.write(c['text'])
        col1.markdown(
            f"<p style='text-align: right;'>情緒分數 {sent}/10</p>", unsafe_allow_html=True)
        # col1.write(f'給分 {sent}')
        col1.write(c['time'])

    col2.subheader('不喜歡的人認為')
    nc = neg_comment[:10] if len(neg_comment) > 10 else neg_comment
    for c in nc:
        sent = c['sentiment']
        col2.write('---')
        col2.write(c['text'])
        col2.markdown(
            f"<p style='text-align: right;'>情緒分數 {sent}/10</p>", unsafe_allow_html=True)
        # col2.write(f'給分 {sent}')
        col2.write(c['time'])
    # st.header('迪卡網友這樣說')
    # col1, col2 = st.columns(2)

    # col1.subheader('喜歡的人認為')
    # for c in pos_comment:
    #     col1.write('---')
    #     col1.write(c[0])
    #     col1.write(f'給分 {8}')
    #     col1.write(c[1])

    # col2.subheader('不喜歡的人認為')
    # for c in neg_comment:
    #     col2.write('---')
    #     col2.write(c[0])
    #     col2.write(f'給分 {9}')
    #     col2.write(c[1])

    # st.header(f'綜合分數: {8.5}')
