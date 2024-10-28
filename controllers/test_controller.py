from flask import Blueprint, request, jsonify, send_file
from gtts import gTTS
import os
import io


test_blueprint = Blueprint('test', __name__)

@test_blueprint.route('/test', methods = ['POST'])
def get_test():

    data = request.get_json()
    text = data.get('text')

    try:
        # tts =  gTTS(text = 'test', lang = 'en')
        
        # tts =  gTTS(text = 'สวัสดีชาวโลก', lang = 'th')
        # tts =  gTTS(text = 'กอไก่', lang = 'th')
        tts =  gTTS(text, lang = 'th')

        audio_bytes = io.BytesIO()
        tts.write_to_fp(audio_bytes)
        audio_bytes.seek(0)
        return send_file(
            audio_bytes,
            mimetype='audio/mpeg',
            as_attachment=False,
            download_name="output.mp3"
        )
        # return jsonify({'name': 'PPM', 'email': 'p@mc.o'})
    except Exception as e:
        return jsonify({"error": str(e)}), 500    