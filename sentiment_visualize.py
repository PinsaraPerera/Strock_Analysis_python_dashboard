import streamlit as st

# Simulate a sentiment score for demonstration purposes

# sentiment_score = st.slider("Sentiment Score:", min_value=0.0, max_value=1.0, value=0.5, step=0.01)

def normalize_sentiment(score):
    return (score + 1) / 2

def set_sentiment_score(sentiment_score):

    # Normalize sentiments for visual representation
    sentiment_score = normalize_sentiment(sentiment_score)

    # Determine the sentiment based on the score
    if sentiment_score < 0.5:
        sentiment = "Negative"
        color = "#FF4B4B"  # Red
    elif sentiment_score > 0.5 and sentiment_score < 0.6:
        sentiment = "Neutral"
        color = "#FFDD59"  # Yellow
    else:
        sentiment = "Positive"
        color = "#57CC99"  # Green

    # Display the sentiment score using a metric widget
    st.metric(label="Sentiment Analysis Score", value=f"{sentiment_score:.2f}", delta=sentiment, delta_color="off")

    # Create a progress bar with dynamic color
    progress_bar = st.progress(sentiment_score, )

    # Use custom HTML to change the progress bar color
    st.markdown(f"""
        <style>
        .stProgress > div > div > div > div {{
            background-color: {color};
        }}
        </style>""",
        unsafe_allow_html=True
    )

    # Optional: Display textual sentiment evaluation
    st.write(f"The sentiment analysis indicates a **{sentiment}** sentiment.")
