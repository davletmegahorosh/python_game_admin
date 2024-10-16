import base64
import uuid
import os
from django.core.files.base import ContentFile
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

class Base64ImageField(serializers.ImageField):

    def to_internal_value(self, data):
        if isinstance(data, str):
            try:
                format, imgstr = data.split(';base64,')
                ext = format.split('/')[-1]
                decoded_data = base64.b64decode(imgstr)

                file_name = f"media/avatars/{uuid.uuid4()}.{ext}"
                output_file_path = os.path.join(file_name)

                with open(output_file_path, 'wb') as output_file:
                    output_file.write(decoded_data)

                return ContentFile(decoded_data, name=file_name)

            except (TypeError, ValueError, base64.binascii.Error) as e:
                raise ValidationError("Invalid base64 data")
        else:
            return super().to_internal_value(data)


