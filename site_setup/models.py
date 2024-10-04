from django.db import models
from utils.model_validator import validator_png

class MenuLink(models.Model):
    class meta:
        verbose_name = 'Menu link'
        verbose_name_plural = 'Menu links'

    text = models.CharField(max_length=50)
    url_or_path = models.CharField(max_length=2048)
    new_tab = models.BooleanField(default=False)
    site_setup = models.ForeignKey('SiteSetup', on_delete=models.CASCADE, blank=True, null=True, default=None)

    def __str__(self) -> str:
        return self.text
    

class SiteSetup(models.Model):
    class meta:
        verbose_name = 'Setup'
        verbose_name_plural = 'setups'

    title = models.CharField(max_length=65)
    description = models.CharField(max_length=250)

    show_search = models.BooleanField(default=True)
    show_header = models.BooleanField(default=True)
    show_menu = models.BooleanField(default=True)
    show_pagination = models.BooleanField(default=True)
    show_footer = models.BooleanField(default=True)

    favicon = models.ImageField(
        upload_to= 'assets/favicon/%Y/%m/',
        blank=True, default='',
        validators=[validator_png],
    )

    def __str__(self) -> str:
        return self.title

