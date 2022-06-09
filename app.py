import streamlit as st
import pickle
import pandas as pd
import requests
import streamlit as st



st.set_page_config(page_title='anime recommender', page_icon=":shrine:", layout="wide")


def fetch(animeid):
    url = "https://anime-db.p.rapidapi.com/anime/by-id/{}".format(animeid)

    headers = {
        "X-RapidAPI-Host": "anime-db.p.rapidapi.com",
        "X-RapidAPI-Key": "08508dfb71msh436f4c5ba31679ep15b9dejsnf9893f55ca2a"
    }

    response = requests.request("GET", url, headers=headers)

    data = response.json()

    return data['title'],data['ranking'], data['image'],data['synopsis'],data['episodes'], data['status']

def recommend(anime):
    idx = anime_index[anime]

    # Get the pairwsie similarity scores of all anime with that anime
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Sort the anime based on the similarity scores

    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the scores of the 10 most similar anime
    sim_scores = sim_scores[0:6]
    #
    # # Get the anime indices
    anime_indices = [i[0] for i in sim_scores]
    #
    # # Return the top 10 most similar animes

    result = df[['anime_id']].iloc[anime_indices].drop(idx)
    recom_anime = []
    ranking = []
    anime_info = []
    sypnopsis = []
    episodes = []
    status = []
    for i in result.anime_id:
        recom_anime.append(fetch(i)[0])
        ranking.append(fetch(i)[1])
        anime_info.append(fetch(i)[2])
        sypnopsis.append(fetch(i)[3])
        episodes.append(fetch(i)[4])
        status.append(fetch(i)[5])


    return recom_anime, ranking, anime_info, sypnopsis, episodes,status

df = pickle.load(open('df1.pkl','rb'))
cosine_sim = pickle.load(open('cosine_sim.pkl','rb'))
anime_index = pickle.load(open('anime_index.pkl','rb'))

st.title('Anime recommender system')
st.image('dataset-cover.jpeg')

anime_dict = pickle.load(open('anime_dict3.pkl','rb'))
anime = pd.DataFrame(anime_dict)


option = st.selectbox('Type or select an Anime from the dropdown',
                      anime['name'].values)

if st.button('Recommend'):
    name, ranking, poster, sypnopsis, episodes, status = recommend(option)
    #
    # col1, col2, col3 = st.columns(3)
    # with col1:
    #     st.text(name[0])
    #     st.image(poster[0])
    # with col2:
    #     st.text(name[1])
    #     st.image(poster[1])
    # with col3:
    #     st.text(name[2])
    #     st.image(poster[2])
    with st.container():
        for i in range(5):
            st.title(name[i])
            st.write("Ranking: " + str(ranking[i]))
            st.image(poster[i])
            st.write(sypnopsis[i])
            st.write("Total number of episodes: "+str(episodes[i]))
            st.write("Status: "+status[i])


hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: show;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

