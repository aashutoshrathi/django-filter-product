import decimal
import uuid

from django.core.validators import MinValueValidator
from django.db import models


class Bands(models.Model):
    class Meta:
        ordering = ('id',)
        verbose_name = 'Band'
        verbose_name_plural = 'Bands'

    id = models.CharField(unique=True, default=uuid.uuid4,
                          editable=False, max_length=50, primary_key=True)
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class OS(models.Model):
    class Meta:
        ordering = ('id',)
        verbose_name = 'Operating System'
        verbose_name_plural = 'Operating Systems'

    id = models.CharField(unique=True, default=uuid.uuid4,
                          editable=False, max_length=50, primary_key=True)
    name = models.CharField(max_length=10)
    version = models.CharField(max_length=10)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name + " " + self.version

    def for_fa(self):
        return self.name.lower()


class Brand(models.Model):
    class Meta:
        ordering = ('id',)
        verbose_name = 'Brand'
        verbose_name_plural = 'Brands'

    id = models.CharField(unique=True, default=uuid.uuid4,
                          editable=False, max_length=50, primary_key=True)
    name = models.CharField(max_length=20)
    origin_country = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Mobile(models.Model):
    class Meta:
        ordering = ('id',)
        verbose_name = 'Mobile'
        verbose_name_plural = 'Mobiles'

    id = models.CharField(unique=True, default=uuid.uuid4,
                          editable=False, max_length=50, primary_key=True)
    brand = models.ForeignKey(Brand, related_name='brand', on_delete=models.CASCADE)
    model = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    os = models.ForeignKey(OS, related_name='operating_system', on_delete=models.CASCADE)
    price = models.FloatField(default=0.0, validators=[MinValueValidator(0.0)])
    band = models.ManyToManyField(Bands, related_name='band')
    proccessor_speed = models.FloatField(default=0.0, validators=[MinValueValidator(0.0)])

    def __str__(self):
        return str(self.brand) + " " + self.name

    def to_India(self):
        n = self.price
        d = decimal.Decimal(str(n))
        if d.as_tuple().exponent < -2:
            s = str(n)
        else:
            s = '{0:.2f}'.format(n)
        l = len(s)
        i = l - 1;
        res = ''
        flag = 0
        k = 0
        while i >= 0:
            if flag == 0:
                res = res + s[i]
                if s[i] == '.':
                    flag = 1
            elif flag == 1:
                k = k + 1
                res = res + s[i]
                if k == 3 and i - 1 >= 0:
                    res = res + ','
                    flag = 2
                    k = 0
            else:
                k = k + 1
                res = res + s[i]
                if k == 2 and i - 1 >= 0:
                    res = res + ','
                    flag = 2
                    k = 0
            i = i - 1

        return res[::-1]

    def for_fa(self):
        return self.os.for_fa()

    def give_me_bands(self):
        bands = ""
        for band in self.band.all():
            bands += band.name + " "
        return bands
