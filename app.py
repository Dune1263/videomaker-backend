from flask import Flask, request, jsonify
import base64, os
from moviepy.editor import ImageSequenceClip

app = Flask(__name__)
FRAMES_FOLDER = "frames"
VIDEO_NAME = "output_video.mp4"
FPS = 12

os.makedirs(FRAMES_FOLDER, exist_ok=True)

@app.route("/upload_frame", methods=["POST"])
def upload_frame():
    data = request.json
    image_data = base64.b64decode(data["image_base64"])
    frame_number = data["frame_number"]
    filename = f"{FRAMES_FOLDER}/frame_{frame_number:03d}.png"
    with open(filename, "wb") as f:
        f.write(image_data)
    return jsonify({"status": "Frame guardado", "nombre": filename})

@app.route("/generate_video", methods=["POST"])
def generate_video():
    frames = sorted(os.listdir(FRAMES_FOLDER))
    frame_paths = [os.path.join(FRAMES_FOLDER, f) for f in frames]
    
    if not frame_paths:
        return jsonify({"status": "No hay frames"})

    clip = ImageSequenceClip(frame_paths, fps=FPS)
    clip.write_videofile(VIDEO_NAME, codec="libx264")
    return jsonify({"status": "Video creado", "video_path": VIDEO_NAME})

@app.route("/reset", methods=["POST"])
def reset():
    for f in os.listdir(FRAMES_FOLDER):
        os.remove(os.path.join(FRAMES_FOLDER, f))
    if os.path.exists(VIDEO_NAME):
        os.remove(VIDEO_NAME)
    return jsonify({"status": "Reiniciado"})

if __name__ == "__main__":
    app.run(port=5000)
