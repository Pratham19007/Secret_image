from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
import io
import base64
from PIL import Image

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Store encrypted image and key in memory for demo
encrypted_image_bytes = None
encryption_key = None

def xor_encrypt(data, key):
    key_bytes = key.encode('utf-8')
    return bytes([b ^ key_bytes[i % len(key_bytes)] for i, b in enumerate(data)])

def xor_decrypt(data, key):
    return xor_encrypt(data, key)  # XOR is symmetric

@app.route('/', methods=['GET', 'POST'])
def image_encrypt():
    global encrypted_image_bytes, encryption_key
    encrypted_img = None
    decrypted_img = None
    show_decrypt_form = False
    if request.method == 'POST':
        if 'image' in request.files and 'set_key' in request.form:
            # Encrypt and store
            file = request.files['image']
            key = request.form.get('set_key')
            if file.filename and key:
                img_bytes = file.read()
                encrypted_image_bytes = xor_encrypt(img_bytes, key)
                encryption_key = key
                encrypted_img = base64.b64encode(encrypted_image_bytes).decode('utf-8')
                show_decrypt_form = True
        elif 'decrypt_key' in request.form:
            # Try to decrypt
            key = request.form.get('decrypt_key')
            if encrypted_image_bytes and key:
                try:
                    decrypted_bytes = xor_decrypt(encrypted_image_bytes, key)
                    img = Image.open(io.BytesIO(decrypted_bytes))
                    buf = io.BytesIO()
                    img.save(buf, format='PNG')
                    buf.seek(0)
                    decrypted_img = base64.b64encode(buf.read()).decode('utf-8')
                except Exception:
                    decrypted_img = 'ERROR'
    return render_template('image_encrypt.html', encrypted_img=encrypted_img, show_decrypt_form=show_decrypt_form, decrypted_img=decrypted_img)

if __name__ == '__main__':
    app.run(debug=True)
