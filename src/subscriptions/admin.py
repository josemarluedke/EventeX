# -*- coding: utf-8 -*-
import datetime
from django.contrib import admin
from subscriptions.models import Subscription
from django.utils.translation import ugettext as _
from django.utils.translation import ungettext
from django.conf.urls.defaults import patterns, url
from django.http import HttpResponse

class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'created_at', 'subscribed_today', 'paid')
    date_hierarchy = 'created_at'
    search_fields = ('name', 'cpf', 'email', 'phone', 'created_at')
    list_filter = ('paid',)

    actions = ['mark_as_paid']

    def mark_as_paid(self, request, queryset):
        count = queryset.update(paid=True)
        msg = ungettext(
            u"%(count)d inscrição foi marcada como paga.",
            u"%(count) inscrições foram marcadas como pagas.",
            count
        ) %  {'count': count}
        self.message_user(request, msg)
    mark_as_paid.short_description = _(u"Marcar como pagas")

    def subscribed_today(self, obj):
        return obj.created_at.date() == datetime.date.today()

    subscribed_today.short_description = u'Inscrito hoje?'
    subscribed_today.boolean = True

    def export_subscriptions(self, request):
        subscriptions = self.model.objects.all()
        rows = [",".join([s.name, s.email]) for s in subscriptions]

        response = HttpResponse('\r\n'.join(rows))
        response.mimetype = "text/csv"
        response['Content-Disposition'] = 'attachment; filename=inscricoes.csv'

        return response
    
    def get_urls(self):
        original_urls = super(SubscriptionAdmin, self).get_urls()
        extra_urls = patterns('',
            url(r'exportar-inscricoes/$',
            self.admin_site.admin_view(self.export_subscriptions), name='export_subscriptions'))

        return extra_urls + original_urls

admin.site.register(Subscription, SubscriptionAdmin)