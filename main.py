import difference_detection
from gdrive import gdrive

def main():
    res = gdrive.get_latest_file()
    if not res:
        return
    difference_detection.main_proccess('img/target.MOV')
    out_path = difference_detection.select_carefully('result')
    gdrive.upload_imgs(out_path)

if __name__ == "__main__":
    main()