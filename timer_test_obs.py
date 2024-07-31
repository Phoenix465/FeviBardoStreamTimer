import time

with open("timer_test.txt", "w") as f:
  for i in range(60):
    time.sleep(1)
    f.seek(0)
    f.write(f"{i}")
    f.truncate()

'''
  7 feature buttons with picture css and conversion
  submit button pressed > take quantity entered and convert it to seconds then add entry to ledger and update output too
  undo button > delete most recent entry in ledger
  output > one line text file hooked into obs
'''