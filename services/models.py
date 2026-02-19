from django.db import models


class GeneralServiceInfo(models.Model):
    SERVICE_ORIGIN_CHOICES = [
        ("ILL", "ILL"),
        ("MEP", "MEP"),
    ]

    operator = models.CharField(max_length=50, blank=True, null=True)
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
        'GeneralServiceInfo',
        on_delete=models.CASCADE,
        related_name='pop_entries'
    )

    # Server Room 1
    srv1_field_value   = models.CharField(max_length=255, blank=True, null=True)
    srv1_room          = models.CharField(max_length=255, blank=True, null=True)
    srv1_rack          = models.CharField(max_length=255, blank=True, null=True)
    srv1_odf           = models.CharField(max_length=255, blank=True, null=True)
    srv1_position      = models.CharField(max_length=255, blank=True, null=True)
    srv1_cust_eq_info  = models.CharField(max_length=255, blank=True, null=True)
    srv1_cust_int_info = models.CharField(max_length=255, blank=True, null=True)

    # Server Room 2
    srv2_field_value   = models.CharField(max_length=255, blank=True, null=True)
    srv2_room          = models.CharField(max_length=255, blank=True, null=True)
    srv2_rack          = models.CharField(max_length=255, blank=True, null=True)
    srv2_odf           = models.CharField(max_length=255, blank=True, null=True)
    srv2_position      = models.CharField(max_length=255, blank=True, null=True)
    srv2_cust_eq_info  = models.CharField(max_length=255, blank=True, null=True)
    srv2_cust_int_info = models.CharField(max_length=255, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"PoP for {self.general_service.service_sign}"
    class Meta:
        verbose_name = "MPLS PoP"
        verbose_name_plural = "MPLS PoPs"

    def __str__(self):
        return f"{self.pop_hostname} ({self.general_service.service_sign})"