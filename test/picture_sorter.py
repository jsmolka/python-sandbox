import fileutil as fu  # Skript. for hard drive

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
    RE_WHATSAPP = r"^IMG-([0-9]{8})-WA([0-9]{4}).*\.jpg$"  # IMG-20160109-WA0002.jpg / WhatsApp pictures
    # WhatsApp pictures (filter AFTER camera!)
    RE_PROFILE = r"^.*([0-9]{8})_([0-9]{6}).*\.jpg$"
    # Scans
    RE_SCAN = r"^.*Scan.*\.png$"
    # Videos
    RE_VIDEO = r"^.*\.(?:mp4|MP4)$"

    # Define used directories
    ROOT = fu.PYDIR
    CAMERA = ROOT + "Camera/"
    TRASH = ROOT + "Müll/"
    VIDEO = ROOT + "Videos/"
    OTHER = ROOT + "Sonstiges/"
    WHATSAPP = ROOT + "WhatsApp/"
    PROFILE = WHATSAPP + "Profilbilder/"

    SCAN = ROOT + "Scanner/"

    files = fu.files(CAMERA)  # Get all data from camera folder

    if files:
        # Filter trash
        files, trash = fu.regex(files, RE_MEDIA)
        if trash:
            print("Müll löschen")
            for f in trash:  # Remove trash
                fu.move(f, TRASH, stdout=STDOUT, stderr=STDERR)

        # Filter main camera
        camera_main, files = fu.regex(files, RE_CAMERA_MAIN)
        if camera_main:
            print("Kamera Bilder verschieben")
            for f in camera_main:
                name = fu.filename(f)
                fu.move(f, ROOT + "{0}/{1}".format(name[:4], year[name[4:6]]), stdout=STDOUT, stderr=STDERR)

        # Filter WhatsApp pictures
        whatsapp, files = fu.regex(files, RE_WHATSAPP)
        if whatsapp:
            print("WhatsApp Bilder verschieben")
            for f in whatsapp:
                name = fu.filename(f)
                fu.move(f, WHATSAPP + "{0}/{1}".format(name[4:8], year[name[8:10]]), stdout=STDOUT, stderr=STDERR)

        # Filter videos
        video, files = fu.regex(files, RE_VIDEO)
        if video:
            print("Videos verschieben")
            for f in video:
                fu.move(f, VIDEO, stdout=STDOUT, stderr=STDERR)

        # Filter WhatsApp profile pictures
        profile, files = fu.regex(files, RE_PROFILE)
        if profile:
            print("WhatsApp Profil Bilder verschieben")
            for f in profile:
                wa_name = PROFILE + fu.filename(f)[:-20]  # Extract WhatsApp name
                while wa_name[-1] == " ":
                    wa_name = wa_name[:-1]
                fu.move(f, wa_name, stdout=STDOUT, stderr=STDERR)

        # Filter scans
        scans, files = fu.regex(files, RE_SCAN)
        if scans:
            print("Scans verschieben")
            for f in scans:
                fu.move(f, SCAN, stdout=STDOUT, stderr=STDERR)

        # Move other
        if files:
            print("Restliche Bilder verschieben")
            for f in files:
                fu.move(f, OTHER, stdout=STDOUT, stderr=STDERR)

        # Remove dirs
        test = fu.files(CAMERA)
        if test:
            for f in test:
                fu.move(f, TRASH)
        dirs = fu.listdir(CAMERA)
        if dirs:
            print("Ordner aufräumen")
            for d in dirs:
                fu.remove(CAMERA + d)
    else:
        print("Es gibt nichts zu verschieben")

except Exception as e:
    print("Es ist ein Fehler aufgetreten")
    print("-----------------------------------------------------------------")
    print(str(e))
    print("-----------------------------------------------------------------")
    input("Enter drücken zum beenden oder Fenster schließen")
