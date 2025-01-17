from flask import Blueprint, request, jsonify, send_file, make_response
from gtts import gTTS
import os
import io


test_blueprint = Blueprint('test', __name__)

@test_blueprint.route('/test', methods = ['POST'])
def get_test():

    data = request.get_json()
    text = data.get('text')
    lang = data.get('lang') or 'th'

    
    try:
        # tts =  gTTS(text = 'test', lang = 'en')
        
        # tts =  gTTS(text = 'สวัสดีชาวโลก', lang = 'th')
        # tts =  gTTS(text = 'กอไก่', lang = 'th')
        tts =  gTTS(text, lang = lang)

        audio_bytes = io.BytesIO()
        tts.write_to_fp(audio_bytes)
        audio_bytes.seek(0)

        response = make_response(
            send_file(
                audio_bytes,
                mimetype='audio/mpeg',
                as_attachment=False,
                download_name=f"{text}.mp3"
            )
        )
        # response.headers["Cache-Control"] = "public, max-age=86400"
        return response
        # return jsonify({'name': 'PPM', 'email': 'p@mc.o'})
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500    