import base64

def encode_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        # Читаем изображение в бинарном формате
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        # Возвращаем строку в формате base64 с заголовком
        return f"data:image/jpeg;base64,{encoded_string}"  # Измените 'jpeg' на 'png', если используете PNG

# Замените 'path/to/your/image.jpg' на путь к вашему изображению
image_base64 = encode_image_to_base64('/Users/Davlet/Downloads/Yo.jpg')

# Выводим результат
print(image_base64)
