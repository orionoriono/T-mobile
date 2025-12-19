from django.db import models
from django.db.models import Max

class Deployment(models.Model):
    # Choices за региони
    REGION_CHOICES = [
        ('', 'Select Region'),
        ('sk', 'Skopje'),
        ('oh', 'Ohrid'),
        ('su', 'Struga'),
        ('bt', 'Bitola'),
        ('st', 'Strumica'),
        ('be', 'Berovo'),
        ('ko', 'Kochani'),
        ('ge', 'Gevgelija'),
        ('st_sh', 'Shtip'),
        ('pe', 'Pehchevo'),
        ('vi', 'Vinica'),
        ('va', 'Valandovo'),
        ('do', 'Dojran'),
    ]

    # Мапа на детски региони кон родителите
    REGION_HIERARCHY = {
        'pe': 'be',
        'vi': 'ko',
        'va': 'st',
        'do': 'ge',
    }

    # Choices за производители
    MANUFACTURER_CHOICES = [
        ('', 'Select Manufacturer'),
        ('cisco', 'Cisco'),
        ('huawei', 'Huawei'),
    ]

    # Choices за модели
    MODEL_CHOICES = [
        ('', 'Select Model'),
        ('m1', 'Model 1'),
        ('m2', 'Model 2'),
    ]

    # DHCP pool за главни региони
    DHCP_POOLS = {
        'sk': {'start': '10.56.117.10', 'end': '10.56.117.50'},
        'oh': {'start': '10.56.118.10', 'end': '10.56.118.50'},
        'su': {'start': '10.56.119.10', 'end': '10.56.119.50'},
        'bt': {'start': '10.56.120.10', 'end': '10.56.120.50'},
        'st': {'start': '10.56.121.10', 'end': '10.56.121.50'},
        'be': {'start': '10.56.122.10', 'end': '10.56.122.50'},
        'ko': {'start': '10.56.123.10', 'end': '10.56.123.50'},
        'ge': {'start': '10.56.124.10', 'end': '10.56.124.50'},
        'st_sh': {'start': '10.56.125.10', 'end': '10.56.125.50'},
    }

    customer_name = models.CharField(max_length=100, blank=True, null=True)
    service_id = models.CharField(max_length=100, blank=True, null=True)
    region = models.CharField(max_length=50, choices=REGION_CHOICES)
    manufacturer = models.CharField(max_length=20, choices=MANUFACTURER_CHOICES)
    model_type = models.CharField(max_length=20, choices=MODEL_CHOICES)
    serial_number = models.CharField(max_length=50, blank=True, null=True)
    reserved_ip = models.GenericIPAddressField(blank=True, null=True)  # Автоматски IP

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.customer_name} - {self.service_id}"

    # Метод за да го користи views.py
    def get_region_display_name(self):
        return dict(self.REGION_CHOICES).get(self.region, self.region)

    @classmethod
    def get_next_ip_for_region(cls, region_code):
        if region_code in cls.REGION_HIERARCHY:
            region_code = cls.REGION_HIERARCHY[region_code]

        pool = cls.DHCP_POOLS.get(region_code)
        if not pool:
            return '10.56.117.100'  # Default IP

        last_deployment = cls.objects.filter(region=region_code).aggregate(Max('reserved_ip'))
        last_ip = last_deployment['reserved_ip__max']
        if not last_ip:
            return pool['start']

        ip_parts = last_ip.split('.')
        last_octet = int(ip_parts[3])
        pool_end_octet = int(pool['end'].split('.')[3])

        if last_octet < pool_end_octet:
            ip_parts[3] = str(last_octet + 1)
            return '.'.join(ip_parts)
        else:
            return pool['start']


class Task(models.Model):
    customer_name = models.CharField(max_length=255, blank=True, null=True)
    service_id = models.CharField(max_length=255, blank=True, null=True)
    service_name = models.CharField(max_length=255, blank=True, null=True)
    region = models.CharField(max_length=50)
    manufacturer = models.CharField(max_length=50)
    model_type = models.CharField(max_length=50)
    serial_number = models.CharField(max_length=255, blank=True, null=True)
    mac_address = models.CharField(max_length=50, blank=True, null=True)
    reserved_ip = models.GenericIPAddressField(blank=True, null=True)
    hostname = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Task {self.id} - {self.customer_name}"
