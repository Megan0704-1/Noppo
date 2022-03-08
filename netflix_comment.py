from datetime import datetime
import jieba
from wordcloud import WordCloud
import streamlit as st
import pandas as pd
from google.cloud import firestore
import matplotlib.pyplot as plt


# @st.cache(suppress_st_warning=True)
def data_loading():
    doc_ref = df.collection('Comments').document(query)
    doc_dt = doc_ref.get().to_dict()
    img_url = doc_ref.get().get('img')
    introduction = doc_ref.get().get('info')
    scores = {'豆瓣': doc_dt['豆瓣'], 'IMDb': doc_ref.get().get(
        'imdb'), '爛番茄': (doc_ref.get().get('rt_tm'), doc_ref.get().get('rt_aad'))}
    print('Scores loaded')
    date = [str(doc.get('date'))[:10]
            for doc in doc_ref.collection('dates').stream()]
    fb_sent = [round(doc.get('sent')*10, 2)
               for doc in doc_ref.collection('sents').stream()]
    print('Date and Sentiment loaded')
    pc = []
    nc = []
    for doc in doc_ref.collection('pos_cms').stream():
        cm_dt = doc.to_dict()
        try:
            try:
                cm_dt['time'] = datetime.strptime(
                    str(cm_dt['time']), '%Y-%m-%d %H:%M:%S')
            except:
                pass
            cm_dt['sentiment'] = round(cm_dt['sentiment']*10, 2)
            pc.append(cm_dt)
        except Exception as err:
            print(err)
            continue

    for doc in doc_ref.collection('neg_cms').stream():
        cm_dt = doc.to_dict()
        try:
            try:
                cm_dt['time'] = datetime.strptime(
                    str(cm_dt['time']), '%Y-%m-%d %H:%M:%S')
            except:
                pass
            cm_dt['sentiment'] = round(cm_dt['sentiment']*10, 2)
            nc.append(cm_dt)
        except Exception as err:
            print(err)
            continue
    print('fb comments loaded')

    dcard_sent = []
    pos_dcard = []
    neg_dcard = []
    for doc in doc_ref.collection('dcard_cms').stream():
        dt = doc.to_dict()
        c_dt = dict()
        c_dt['text'] = dt['text']
        c_dt['sentiment'] = round(dt['sentiment']*10, 2)
        if c_dt['sentiment'] >= 5:
            pos_dcard.append(c_dt)
        else:
            neg_dcard.append(c_dt)
        # dcard_comment.append(c_dt)
        dcard_sent.append(c_dt['sentiment'])

    print('dcard comments loaded')
    return scores, img_url, introduction, date, fb_sent, pc, nc, dcard_sent, pos_dcard, neg_dcard, doc_ref, doc_dt


st.set_option('deprecation.showPyplotGlobalUse', False)
df = firestore.Client.from_service_account_json(
    './netflix-comment-system-firebase-adminsdk-hq5cn-9c691199bd.json')

title = '<p style="font-family:sans-serif; font-size: 42px;">Noppo</p>'
st.sidebar.markdown(title, unsafe_allow_html=True)
st.sidebar.header('Netflix原創影劇評價整合平台')

with open('./drama_list.txt') as fh:
    drama_list = [d[:-1] for d in fh.readlines()]

selection = st.sidebar.selectbox(
    '展開選單或直接搜尋', drama_list, drama_list.index('魷魚遊戲'))
st.title(selection)
query = selection

if query not in drama_list:
    st.write('Not found')
