from django.core.management.base import BaseCommand

from app_medicine.models import MedicineModel

import csv
import codecs


class Command(BaseCommand):
    help = "Initiate DB with our default medicines"

    def handle(self, *args, **options):
        medicines_path = "Medicines.csv"
        with open(medicines_path, "rb") as medicines_file:
            reader_medicines = csv.reader(codecs.iterdecode(medicines_file, "utf-8"))
            header_medicines = next(reader_medicines)
            bulk_medicines = []
            for index, row in enumerate(reader_medicines):
                _object_dict = {key: value for key, value in zip(header_medicines, row)}
                brand_code = f"{'0' * (5 - len(str(_object_dict['brand_code'])))}{_object_dict['brand_code']}"
                price_list = _object_dict["price_exchange_subsidy"].split("\n")

                def mapping_price_list(number):
                    try:
                        split_var = number.split()[0]
                        if split_var == "":
                            return 0
                        else:
                            split_var = split_var.split(",")
                            return int("".join(split_var))
                    except IndexError:
                        return 0

                price_list = list(map(mapping_price_list, price_list))
                sorted_price_list = sorted(price_list, key=lambda x: x, reverse=True)
                percent_list = _object_dict[
                    "percent_share_of_organization_exchange_subsidy"
                ].split("\n")

                def mapping_percent_list(number):
                    try:
                        split_var = number.split()[0]
                        if split_var == "":
                            return 0
                        else:
                            float_var = float(split_var.split("%")[0])
                            if float_var > 100:
                                return 100
                            return float_var
                    except IndexError:
                        return 0

                percent_list = list(map(mapping_percent_list, percent_list))
                sorted_percent_list = sorted(
                    percent_list, key=lambda x: x, reverse=True
                )
                bulk_medicines.append(
                    MedicineModel(
                        brand_code=brand_code,
                        title=_object_dict["title"],
                        term=_object_dict["term"],
                        shape=_object_dict["shape"],
                        dose=_object_dict["dose"],
                        price_exchange_subsidy=sorted_price_list[0],
                        percent_share_of_organization_exchange_subsidy=sorted_percent_list[
                            0
                        ],
                    )
                )
                print(index)
                print(f"append {brand_code} to bulk create list")
            MedicineModel.objects.bulk_create(bulk_medicines)
            print("finished, enjoy")
