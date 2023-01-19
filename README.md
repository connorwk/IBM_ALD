# IBM_ALD
IBM Automation Logic Design viewer and editor

## ibm_ald_decode.py
Requires Tkinter, PIL (Pillow)
You can enter a Circuit ID from an ALD block and it will provide the Class, Type, and Description along with a photo of the SLT Module if there is one associated with the Circuit ID.
This list will be ever growing as associations are made and added along with Module schematics photos added.
Uses `ibm_circuit_info.json` and the `photos/` directory.

## ibm_ald.py
Experiment into digitizing IBM ALDs into a json file format and re-rendering them from this json file.
This is far from a complete project and more of an experiment to see if it was worth the time and effort for my reverse engineering of the 1130 ALDs. I decided that at this time it is not worth the effort and currently its at the point of needing a trace routing algorithm implemented.
The `ibm_1130_ald.json` is an example of the format it takes in.
If someone wants to work on this please let me know and I will support you any way I can but I don't have the time to work this project at the moment.
