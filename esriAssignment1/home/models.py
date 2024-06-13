from django.db import models
from django.utils.translation import gettext as _

# Create your models here.
class seismicdataforexam(models.Model):
    block = models.CharField(_("BLOCK"), max_length=255)
    usi_code = models.CharField(_("USI_CODE"), max_length=255)
    region = models.CharField(_("REGION"), max_length=255)
    length_km = models.FloatField(_("LENGTH_KM"))
    acquisition_year = models.IntegerField(_("ACQUISITION_YEAR"))
    processing_year = models.IntegerField(_("PROCESSING_YEAR"))

    # def __str__(self):
    #     return self.name