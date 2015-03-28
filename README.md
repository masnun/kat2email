## KAT2EMAIL
__Monitors Kick Ass Torrents for new Torrents and emails them__   

### What does it do?

I am a big fan of several TV series which I watch from torrents. Kick Ass Torrents is my favorite service for tracking new torrents. It gets a little hard sometimes to repeatedly check KAT for new episodes of my favorite series. So I decided to automate the task. 

When you run `python main.py` it scrapes the torrents available in the `types` (eg. tv, movies, animes) you choose and matches with a set of `keywords` you defined. If there are new torrents available, it sends you an email with the list. It uses MongoDB for storing which torrent it has already emailed. 


### Requirements 

* Python 3
* MongoDB

You need to install the dependencies using `pip`

	pip install -r requirements.txt
	

### Running

Execute `main.py`: 

	python main.py
	
You should add the script to a cron job for repeatedly checking. 

### Configuration

Edit `config.yaml` for different configuration options. You can configure pretty much everything. It uses YAML format. 

Here are the summary of available configuration options.


__Torrents__:

Choose the `type` of torrents you would like to monitor and choose the `keywords` you want to look for. You can also choose the number of `pages` it should monitor (it helps in the case of less popular items) and the `source` url (in case the domain changes or you want to use a KAT proxy). 


__Email__: 

The options are fairly obvious. You choose the `to`, `from`, `subject`, `template` and the `smtp` details. I locally use Postfix which doesn't need authentication. If your SMTP server needs auth, please modify the `send_email` function in `helpers.py` accordingly. 

__Mongo__: 

This section should contain your MongoDB `host`, `port` and preferred `database` and `collection`


### Additional Help

If you need further assistance, you can create an issue on Github or email me to masnun [at] gmail.com 

