import glob
import os

from mediaconch import *
from pymediainfo import MediaInfo
from pprint import pprint

MC = MediaConch()

# Add policy
MC.add_policy("./ArchivematicaPolicies/Audio-AMI-WAV.xml")

# Set display format (optional, default to xml)
MC.set_format(Format.text)

for filename in glob.iglob('./validationFiles/**', recursive=True):
    # filter dirs
    if os.path.isfile(filename):
        # look for WAV files
        if filename.endswith(".wav"):
            # What about DAT files? How do we know if it was a DAT?
            media_info = MediaInfo.parse(filename)

            #print(type(media_info))
            for trackobj in media_info.tracks:
                #print(type(trackobj))
                track = trackobj.to_data()
                if track["track_type"] == "General":
                    if trackobj.encoding_settings:
                        if "DAT" in trackobj.encoding_settings:
                            #print(track["encoding_settings"])
                            print(filename + " is a DAT file!")
                            # insert MC policy info here

                        else:
                            print(filename + " is not a DAT file!")
                            file_id = MC.add_file(filename)
                            # Display report
                            # print(MC.get_report(file_id))
                            report = MC.get_report(file_id)
                            # print(type(report))
                            if "Outcome: fail" in report:
                                print("Fail " + filename)
                                with open(filename + "-FailReport.txt", "w") as text_file:
                                    text_file.write(report)
                                # save report with WAV filename?
                            else:
                                print("Pass")
                    else:
                        print("No encoding info available")









