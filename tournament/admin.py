from django.contrib import admin
from .models import Tournament, UserTournament, Match
from django import forms


class TournamentAdmin(admin.ModelAdmin):
    list_display = ['name', 'game_map_display']

    def game_map_display(self, obj):
        if obj.game_map:
            return "Uploaded"
        return "No file"

    game_map_display.short_description = 'Game Map'

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'game_map':
            return forms.FileField(label='Game Map', required=False)
        return super().formfield_for_dbfield(db_field, **kwargs)

    def save_model(self, request, obj, form, change):
        if 'game_map' in form.cleaned_data:
            uploaded_file = form.cleaned_data['game_map']
            if uploaded_file:
                obj.game_map = uploaded_file.read()
        super().save_model(request, obj, form, change)


admin.site.register(Tournament, TournamentAdmin)
admin.site.register(UserTournament)
admin.site.register(Match)
