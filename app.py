import streamlit as st
import pickle
import requests
import gdown

# Google Drive file ID
file_id = "1HHVd-2L6JqkBpLh3wJIXw0AKlfoCxUpo"
download_url = f"https://drive.google.com/uc?id={file_id}"
file_path = "movies_data.pkl"


@st.cache_data
def load_data():
    # Download file from Google Drive
    gdown.download(download_url, file_path, quiet=False)

    # Load the pickle file
    with open(file_path, "rb") as f:
        data = pickle.load(f)

    return data["movies_df"], data["similarity"]


movies_df, similarity = load_data()

api_key = "352b2ab6701da1c72cdadbaccf4af3e6"




def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
    data = requests.get(url).json()
    if data.get('poster_path'):
        return "https://image.tmdb.org/t/p/w500" + data['poster_path']
    else:
        return "https://via.placeholder.com/500x750?text=No+Poster+Available"


def recommend(movie_title, n=5):
    movie_index = movies_df[movies_df['title'] == movie_title].index[0]
    scores = list(enumerate(similarity[movie_index]))
    sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)[1:n + 1]

    recommended_titles = []
    recommended_posters = []
    for i, _ in sorted_scores:
        movie_id = movies_df.iloc[i]['movie_id']
        recommended_titles.append(movies_df.iloc[i]['title'])
        recommended_posters.append(fetch_poster(movie_id))

    return recommended_titles, recommended_posters


# 2. Streamlit UI
st.title("Movie Recommender System")

movie_list = movies_df['title'].values
selected_movie = st.selectbox("Select a movie", movie_list)

if st.button("Recommend"):
    recommended_titles, recommended_posters = recommend(selected_movie, n=5)
    st.subheader("Top 5 Recommendations:")

    # Display side-by-side
    cols = st.columns(5)
    for idx, (title, poster) in enumerate(zip(recommended_titles, recommended_posters)):
        with cols[idx]:
            st.image(poster, use_container_width=True)
            st.write(title)
