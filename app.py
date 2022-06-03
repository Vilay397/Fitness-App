import random
import streamlit as st
from yt_extractor import get_info
import database_service as dbs


@st.cache(allow_output_mutation=True)
def get_yogas():
    return dbs.get_all_yoga()


def get_duration_text(duration_s):
    seconds = duration_s % 60
    minutes = int((duration_s / 60) % 60)
    hours = int((duration_s / (60*60)) % 24)
    text = ''
    if hours > 0:
        text += f'{hours:02d}:{minutes:02d}:{seconds:02d}'
    else:
        text += f'{minutes:02d}:{seconds:02d}'
    return text


st.title("Yoga APP")

menu_options = ("Today's yoga", "All yoga", "Add yoga")
selection = st.sidebar.selectbox("Menu", menu_options)

if selection == "All yoga":
    st.markdown(f"##All yoga")

    yogas = get_yogas()
    for yo in yogas:
        url = "https://youtu.be/" + yo["video_id"]
        st.text(yo['title'])
        st.text(f"{yo['channel']} - {get_duration_text(yo['duration'])}")

        ok = st.button('Delete yoga', key=yo["video_id"])
        if ok:
            dbs.delete_yoga(yo["video_id"])
            st.legacy_caching.clear_cache()
            st.experimental_rerun()

        st.video(url)
    else:
        st.text("No yoga in Database!")
elif selection == "Add yoga":
    st.markdown(f"##Add yoga")

    url = st.text_input('Please enter the video url')
    if url:
        yoga_data = get_info(url)
        if yoga_data is None:
            st.text("Could not find video")
        else:
            st.text(yoga_data['title'])
            st.text(yoga_data['channel'])
            st.video(url)
            if st.button("Add yoga"):
                dbs.insert_yoga(yoga_data)
                st.text("Added yoga!")
                st.legacy_caching.clear_cache()
else:
    st.markdown(f"## Today's Yoga")

    yogas = get_yogas()
    if not yogas:
        st.text("No yoga in Database!")
    else:
        yo = dbs.get_yoga_today()

        if not yo:
            # not yet defined
            yogas = get_yogas()
            n = len(yogas)
            idx = random.randint(0, n - 1)
            yo = yogas[idx]
            dbs.update_yoga_today(yo, insert=True)
        else:
            # first item in list
            wo = yo[0]

        if st.button("Choose another yoga"):
            yogas = get_yogas()
            n = len(yogas)
            if n > 1:
                idx = random.randint(0, n - 1)
                yo_new = yogas[idx]
                while yo_new['video_id'] == yo['video_id']:
                    idx = random.randint(0, n - 1)
                    yo_new = yogas[idx]
                yo = yo_new
                dbs.update_yoga_today(yo)

        url = "https://youtu.be/" + yo[0]["video_id"]
        st.text(yo[0]['title'])
        st.text(f"{yo[0]['channel']} - {get_duration_text(yo[0]['duration'])}")
        st.video(url)