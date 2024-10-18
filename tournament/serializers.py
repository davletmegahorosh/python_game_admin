from rest_framework import serializers
from .models import Tournament
import json


class TournamentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tournament
        fields = ['name', 'game_map']

    def validate_game_map(self, value):
        try:
            import json
            if isinstance(value, bytes):
                value = value.decode('utf-8')
            decoded_map = json.loads(value)

            if not all(isinstance(i, list) for i in decoded_map):
                raise serializers.ValidationError("game_map должен быть двумерным массивом.")

            row_length = len(decoded_map[0])
            if not all(len(row) == row_length for row in decoded_map):
                raise serializers.ValidationError("Каждый подмассив должен быть одинаковой длины.")

            if len(decoded_map) != row_length:
                raise serializers.ValidationError("Массив должен быть квадратным (одинаковая длина и ширина).")

        except (json.JSONDecodeError, UnicodeDecodeError, AttributeError):
            raise serializers.ValidationError("Неверный формат или кодировка для game_map.")

        return value

    def create(self, validated_data):
        print(validated_data)
        name = validated_data['name']
        game_map = validated_data['game_map']

        tournament = Tournament.objects.create(name=name, game_map=game_map)

        return tournament

