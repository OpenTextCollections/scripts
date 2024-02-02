import lingtypology
from datetime import datetime
import csv
from PIL import Image

def crop(image_path, coords, saved_location):
    image_obj = Image.open(image_path)
    cropped_image = image_obj.crop(coords)
    cropped_image.save(saved_location)
    cropped_image.show()


if __name__ == '__main__':
    location_glottocodes = []
    with open('collections_overview.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            location_glottocode = row['Location Glottocode']
            glottocode = row['Glottocode']
            if location_glottocode and location_glottocode.strip() != '':
                location_glottocodes.append(location_glottocode)
            else:
                location_glottocodes.append(glottocode)

    m = lingtypology.LingMap(location_glottocodes, glottocode=True)
    m.tiles = "openstreetmap"
    m.create_map()
    today = datetime.now().strftime("%Y-%m-%d")
    fname = f"otclgs{today}.png"
    print(f"saving to {fname}")
    m.save_static(fname=fname)
    image = fname
    crop(image, (200, 20, 1230, 600), 'otclgs.png')

