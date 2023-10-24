# Noppo: Netflix Comment Aggregator & Analyzer

Dive deep into the world of Netflix's original series and movies with Noppo! This platform not only aggregates comments and ratings from various sources but also provides insightful sentiment analysis to gauge audience reactions.

## 🚀 Features

- **Dynamic Data Loading**: Seamlessly fetches comments, ratings, and other relevant data from Firestore.
- **Sentiment Superpower**: Uses TensorFlow to perform sentiment analysis on comments, giving you a pulse of the audience's feelings.
- **Web Crawling Wizards**: Employs Selenium and BeautifulSoup to crawl and gather data from multiple platforms.
- **Interactive Visualizations**: Offers histogram plots for sentiment distribution and word clouds for keyword visualization, making data interpretation a breeze.
- **Sleek UI**: Built with Streamlit, offering an intuitive and interactive web application experience.
- **Cloud-Backed**: Uses Firebase as a robust backend database to store and manage data.

## 🛠 Tech Stack

- **TensorFlow**: For training and deploying the sentiment analysis model.
- **Selenium & BeautifulSoup**: Powerful tools for web scraping and data extraction.
- **Streamlit**: Rapidly build and deploy interactive web applications.
- **Firebase**: Cloud database for real-time data storage and retrieval.
- **Python**: The backbone of the application, tying all components together.

## 📚 Data Sources

- **Facebook**: Dive into public group posts and comments.
- **Dcard**: Explore discussion board posts and comments.
- **Douban**: Get ratings and reviews of movies and series.
- **IMDb & Rotten Tomatoes**: Fetch renowned ratings and reviews.
- **Wikipedia**: Source general information and trivia.

[Additional code and resources can be found here.](https://drive.google.com/drive/folders/13NmCzBN1ZHL_l6h-PGGuDQiw57P1n5Zo?usp=sharing)

## 🛠 Setup & Run

1. **Clone & Setup**: Clone the repository and navigate to its directory.
2. **Dependencies**: Install the required packages using:
   ```bash
   pip install -r requirements.txt
   ```
3. **Credentials**: Ensure you have the necessary credentials for Firestore.
4. **Launch**: Fire up the Streamlit app:
   ```bash
   streamlit run netflix_comment.py
   ```

## 🤝 Contributing

We welcome innovators and thinkers! Feel free to fork the repository, make your enhancements, and submit pull requests. Let's make Noppo even better together!
