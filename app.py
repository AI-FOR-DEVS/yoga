import cv2
import base64
import openai
import streamlit as st
import tempfile


def generate_base64_frames(video):

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmpfile:
        tmpfile.write(video.read())
        video_filename = tmpfile.name

    video = cv2.VideoCapture(video_filename)

    base64Frames = []

    while video.isOpened():
        success, frame = video.read()
        if not success:
            break
        _, buffer = cv2.imencode(".jpg", frame)
        base64Frames.append(base64.b64encode(buffer).decode("utf-8"))
    video.release()

    return base64Frames


def generate_voiceover_text(frames):
    chat_completion = openai.chat.completions.create(
        model="gpt-4-vision-preview",
        max_tokens=200,
        messages=[
            {
                "role": "user",
                "content": [
                    f"As a Yoga Instructor, could you provide specific tips based on these video frames to enhance the yoga posture? Please do not include any personal information",
                    * [{"image": x, "resize": 512} for x in frames[0::30]]
                ],
            }
        ]
    )

    result = chat_completion.choices[0].message.content
    return result

def main():
    st.header('Analyze Yoga Posture')
    uploaded_file = st.file_uploader("choose a file")

    if uploaded_file is not None:
        st.video(uploaded_file)

    if st.button('Run', type="primary") and uploaded_file is not None:
        with st.spinner('Running ...'):
            frames = generate_base64_frames(uploaded_file)
            text = generate_voiceover_text(frames)
            st.write(text)

if __name__ == '__main__':
    main()