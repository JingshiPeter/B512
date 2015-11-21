import subprocess
subprocess.call("git add .",shell=True)
subprocess.call("git commit . -m \"automatic commit from python\" ",shell=True)
subprocess.call("git push heroku master",shell=True)
print "end"
