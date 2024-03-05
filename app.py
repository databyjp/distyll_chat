import streamlit as st
import weaviate
from weaviate.classes.query import Filter, MetadataQuery
import os


MAX_N_CHUNKS = 15

st.set_page_config(layout="wide")

img_col, _, _ = st.columns([10, 30, 30])
with img_col:
    st.image("media/weaviate-logo-dark-name-transparent-for-light.png")
st.header("Better living through RAG")

video_options = [
    "https://youtu.be/K1R7oK2piUM",  # Our Mad Journey of Building a Vector Database in Go - Weaviate at FOSDEM 2023
    "https://youtu.be/4sLJapXEPd4",  # Weaviate: An Architectural Deep Dive (Etienne Dilocker)
    "https://youtu.be/KT2RFMTJKGs",  # Etienne AI conference talk on multi-tenancy
    "https://youtu.be/-ebMbqkdQdg",  # Margot Robbie interview
    "https://youtu.be/5p248yoa3oE",  # Andrew Ng interview
    "https://youtu.be/LkV5DTRNxAg",  # Connor Gorilla video
    "https://youtu.be/nMMNkfSQuiU",  # Starfield (video game) review - from a week ago
]

background, info, tab1, tab2 = st.tabs(
    ["Background", "Source data", "Demo", "Behind the magic"]
)
with background:
    with st.expander("Problem statement"):
        st.markdown("### There is way too much content out there")
        st.markdown("*****")
    with st.expander("Solution"):
        st.markdown(
            "### What if you didn't *have* to watch a video for its information?"
        )
        st.markdown("- Get a video summary.\n- Ask the video whatever you want.")
        st.markdown("*****")


with weaviate.connect_to_wcs(
    cluster_url=os.getenv("JP_WCS_URL"),
    auth_credentials=weaviate.auth.AuthApiKey(os.getenv("JP_WCS_RO_KEY")),
    headers={"X-OpenAI-Api-Key": os.getenv("OPENAI_APIKEY")},
) as client:
    chunks = client.collections.get("TextChunk")

    def get_youtube_title(video_url):
        try:
            response = chunks.query.fetch_objects(
                filters=Filter.by_property("url").equal(video_url), limit=1
            )
            title = response.objects[0].properties["title"]
            return title
        except:
            return "No title found"

    video_title_dict = {
        video_id: get_youtube_title(video_id) for video_id in video_options
    }
    title_video_dict = {v: k for k, v in video_title_dict.items()}

    with info:
        st.subheader("Available videos:")
        a, b, c = st.columns(3)
        columns = [a, b, c]

        for i, video in enumerate(video_options):
            col_index = i % 3
            with columns[col_index]:
                st.video(data=video)
                title = video_title_dict[video]
                st.write(title)

    with tab1:
        st.subheader("Talk to a video")

        video_selection = st.selectbox(
            "Select a video", options=title_video_dict.keys()
        )
        youtube_url = title_video_dict[video_selection]
        st.markdown("#### Extract anything from this video")
        user_question = st.text_input("Ask the video anything!")

    with tab2:
        st.subheader("How does it all work?")

    if len(user_question) > 3:
        with tab1:
            with st.expander("Raw data used:"):
                response = chunks.query.near_text(
                    query=user_question,
                    filters=Filter.by_property("url").equal(youtube_url),
                    limit=MAX_N_CHUNKS,
                )

                for resp_obj in response.objects:
                    st.write(resp_obj)

            prompt = f"""
            Answer the question: {user_question}.
            Feel free to use the text contained here.
            The answer should be well-written, succinct and thoughtful, using plain language even if the source material is technical.
            If there is no information, say 'The source material does not say.'.
            """

            response = chunks.generate.near_text(
                query=user_question,
                filters=Filter.by_property("url").equal(youtube_url),
                limit=MAX_N_CHUNKS,
                grouped_task=prompt,
            )

            # for resp_obj in response.objects:
            #     st.write(resp_obj)

            st.write(response.generated)

        with tab2:
            with st.expander("Code snippet:"):
                st.code(
                    '''
                    prompt = f"""
                    Answer the question: {user_question}.
                    Feel free to use the text contained here.
                    The answer should be well-written, succinct and thoughtful, using plain language even if the source material is technical.
                    If there is no information, say 'The source material does not say.'.
                    """,

                    response = chunks.generate.near_text(
                        filters=Filter.by_property("url").equal(youtube_url),
                        query=user_question,
                        limit=MAX_N_CHUNKS,
                        grouped_task=prompt
                    )

                    ''',
                    language="python",
                )
    else:
        with tab2:
            st.write("Run a search first and come back! :)")
