from django.db import models
from user.models import CustomUser

class Tournament(models.Model):
    name = models.CharField(max_length=100)
    game_map = models.TextField()
    first = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name='first_place_tournaments')
    second = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name='second_place_tournaments')
    third = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name='third_place_tournaments')

    def __str__(self):
        return f"tournament: {self.name}"

class UserTournament(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='participants')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_tournaments')
    file = models.FileField(upload_to='tournament_files/')

    def __str__(self):
        return f"{self.user} participates in {self.tournament}"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['tournament', 'user'], name='unique_user_tournament')
        ]

class Match(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='matches')
    player_1 = models.ForeignKey(UserTournament, on_delete=models.CASCADE, related_name='player_1_matches')
    player_2 = models.ForeignKey(UserTournament, on_delete=models.CASCADE, related_name='player_2_matches')
    winner = models.ForeignKey(UserTournament, on_delete=models.CASCADE, null=True, blank=True, related_name='won_matches')
    circle = models.PositiveIntegerField()


    def __str__(self):
        return f"{self.tournament}'s {self.circle} circle"
