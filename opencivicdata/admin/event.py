from django.contrib import admin
from django.template import defaultfilters
from opencivicdata.models import event as models
from opencivicdata.admin.base import (
    LinkAdmin, LinkAdminInline,
    MimetypeLinkAdmin, MimetypeLinkInline,
    RelatedEntityInline)


@admin.register(models.EventLocation)
class EventLocationAdmin(admin.ModelAdmin):
   pass


class EventLinkInline(LinkAdminInline):
    model = models.EventLink


class EventSourceInline(LinkAdminInline):
    model = models.EventSource


class EventParticipantInline(RelatedEntityInline):
    model = models.EventParticipant
    readonly_fields = ('organization', 'person')


@admin.register(models.Event)
class EventAdmin(admin.ModelAdmin):
    readonly_fields = ('jurisdiction', 'location')
    fields = (
        'name', 'jurisdiction', 'location', 'description',
        'classification', 'status',
        ('start_time', 'end_time'),
        ('timezone', 'all_day'),
        )

    def source_link(self, obj):
        source = obj.sources.filter(url__icontains="meetingdetail").get()
        tmpl = u'<a href="{0}" target="_blank">View source</a>'
        return tmpl.format(source.url)
    source_link.short_description = 'View source'
    source_link.allow_tags = True

    list_display = (
        'jurisdiction', 'name', 'start_time', 'source_link')

    inlines = [
        EventLinkInline,
        EventSourceInline,
        EventParticipantInline,
        ]

@admin.register(models.EventMedia)
class EventMediaAdmin(admin.ModelAdmin):
    pass


@admin.register(models.EventMediaLink)
class EventMediaLinkAdmin(admin.ModelAdmin):
    pass


@admin.register(models.EventDocument)
class EventDocumentAdmin(admin.ModelAdmin):
    readonly_fields = ('event',)
    list_display = ('event', 'date', 'note')


@admin.register(models.EventDocumentLink)
class EventDocumentLinkAdmin(MimetypeLinkAdmin):
    readonly_fields = ('document',)


@admin.register(models.EventLink)
class EventLinkAdmin(LinkAdmin):
    readonly_fields = ('event',)
    list_display = ('url', 'note')


@admin.register(models.EventSource)
class EventSourceAdmin(admin.ModelAdmin):
    readonly_fields = ('event',)


@admin.register(models.EventParticipant)
class EventParticipantAdmin(admin.ModelAdmin):
    pass


@admin.register(models.EventAgendaItem)
class EventAgendaItemAdmin(admin.ModelAdmin):
    readonly_fields = ('event',)
    fields = ('event', 'description', 'order', 'subjects', 'notes')

    def get_truncated_description(self, obj):
        return defaultfilters.truncatewords(obj.description, 25)
    get_truncated_description.short_description = 'Description'

    def get_truncated_event_name(self, obj):
        return defaultfilters.truncatewords(obj.event.name, 8)
    get_truncated_event_name.short_description = 'Event Name'

    list_display = ('get_truncated_event_name', 'get_truncated_description')


@admin.register(models.EventRelatedEntity)
class EventRelatedEntityAdmin(admin.ModelAdmin):
    pass


@admin.register(models.EventAgendaMedia)
class EventAgendaMediaAdmin(admin.ModelAdmin):
    pass


@admin.register(models.EventAgendaMediaLink)
class EventAgendaMediaLinkAdmin(admin.ModelAdmin):
    pass

