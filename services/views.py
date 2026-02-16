from django.shortcuts import render
from .models import GeneralServiceInfo, MPLSPoP
from django.core.paginator import Paginator

from django.shortcuts import render
from .models import GeneralServiceInfo
from django.core.paginator import Paginator

def services_dashboard(request):

    services = GeneralServiceInfo.objects.all()

    paginator = Paginator(services, 20)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "services/services.html", {
        "page_obj": page_obj
    })

from django.http import JsonResponse
from .models import GeneralServiceInfo

def pop_info(request, service_id):
    try:
        pop = MPLSPoP.objects.filter(general_service_id=service_id).first()

        if not pop:
            return JsonResponse({"error": "No PoP found"})

        data = {
            "hostname": pop.pop_hostname,
            "vsi": pop.vsi,
            "vsi_id": pop.vsi_id,
            "vsi_peers": pop.vsi_peers,
            "l3_interface": pop.l3_interface,
            "vpn_instance": pop.vpn_instance,
            "transport_ip": pop.transport_ip_address,
            "routed_lan_pool": pop.routed_lan_pool,
            "service_port": pop.service_port,
            "remark": pop.remark,
            "interface_type": pop.interface_type,
            "service_vlan": pop.service_vlan,
            "rate_limit": pop.rate_limit,
            "service": pop.general_service.service_sign,
        }

        return JsonResponse(data)

    except Exception as e:
        return JsonResponse({"error": str(e)})