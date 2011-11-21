# -*- coding: utf-8 -*-
from django.db import models

class Subscription(models.Model):
    name = models.CharField("Nome", max_length=100)
    cpf = models.CharField("CPF", max_length=11, unique=True)
    email = models.EmailField("E-mail", unique=True)
    phone = models.CharField("Telefone", max_length=20, blank=True)
    created_at = models.DateTimeField("Criado em", auto_now_add=True)

    def __unicode__(self): 
        return self.name

    class Meta:
        ordering = ["created_at"]
        verbose_name = u"Inscrição"
        verbose_name_plural = u"Inscrições"