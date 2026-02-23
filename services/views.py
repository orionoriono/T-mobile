

from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse

from .models import GeneralCCInfo, ServerRoomDetails


def services_dashboard(request):
    services_qs = GeneralCCInfo.objects.all()

    operators = (
        GeneralCCInfo.objects.order_by("operator")
        .values_list("operator", flat=True)
        .distinct()
    )

    locations = (
        GeneralCCInfo.objects.order_by("location")
        .values_list("location", flat=True)
        .distinct()
    )

    operator = request.GET.get("operator")
    if operator and operator != "All":
        services_qs = services_qs.filter(operator=operator)

    location = request.GET.get("location")
    if location and location != "All":
        services_qs = services_qs.filter(location=location)

    keyword = request.GET.get("keyword")
    if keyword:
        services_qs = services_qs.filter(
            Q(service_sign__icontains=keyword)
            | Q(service_type__icontains=keyword)
            | Q(location__icontains=keyword)
            | Q(operator__icontains=keyword)
        )

    paginator = Paginator(services_qs, 20)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "services/services.html",
        {
            "page_obj": page_obj,
            "operators": operators,
            "locations": locations,
        },
    )


def details_detail_api(request, service_id):
    details = ServerRoomDetails.objects.filter(general_service_id=service_id).first()

    if not details:
        return JsonResponse({"error": "No Details found for this service."})

    data = {
        "server_room_1": {
            "prostorija": details.srv1_room,
            "rack": details.srv1_rack,
            "odf": details.srv1_odf,
            "pozicija": details.srv1_position,
            "end_customer_eq_info": details.srv1_cust_eq_info,
            "end_customer_int_info": details.srv1_cust_int_info,
        },
        "server_room_2": {
            "prostorija": details.srv2_room,
            "rack": details.srv2_rack,
            "odf": details.srv2_odf,
            "pozicija": details.srv2_position,
            "end_customer_eq_info": details.srv2_cust_eq_info,
            "end_customer_int_info": details.srv2_cust_int_info,
        },
    }

    return JsonResponse(data)