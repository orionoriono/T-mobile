from django.contrib import messages
from django.shortcuts import render, redirect

from .forms import DeployForm
from .models import Task, Deployment


def deploy_service(request):
    if request.method == "POST":
        form = DeployForm(request.POST)
        if "delete" in request.POST:
            Task.objects.all().delete()
            messages.success(request, "Сите записи се избришани!")
            return redirect("deploy_service")

        if form.is_valid():
            deployment = form.save(commit=False)  # НЕ зачувувај уште

            # АВТОМАТСКО ГЕНЕРИРАЊЕ НА IP ОД "DHCP"
            auto_ip = Deployment.get_next_ip_for_region(deployment.region)
            deployment.reserved_ip = auto_ip

            deployment.save()  # Сега зачувај

            # Генерирај service name
            region_display = dict(Deployment.REGION_CHOICES).get(
                deployment.region, deployment.region
            )
            service_name = f"{deployment.customer_name}_{region_display}{deployment.service_id}"

            # Креирај Task
            task = Task.objects.create(
                customer_name=deployment.customer_name,
                service_id=deployment.service_id,
                service_name=service_name,
                region=deployment.get_region_display_name(),
                manufacturer=dict(Deployment.MANUFACTURER_CHOICES).get(
                    deployment.manufacturer, deployment.manufacturer
                ),
                model_type=dict(Deployment.MODEL_CHOICES).get(
                    deployment.model_type, deployment.model_type
                ),
                serial_number=deployment.serial_number,
                mac_address=getattr(deployment, "mac_address", ""),  # безбедно ако нема поле
                reserved_ip=auto_ip,  # Автоматски генерирана IP
                hostname=service_name,
            )

            # Информативна порака
            parent_info = ""
            if deployment.region in Deployment.REGION_HIERARCHY:
                parent_code = Deployment.REGION_HIERARCHY[deployment.region]
                parent_name = dict(Deployment.REGION_CHOICES).get(parent_code)
                region_name = dict(Deployment.REGION_CHOICES).get(deployment.region)
                parent_info = f" (од DHCP pool на {parent_name})"


            return redirect("deploy_service")
    else:
        form = DeployForm()  # GET request → празна форма

    # Врти го template со form и task preview
    tasks = Task.objects.all().order_by("-id")
    return render(request, "home/deploy.html", {"form": form, "tasks": tasks})
