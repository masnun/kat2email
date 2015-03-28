from helpers import configs, get_torrents, send_email

all_torrents = {}
for type_ in configs['torrents']['types']:
    all_torrents[type_] = []
    for page in range(1, (int(configs['torrents']['pages']) + 1)):
        torrents = get_torrents(type_, page)
        if len(torrents) > 0:
            all_torrents[type_].extend(torrents)

if all_torrents:
    send_email({'torrents': all_torrents})
    print("Email sent")
else:
    print("No new torrents found!")


