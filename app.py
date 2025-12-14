import streamlit as st
import pickle
import requests

# ---------------------------------
# Page Configuration
# ---------------------------------
st.set_page_config(
    page_title="🎵 Song Recommender",
    page_icon="🎧",
    layout="wide"
)

# ---------------------------------
# Load Data
# ---------------------------------
@st.cache_data
def load_data():
    songs = pickle.load(open("songs.pkl", "rb"))
    similarity = pickle.load(open("similarity.pkl", "rb"))
    return songs, similarity

songs, similarity = load_data()

# ---------------------------------
# Fetch Poster using iTunes API
# ---------------------------------
@st.cache_data(show_spinner=False)
def fetch_poster(song_name):
    url = "https://itunes.apple.com/search"
    params = {
        "term": f"{song_name} song",
        "media": "music",
        "limit": 1
    }

    response = requests.get(url, params=params, timeout=5)
    data = response.json()

    if data.get("resultCount", 0) > 0:
        return data["results"][0]["artworkUrl100"].replace("100x100", "400x400")
    return None

# ---------------------------------
# Recommendation Logic
# ---------------------------------
def recommend(song_name, n=5):
    idx = songs[songs['track_name'] == song_name].index[0]

    similarity_scores = list(enumerate(similarity[idx]))
    similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)

    rec_names, rec_posters = [], []

    for i in similarity_scores[1:n+1]:
        track = songs.iloc[i[0]].track_name
        rec_names.append(track)
        rec_posters.append(fetch_poster(track))

    return rec_names, rec_posters

# ---------------------------------
# UI Header
# ---------------------------------
st.markdown(
    """
    <h1 style='text-align: center;'>🎵 Music Recommendation System</h1>
    <p style='text-align: center; font-size: 18px; color: gray;'>
        Discover similar songs with AI-powered recommendations
    </p>
    """,
    unsafe_allow_html=True
)

st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------------
# Song Selector
# ---------------------------------
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    selected_song = st.selectbox(
        "🎶 Select a song you like",
        songs['track_name'].values
    )

st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------------
# Recommendation Button
# ---------------------------------
col1, col2, col3 = st.columns([2, 1, 2])
with col2:
    recommend_btn = st.button("🎧 Recommend Songs", use_container_width=True)

# ---------------------------------
# Display Recommendations
# ---------------------------------
if recommend_btn:
    with st.spinner("Finding similar songs for you 🎵..."):
        names, posters = recommend(selected_song)

    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("✨ Recommended for you")

    cols = st.columns(len(names))
    for i in range(len(names)):
        with cols[i]:
            st.markdown(
                """
                <div style='padding:10px; border-radius:15px;
                            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
                            text-align:center;'>
                """,
                unsafe_allow_html=True
            )

            if posters[i]:
                st.image(posters[i], use_container_width=True)
            else:
                st.image(
                    "https://via.placeholder.com/400x400?text=No+Image",
                    use_container_width=True
                )

            st.markdown(
                f"<p style='font-weight:600; margin-top:10px;'>{names[i]}</p>",
                unsafe_allow_html=True
            )

            st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------
# Footer
# ---------------------------------
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align:center; color:gray;'>Built with ❤️ using Streamlit & Machine Learning</p>",
    unsafe_allow_html=True
)
