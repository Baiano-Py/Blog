from django.core.management.base import BaseCommand
from blog.models import Follow, Profile

class Command(BaseCommand):
    help = 'Reseta todos os follows e seguidores'

    def handle(self, *args, **kwargs):
        # Remove todos os objetos Follow
        Follow.objects.all().delete()
        
        # Reseta os contadores de followers
        profiles = Profile.objects.all()
        for profile in profiles:
            profile.followers_count = 0
            profile.save()

        self.stdout.write(self.style.SUCCESS('Todos os follows foram resetados com sucesso.'))