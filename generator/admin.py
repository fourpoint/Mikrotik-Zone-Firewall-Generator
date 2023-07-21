from django.contrib import admin
from generator.models import *


class FWActionsAdmin(admin.ModelAdmin):
    pass


class ConnStateAdmin(admin.ModelAdmin):
    pass


class IPProtocolAdmin(admin.ModelAdmin):
    pass


class FWInterfaceAdmin(admin.ModelAdmin):
    pass


class FWZoneInline(admin.TabularInline):
    model = FWZoneMap
    fk_name = "to_zone"
    extra = 1


class FWZoneAdmin(admin.ModelAdmin):
    inlines = [FWZoneInline]


class FWNamedRuleInline(admin.TabularInline):
    model = FWRule
    extra = 1


class FWNameRuleAdmin(admin.ModelAdmin):
    inlines = [FWNamedRuleInline]


class FWRuleAdmin(admin.ModelAdmin):
    pass


class FWZoneMapAdmin(admin.ModelAdmin):
    pass


admin.site.register(FWActions, FWActionsAdmin)
admin.site.register(ConnState, ConnStateAdmin)
admin.site.register(IPProtocol, IPProtocolAdmin)
admin.site.register(FWInterface, FWInterfaceAdmin)
admin.site.register(FWZone, FWZoneAdmin)
admin.site.register(FWNameRule, FWNameRuleAdmin)
admin.site.register(FWRule, FWRuleAdmin)
admin.site.register(FWZoneMap, FWZoneMapAdmin)
