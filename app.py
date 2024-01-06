import cv2
import base64
import openai


# Load video

video = cv2.VideoCapture("yoga.mp4")

# Convert video into its frames

base64Frames = []

while video.isOpened():
    success, frame = video.read()
    if not success:
        break
    _, buffer = cv2.imencode(".jpg", frame)
    base64Frames.append(base64.b64encode(buffer).decode("utf-8"))
video.release()


# Send frames to OpenAI

chat_completion = openai.chat.completions.create(
    model="gpt-4-vision-preview",
    max_tokens=200,
    messages=[
        {
            "role": "user",
            "content": [
                f"As a Yoga Instructor, could you provide specific tips based on these video frames to enhance the yoga posture? Please do not include any personal information",
                * [{"image": x, "resize": 512} for x in base64Frames[0::30]]
            ],
        }
    ]
)

result = chat_completion.choices[0].message.content
print(result)
