import distyll
from distyll.db import add_yt_to_db
import weaviate
import os

client = weaviate.connect_to_wcs(
    cluster_url=os.getenv("JP_WCS_URL"),
    auth_credentials=weaviate.auth.AuthApiKey(os.getenv("JP_WCS_ADMIN_KEY")),
    headers={"X-OpenAI-Api-Key": os.getenv("OPENAI_APIKEY")},
)

urls = [
    "https://youtu.be/K1R7oK2piUM",  # Our Mad Journey of Building a Vector Database in Go - Weaviate at FOSDEM 2023
    "https://youtu.be/4sLJapXEPd4",  # Weaviate: An Architectural Deep Dive (Etienne Dilocker)
    "https://youtu.be/KT2RFMTJKGs",  # Etienne AI conference talk on multi-tenancy
    # "https://youtu.be/-ebMbqkdQdg",  # Margot Robbie interview
    # "https://youtu.be/5p248yoa3oE",  # Andrew Ng interview
    # "https://youtu.be/LkV5DTRNxAg",  # Connor Gorilla video
    # "https://youtu.be/nMMNkfSQuiU",  # Starfield (video game) review - from a week ago
    # "https://youtu.be/enRb6fp5_hw",  # Stanford: NLU Information Retrieval: Guiding Ideas Spring 2023
]

for yt_url in urls:
    add_yt_to_db(client=client, yt_url=yt_url)

client.close()
