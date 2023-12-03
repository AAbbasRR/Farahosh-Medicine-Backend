from django.apps import AppConfig


class AppMedicineConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "app_medicine"

    def ready(self):
        import app_medicine.signals.medicine
