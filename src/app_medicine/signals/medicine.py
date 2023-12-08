from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from app_medicine.models import MedicineModel
from app_medicine.api.user.serializers.medicine import UserDetailMedicineSerializer

from utils.classes import Redis, RedisKeys


@receiver(post_save, sender=MedicineModel)
@receiver(post_delete, sender=MedicineModel)
def set_all_medicine_in_redis_cache_handler(sender, instance, **kwargs):
    redis_cache_service = Redis("medicine", RedisKeys.list_all_data)
    all_medicine = MedicineModel.objects.all().order_by("title")
    serializer_medicine_data = UserDetailMedicineSerializer(
        all_medicine, many=True
    ).data
    redis_cache_service.set_json_value(serializer_medicine_data)
