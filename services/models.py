from django.db import models


class GeneralServiceInfo(models.Model):
    OPERATOR_CHOICES = [
        ("A1 MK", "A1 MK"),
        ("MT", "Makedonski Telekom"),
    ]

    SERVICE_ORIGIN_CHOICES = [
        ("ILL", "ILL"),
        ("MEP", "MEP"),
    ]

    operator = models.CharField(
        max_length=50,
        choices=OPERATOR_CHOICES
    )
    district = models.CharField(max_length=255)
    service_sign = models.CharField(
        max_length=100,
        verbose_name="Service ID"
    )
    service_type = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    speed = models.CharField(max_length=100)
    contract_start_date = models.DateField()
    access_address = models.CharField(max_length=255)
    service_origin = models.CharField(
        max_length=10,
        choices=SERVICE_ORIGIN_CHOICES,
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Service"
        verbose_name_plural = "Services"

    def __str__(self):
        return f"{self.service_sign} - {self.location}"


class MPLSPoP(models.Model):
    general_service = models.ForeignKey(
        GeneralServiceInfo,
        on_delete=models.CASCADE,
        related_name="mpls_pops"
    )
    pop_hostname = models.CharField(max_length=255)
    vsi = models.CharField(max_length=255)
    vsi_id = models.CharField(max_length=255)
    vsi_peers = models.TextField()
    l3_interface = models.CharField(max_length=255)
    vpn_instance = models.CharField(max_length=255)
    transport_ip_address = models.GenericIPAddressField()
    routed_lan_pool = models.CharField(max_length=255)
    service_port = models.CharField(max_length=255)
    remark = models.CharField(max_length=255, blank=True)
    interface_type = models.CharField(max_length=255)
    service_vlan = models.PositiveIntegerField()
    rate_limit = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "MPLS PoP"
        verbose_name_plural = "MPLS PoPs"

    def __str__(self):
        return f"{self.pop_hostname} ({self.general_service.service_sign})"