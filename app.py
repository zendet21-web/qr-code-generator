from flask import Flask, render_template, request, send_file, redirect, url_for
import qrcode
import io
import base64
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Словарь для временного хранения данных (в реальном приложении используйте БД)
qr_data_store = {}


@app.route('/', methods=['GET', 'POST'])
def index():
    qr_image = None
    qr_id = None

    if request.method == 'POST':
        data = request.form.get('data', '').strip()

        if data:
            # Генерируем уникальный ID для QR-кода
            qr_id = secrets.token_urlsafe(8)

            # Сохраняем данные во временном хранилище
            qr_data_store[qr_id] = data

            # Создаем QR-код
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(data)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")

            # Сохраняем изображение в буфер
            img_buffer = io.BytesIO()
            img.save(img_buffer, format='PNG')
            img_buffer.seek(0)

            # Конвертируем в base64 для отображения
            qr_image = base64.b64encode(img_buffer.getvalue()).decode('utf-8')

    return render_template('index.html', qr_image=qr_image, qr_id=qr_id)


@app.route('/download/<qr_id>')
def download_qr(qr_id):
    """Скачать QR-код по его ID"""
    # Получаем данные по ID
    data = qr_data_store.get(qr_id)

    if not data:
        return "QR-код не найден или устарел", 404

    # Создаем QR-код
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    # Сохраняем в буфер
    img_buffer = io.BytesIO()
    img.save(img_buffer, format='PNG')
    img_buffer.seek(0)

    # Формируем имя файла
    safe_name = "".join(c for c in data[:30] if c.isalnum() or c in ('-', '_', '.'))
    if not safe_name:
        safe_name = "qr_code"
    filename = f"qr_code_{safe_name}.png"

    return send_file(
        img_buffer,
        as_attachment=True,
        download_name=filename,
        mimetype='image/png'
    )


# Очистка старых данных (опционально)
@app.before_request
def cleanup():
    # Здесь можно добавить логику очистки старых данных
    # Например, удалять записи старше 1 часа
    pass


if __name__ == '__main__':
    app.run(debug=True, port=5000)