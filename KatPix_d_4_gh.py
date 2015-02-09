import praw, urllib, os
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from datetime import date

print "Starting KatPix..."
subreddit = "cats"
directory = "Attachments\Cats\Daily"

path = os.path.join(os.getcwd(), directory)
if not os.path.exists(path):
	os.makedirs(path)
r = praw.Reddit(user_agent="KatPix3.n /u/*******")
username = "KatPix4Errbody"
password = "****************"
today = date.today()
day = str(today.month) + "/" + str(today.day)

#Generate Recipient List
f = open("List_KatPix_d.txt", "r")
list = f.read()
address_list = list.split("\n")
while '' in address_list:
	address_list.remove('')
while ' ' in address_list:
	address_list.remove(' ')
f.close()

#Compiling Messagae
text = "Your cat picture is here! Yay!"
text += "\n\nThis is an automated service designed to send pictures of cats on a regular basis.\n"
text += "This bot attaches today's top post from http://www.reddit.com/r/cats (hosted by imgur) to ensure quality content.\n\n"
text += "The email address associated with this service forwards to the creator's personal address. You can therefore contact the creator simply by responding to this email.\n"
text += "Thus, if you want to recieve KatPix more frequently, you need only ask in reply to this message. "
text += "If, for some reason, you have subscribed to another service or are getting KatPix for yourself, you can request to recieve these emails less frequently instead. "
text += "If you wish to change the email address to which these are sent, you can unsubscribe (and then resubscribe with a different address of course).\n\n"
text += "If you have any complaints in general, please feel free to voice them. Your satisfaction is our top priority.\n\n"
text += "Sincerely,\nThe KatPix Team"
text += "\n\n\nBug Fixes:\n"
text += "10/21: Per request of namesake, email address was formalized;\n"
text += "12/29: Reliability issues addressed;\n"
text += "01/18: Email address changed;\n"
text += "02/26: Email domain changed;\n"
text += "05/19: Weekly alternative introduced;\n"
text += "08/02: Reddit API incorporated;\n"
subject = "Cat Pic for " + day

msg = MIMEMultipart()
msg["Subject"] = subject
msg["From"] = username + "@yahoo.com"
msg["To"] = "Errbody"

print "Retrieving Image..."
posts = r.get_subreddit(subreddit).get_top_from_day(limit=15)
for post in posts:
	if "imgur.com/" in post.url and "/a/" not in post.url:
		if "i.imgur.com" in post.url:
			url = post.url
			break
		else:
			url = "http://i." + post.url[7:] + ".jpg" #not png? Every other image seems to be jpg
			break

print "\t", url
img_id = url[19:30]
img_id = os.path.join(path, img_id)
for i in range(10):
	try:
		urllib.urlretrieve(url, img_id)
	except:
		print "Encountered error retrieving image... retrying", 9 - i, "more times..."
		pass
	else:
		print " Succeeded"
		break

print "Attaching Image..."
f = open(img_id, 'rb')
image = MIMEImage(f.read(), _subtype="png")
f.close()
msg.attach(image)
msgText = MIMEText(text)
msg.attach(msgText)

print "Sending Message..."
for i in range(10):
	try:
		server = smtplib.SMTP("smtp.mail.yahoo.com:587")
		server.starttls()
		server.login(username, password)
	except:
		print "Encountered error sending email... retrying", 9 - i, "more times..."
		pass
	else:
		print " Succeeded"
		break
print "Sending to:"
for address in address_list:
	print "\t" + address
server.sendmail(username + "@yahoo.com", address_list, msg.as_string())
server.quit()

print "Message Sent!"
