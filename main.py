from helpers import configs, get_torrents, send_email

all_torrents = {}
for cat in configs['torrents']['categories']:
    all_torrents[cat] = []
    for page in range(1, (int(configs['torrents']['pages']) + 1)):
        torrents = get_torrents(cat, page)
        if len(torrents) > 0:
            all_torrents[cat].extend(torrents)

if all_torrents:
    send_email({'torrents': all_torrents})
    print("Email sent")
else:
    print("No new torrents found!")


