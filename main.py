import difference_detection
from gdrive import gdrive

res = gdrive.get_latest_file()
difference_detection.main_proccess('img/target.MOV')
out_path = difference_detection.select_carefully('result')
gdrive.upload_imgs(out_path)