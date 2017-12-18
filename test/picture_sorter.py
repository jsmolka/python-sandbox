import fileutil as fu

try:
    STDOUT = False
    STDERR = False

    # Define dictionary for year
    year = {
        "01": "Januar",
        "02": "Februar",
        "03": "März",
        "04": "April",
        "05": "Mai",
        "06": "Juni",
        "07": "Juli",
        "08": "August",
        "09": "September",
        "10": "Oktober",
        "11": "November",
        "12": "Dezember"
    }

    # Define regular expressions for different cameras and other stuff
    # Possible media
    RE_MEDIA = r"^.*\.(?:mp4|MP4|png|PNG|jpg|JPG|jpeg|jpeg)$"
    # Current main camera (might change)
    RE_CAMERA_MAIN = r"^([0-9]{8})_([0-9]{6}).*\.jpg$"  # 20130920_215310.jpg
    # Other camera which occurs sometimes
    RE_CAMERA2 = r"^IMG-([0-9]{8})-WA([0-9]{4}).*\.jpg$"  # IMG-20160109-WA0002.jpg
    # WhatsApp pictures (filter AFTER camera!)
    RE_WHATSAPP = r"^.*([0-9]{8})_([0-9]{6}).*\.jpg$"
    # Videos
    RE_VIDEO = r"^.*\.(?:mp4|MP4)$"  # Videos

    # Define used directories
    ROOT = fu.PYDIR
    CAMERA = ROOT + "Camera/"
    TRASH = ROOT + "Müll/"
    VIDEO = ROOT + "Videos/"
    OTHER = ROOT + "Sonstiges/"
    WHATSAPP = ROOT + "WhatsApp/"

    files = fu.files(CAMERA)  # Get all data from camera folder

    if files:
        # Filter trash
        print("Müll löschen...")
        files, trash = fu.regex(files, RE_MEDIA)
        if trash:
            for f in trash:  # Remove trash
                fu.move(f, TRASH, stdout=STDOUT, stderr=STDERR)

        # Filter main camera
        print("Kamera Bilder einordnen...")
        camera_main, files = fu.regex(files, RE_CAMERA_MAIN)
        if camera_main:
            for f in camera_main:
                name = fu.filename(f)
                fu.move(f, ROOT + "{0}/{1}".format(name[:4], year[name[4:6]]), stdout=STDOUT, stderr=STDERR)

        # Filter camera 2
        camera2, files = fu.regex(files, RE_CAMERA2)
        if camera2:
            for f in camera2:
                name = fu.filename(f)
                fu.move(f, ROOT + "{0}/{1}".format(name[4:8], year[name[8:10]]), stdout=STDOUT, stderr=STDERR)

        # Filter videos
        print("Videos verschieben...")
        video, files = fu.regex(files, RE_VIDEO)
        if video:
            for f in video:
                fu.move(f, VIDEO, stdout=STDOUT, stderr=STDERR)

        # Filter WhatsApp
        print("WhatsApp Bilder verschieben...")
        whatsapp, files = fu.regex(files, RE_WHATSAPP)
        if whatsapp:
            for f in whatsapp:
                fu.move(f, WHATSAPP, stdout=STDOUT, stderr=STDERR)

        # Move other
        print("Restliche Bilder verschieben...")
        if files:
            for f in files:
                fu.move(f, OTHER, stdout=STDOUT, stderr=STDERR)

        # Remove dirs
        print("Ordner aufräumen...")
        test = fu.files(CAMERA)
        if test:
            for f in test:
                fu.move(f, TRASH)
        dirs = fu.listdir(CAMERA)
        if dirs:
            for d in dirs:
                fu.remove(CAMERA + d)
    else:
        print("Es gibt nichts zu verschieben...")

except Exception as e:
    print("Es ist ein Fehler aufgetreten!")
    print("Bitte schicke ein Bild mit dem folgenden Fehler an den Verfasser!")
    print("-----------------------------------------------------------------")
    print(str(e))
    print("-----------------------------------------------------------------")
    input("Enter drücken zum beenden oder Fenster schließen!")
