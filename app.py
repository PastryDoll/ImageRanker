import streamlit as st
import random
from PIL import Image
import itertools

st.set_page_config(
    page_title="Rank Images",
    layout="wide",  
)
st.title("Image Ranker")

def image_selected(idx):
    st.session_state.wins[idx] += 1
    if st.session_state.pairs:
        st.session_state.current_pair = st.session_state.pairs.pop(0)
    else:
        st.session_state.ranking_complete = True
    return True


#
## Upload Images
#
if 'images' not in st.session_state:
    uploaded_files = st.file_uploader("Choose images...", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

    if uploaded_files:
        images = [Image.open(uploaded_file) for uploaded_file in uploaded_files]
        st.session_state.images = images
else:
    if not st.session_state.get('ranking_started', False):
        st.write("Please upload one or more image files.")
#
## Main app
#
if st.session_state.get("images", False):

    images = st.session_state.images

    if 'images' not in st.session_state:
        st.session_state.images = images

    if 'pairs' not in st.session_state:
        st.session_state.pairs = list(itertools.combinations(range(len(images)), 2))
        random.shuffle(st.session_state.pairs)  

    if 'wins' not in st.session_state:
        st.session_state.wins = [0] * len(images)

    if 'current_pair' not in st.session_state:
        st.session_state.current_pair = st.session_state.pairs.pop(0)

    # Before ranking UI 
    if not st.session_state.get('ranking_started', False):
        st.write(f"Uploaded {len(images)} image(s)")
        st.button("Start Ranking", on_click=lambda: st.session_state.update({"ranking_started": True}))
        for i in range(0, len(uploaded_files), 4):
            cols = st.columns(4)
            for idx, uploaded_file in enumerate(uploaded_files[i:i+4]):
                image = Image.open(uploaded_file)
                with cols[idx]:
                    st.image(image, caption=f"Image {i+idx+1}", use_column_width=True)
              
    # After ranking UI
    if not st.session_state.get('ranking_complete', False) and st.session_state.get('ranking_started', False):
        idx1, idx2 = st.session_state.current_pair
        col1, col2 = st.columns(2)

        with col1:
            st.button(f"Select Image {idx1 + 1}", key=f"select_{idx1}", on_click=image_selected, args=[idx1])
            st.image(images[idx1], caption=f"Image {idx1 + 1}", use_column_width=True)

        with col2:
            st.button(f"Select Image {idx2 + 1}", key=f"select_{idx2}",on_click=image_selected, args=[idx2])
            st.image(images[idx2], caption=f"Image {idx2 + 1}", use_column_width=True)

    if st.session_state.get('ranking_complete', False):
        st.write("Ranking Complete!")

        ranked_images = sorted(enumerate(st.session_state.wins), key=lambda x: -x[1])

        st.write("Final Ranking:")
        for rank, (image_idx, wins) in enumerate(ranked_images, start=1):
            st.write(f"Rank {rank}: Image {image_idx + 1} with {wins} win(s)")
            st.image(images[image_idx], use_column_width=True)