else:
    # Data Preparation
    scores, img_url, introduction, date, fb_sent, pc, nc, dcard_sent, pos_dc, neg_dc, doc_ref, doc_dt = data_loading()

    jieba.dt.cache_file = 'jieba.cache.new'
    all_text = doc_dt['all_text']

    for cm in pos_dc + neg_dc:
        all_text += cm['text']

    # wordcloud
    with open('./stopwords.txt') as fh:
        stopword = [d[:-1] for d in fh.readlines()]
    docs = ' '.join([w for w in jieba.cut(all_text)
                     if w not in stopword and len(w) > 3])
    try:
        wordcloud = WordCloud(
            margin=2, font_path='./setofont.ttf').generate(docs)
    except:
        pass

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

    if len(pc) > 0 or len(nc) > 0:
        st.header('臉書網友這樣說')
        st.write(
            '我們從「NETFLIX 新台灣討論區(非官方)」中找出與該劇相關的貼文並整理底下留言，透過以外送平台評論訓練的情緒分析模型來幫每則留言計算情緒分數，作為分類之依據。')
        col1, col2 = st.columns(2)

        col1.subheader('喜歡的人認為')
        for c in pc:
            sent = c['sentiment']
            col1.write('---')
            col1.write(c['text'])
            col1.markdown(
                f"<p style='text-align: right;'>情緒分數 {sent}/10</p>", unsafe_allow_html=True)
            # col1.write(f'給分 {sent}')
            col1.write(c['time'])

        col2.subheader('不喜歡的人認為')
        for c in nc:
            sent = c['sentiment']
            col2.write('---')
            col2.write(c['text'])
            col2.markdown(
                f"<p style='text-align: right;'>情緒分數 {sent}/10</p>", unsafe_allow_html=True)
            # col2.write(f'給分 {sent}')
            col2.write(c['time'])

    if len(fb_sent) > 0:
        st.subheader('臉書留言情緒分佈')
        n, bins, patches = plt.hist(fb_sent, bins=20)
        plt.xlabel("scores")
        plt.ylabel("frequency")
        plt.title("Sentiment Score Histogram Plot")
        plt.show()
        st.pyplot()

    if len(date) > 0:
        st.subheader('討論度分佈')
        date = pd.DataFrame(date)
        try:
            x = [k[0] for k in pd.DataFrame(date).value_counts(
                sort=False).to_dict().keys()]
            y = [v for v in pd.DataFrame(date).value_counts(
                sort=False).to_dict().values()]
            k = plt.barh(x, y)
            plt.show()
            st.pyplot()
        except:
            pass

    # pos_dc = [c for c in dcard_comment if 9.5 > c['sentiment'] > 5]
    # neg_dc = [c for c in dcard_comment if 1.5 < c['sentiment'] < 5]
    pos_dc.sort(key=lambda x: float(x['sentiment']), reverse=True)
    neg_dc.sort(key=lambda x: float(x['sentiment']))
    st.header('迪卡網友這樣說')
    col1, col2 = st.columns(2)

    col1.subheader('喜歡的人認為')
    pc = pos_dc[:10] if len(pos_dc) > 10 else pos_dc
    for c in pc:
        sent = c['sentiment']
        col1.write('---')
        col1.write(c['text'])
        col1.markdown(
            f"<p style='text-align: right;'>情緒分數 {sent}/10</p>", unsafe_allow_html=True)

    col2.subheader('不喜歡的人認為')
    nc = neg_dc[:10] if len(neg_dc) > 10 else neg_dc
    for c in nc:
        sent = c['sentiment']
        col2.write('---')
        col2.write(c['text'])
        col2.markdown(
            f"<p style='text-align: right;'>情緒分數 {sent}/10</p>", unsafe_allow_html=True)

    if len(dcard_sent) > 0:
        st.subheader('Dcard留言情緒分佈')
        n, bins, patches = plt.hist(dcard_sent, bins=20)
        plt.xlabel("scores")
        plt.ylabel("frequency")
        plt.title("Sentiment Score Histogram Plot")
        plt.show()
        st.pyplot()

    if len(all_text) > 0:
        try:
            st.subheader('文字雲')
            st.write('透過社群留言的文字去產出關鍵字之文字雲')
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis("off")
            plt.show()
            st.pyplot()
        except:
            pass
