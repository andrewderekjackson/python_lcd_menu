import msvcrt

# Now mainloop runs "forever"
while True:
    ky = msvcrt.getch()
    length = len(ky)
    if length != 0:
        # send events to event handling functions
        if ky == " ":
            raise SystemExit
        else:
            if key == '\x00' or key == '\xe0':
                key = msvcrt.getch()
            print ord(key),