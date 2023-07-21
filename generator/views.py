from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import HttpResponse

from .models import *


def list_generate():
    list_command = "/interface list\n"
    list_int_command = "/interface list member\n"

    zones = FWZone.objects.filter(local=False)
    for zone in zones:
        zone_name = f"{zone.name}_zone"
        list_command += f"add name={zone_name} comment=\"{zone.description}\"\n"
        # print(zone.interfaces.get())
        for interface in zone.interfaces.all():
            list_int_command += f"add list={zone_name} interface={interface.name}\n"

    return list_command, list_int_command


def jump_generate():
    zone_jumps = ""
    maps = FWZoneMap.objects.exclude(Q(from_zone__local=True) | Q(to_zone__local=True))
    for m in maps:
        zone_jumps += f"add chain=forward action=jump jump-target={m.rule.name} " \
                      f"in-interface-list={m.from_zone.name}_zone out-interface-list={m.to_zone.name}_zone " \
                      f"comment=\"{m.from_zone.name} -> {m.to_zone.name}\"\n"

    zone_jumps += "\n"
    maps = FWZoneMap.objects.filter(to_zone__local=True)
    for m in maps:
        zone_jumps += f"add chain=input action=jump jump-target={m.rule.name} " \
                      f"in-interface-list={m.from_zone.name}_zone " \
                      f"comment=\"{m.from_zone.name} -> router\"\n"

    zone_jumps += "\n"
    maps = FWZoneMap.objects.filter(from_zone__local=True)
    for m in maps:
        zone_jumps += f"add chain=output action=jump jump-target={m.rule.name} " \
                      f"out-interface-list={m.to_zone.name}_zone " \
                      f"comment=\"router -> {m.to_zone.name}\"\n"

    return zone_jumps


def chain_generate():
    chains = ""
    rules = FWRule.objects.order_by('rule__name', 'rule_number')
    for rule in rules:
     pass
    print(rules)
    return chains


def generate(request):
    list_com, list_int = list_generate()
    jumps = jump_generate()
    chains = chain_generate()
    out = f"{list_com}\n\n{list_int}\n\n/ip firewall filter\n{jumps}"
    return HttpResponse(out, content_type="text/plain")
