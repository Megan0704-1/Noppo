from facebook_scraper import get_posts
import pandas as pd

post_df_full = pd.DataFrame()
comments_df = pd.DataFrame()

num_of_pages = 30
group_id = '235385084142732'
count = 0
try:
    for post in get_posts(group=group_id, pages=num_of_pages, cookies='from_browser', options={'comments': True, 'progress': True}):
        post_entry = post
        fb_post_df = pd.DataFrame.from_dict(post_entry, orient='index')
        fb_post_df = fb_post_df.transpose(
        )[['post_id', 'time', 'post_text', 'likes', 'comments']]
        post_df_full = post_df_full.append(fb_post_df)
        tmp_df = pd.DataFrame(post['comments_full'])
        tmp_df['post_id'] = [post['post_id']] * tmp_df.shape[0]

        try:
            comments_df = comments_df.append(
                tmp_df[['post_id', 'comment_id', 'comment_time', 'comment_text']])
        except Exception as e:
            print(e)
            continue

        count += 1
        print(post['post_id'] + ' get!')
        print(f'Current number of posts: {count}\n')
        post_df_full.to_csv('./Posts_from_fb_raw.csv', index=False)
        comments_df.to_csv('./Comments_from_fb_raw.csv', index=False)
        print('Process saved!', post_df_full.shape,
              comments_df.shape, '\n\n')
        else:
            print('repeated!!!')

except Exception as e:
    print(e)
    post_df_full.to_csv('./Posts_from_fb_raw.csv', index=False)
    comments_df.to_csv('./Comments_from_fb_raw.csv', index=False)

post_df_full.to_csv('./Posts_from_fb_raw.csv', index=False)
comments_df.to_csv('./Comments_from_fb_raw.csv', index=False)
