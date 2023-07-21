from django.db import models


class FWActions(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Firewall Action"
        verbose_name_plural = "Firewall Actions"


class ConnState(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Connection State"
        verbose_name_plural = "Connection States"


class IPProtocol(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "IP Protocol"
        verbose_name_plural = "IP Protocols"


class FWInterface(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Firewall Interface"
        verbose_name_plural = "Firewall Interfaces"


class FWZone(models.Model):
    name = models.CharField(max_length=100)
    local = models.BooleanField(default=False)
    interfaces = models.ManyToManyField(FWInterface, blank=True)
    description = models.TextField(null=True, blank=True)
    zone_map = models.ManyToManyField(
        "self",
        through='FWZoneMap',
        through_fields=("to_zone", "from_zone"),
        symmetrical=False,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Firewall Zone"
        verbose_name_plural = "Firewall Zones"


class FWNameRule(models.Model):
    name = models.CharField(max_length=100)
    default_action = models.ForeignKey(FWActions, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Firewall Named Rule"
        verbose_name_plural = "Firewall Named Rules"


class FWRule(models.Model):
    rule = models.ForeignKey(FWNameRule, on_delete=models.CASCADE)
    rule_number = models.IntegerField()
    action = models.ForeignKey(FWActions, on_delete=models.CASCADE)
    conn_status = models.ManyToManyField(ConnState, blank=True)
    src_addr = models.GenericIPAddressField(null=True, blank=True)
    dst_addr = models.GenericIPAddressField(null=True, blank=True)
    protocol = models.ForeignKey(IPProtocol, on_delete=models.CASCADE, null=True, blank=True)
    src_port = models.IntegerField(null=True, blank=True)
    dst_port = models.IntegerField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.rule} {self.rule_number} action {self.action}"

    class Meta:
        verbose_name = "Firewall Rule"
        verbose_name_plural = "Firewall Rules"


class FWZoneMap(models.Model):
    to_zone = models.ForeignKey(FWZone, on_delete=models.CASCADE, related_name="dst_zone")
    from_zone = models.ForeignKey(FWZone, on_delete=models.CASCADE, related_name="src_zone")
    rule = models.ForeignKey(FWNameRule, on_delete=models.CASCADE)

    def __str__(self):
        return f"From {self.from_zone} to {self.to_zone} firewall name {self.rule}"

    class Meta:
        verbose_name = "Firewall From Zone Mapping"
        verbose_name_plural = "Firewall From Zone Mappings"

