from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse

from .models import GeneralServiceInfo, MPLSPoP


def services_dashboard(request):
    """
    Services table with filtering and pagination.
    """
    services_qs = GeneralServiceInfo.objects.all()

    # Distinct operators and locations for filter dropdowns
    operators = (
        GeneralServiceInfo.objects.order_by("operator")
        .values_list("operator", flat=True)
        .distinct()
    )
    locations = (
        GeneralServiceInfo.objects.order_by("location")
        .values_list("location", flat=True)
        .distinct()
    )

    # Apply filters from query params
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


def pop_detail_api(request, service_id):
    """
    API endpoint returning PoP details for a given service.
    URL: /services/api/pop-detail/<service_id>/
    Response contains two server room objects.
    """
    try:
        pop = MPLSPoP.objects.filter(general_service_id=service_id).first()

        if not pop:
            return JsonResponse(
                {"error": "No PoP found for this service."},
                status=404,
            )

        data = {
            "service_id": pop.general_service_id,
            "oznaka": pop.general_service.service_sign,
            "server_room_1": {
                "field_value": pop.srv1_field_value,
                "prostorija": pop.srv1_room,
                "rack": pop.srv1_rack,
                "odf": pop.srv1_odf,
                "pozicija": pop.srv1_position,
                "end_customer_eq_info": pop.srv1_cust_eq_info,
                "end_customer_int_info": pop.srv1_cust_int_info,
            },
            "server_room_2": {
                "field_value": pop.srv2_field_value,
                "prostorija": pop.srv2_room,
                "rack": pop.srv2_rack,
                "odf": pop.srv2_odf,
                "pozicija": pop.srv2_position,
                "end_customer_eq_info": pop.srv2_cust_eq_info,
                "end_customer_int_info": pop.srv2_cust_int_info,
            },
        }

        return JsonResponse(data)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def pop_info(request, service_id):
    """
    Backwards-compatible alias for the original PoP endpoint.
    Delegates to pop_detail_api to keep a single response shape.
    """
    return pop_detail_api(request, service_id)