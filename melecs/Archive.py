from pathlib import Path
from zipfile import ZipFile
from django.core import serializers
from django.core.files import File
import os
from user_side.models import measurement_list,measured_place,measurement_data, user, all_measurement, Archive
import shutil

def Archivation(arlib, arname, datas):
    arname=str(arname)+".zip"
    BASE_DIR=Path(__file__).resolve().parent/"archive"/arlib
    if type(datas) != list:
        datas=list(datas)
    print(str(BASE_DIR/arname))
    
    # make the directory systems
    directory = ""
    for i in str(BASE_DIR/"temp").split("/"):
        directory += i
        if not os.path.exists(directory):
            os.makedirs(directory)
    
    
    with ZipFile(str(BASE_DIR/arname), "w") as zip_object:
        for data in datas:
            dtxml_name = ""
            match data:
                case 1:
                    dtxml_name="all_measurement.xml"
                    f_name = open(BASE_DIR/"temp"/dtxml_name, "w")
                    new_file= File(f_name)
                    new_file.write(serializers.serialize("xml", all_measurement.objects.all()))
                    new_file.close()
                case 2:
                    dtxml_name="measurement_list.xml"
                    f_name = open(BASE_DIR/"temp"/dtxml_name, "w")
                    new_file= File(f_name)
                    new_file.write(serializers.serialize("xml", measurement_list.objects.all()))
                    new_file.close()
                case 3:
                    dtxml_name="measurement_data.xml"
                    f_name = open(BASE_DIR/"temp"/dtxml_name, "w")
                    new_file= File(f_name)
                    new_file.write(serializers.serialize("xml", measurement_data.objects.all()))
                    new_file.close()
                case 4:
                    dtxml_name="measured_place.xml"
                    f_name = open(BASE_DIR/"temp"/dtxml_name, "w")
                    new_file= File(f_name)
                    new_file.write(serializers.serialize("xml", measured_place.objects.all()))
                    new_file.close()
                case 5:
                    dtxml_name="user.xml"
                    f_name = open(BASE_DIR/"temp"/dtxml_name, "w")
                    new_file= File(f_name)
                    new_file.write(serializers.serialize("xml", user.objects.all()))
                    new_file.close()
            zip_object.write(BASE_DIR/"temp"/dtxml_name,os.path.basename(BASE_DIR/"temp"/dtxml_name))
            
        new_archive = Archive()
        new_archive.Name = arname
        new_archive.File_Location = arlib + "/" + arname
        # new_archive.File = os.path.basename(Path(BASE_DIR/arname))
        new_archive.type = arlib
        new_archive.save()
    shutil.rmtree(BASE_DIR/"temp")
    print("archive is finished")