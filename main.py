from helpers import configs, get_torrents, send_email

all_torrents = {}
for type_ in configs['torrents']['types']:
    for page in range(1, (int(configs['torrents']['pages']) + 1)):
        torrents = get_torrents(type_, page)
        if len(torrents) > 0:
            all_torrents[type_] = torrents

if all_torrents:
    send_email({'torrents': all_torrents})
else:
    print("No new torrents found!")


