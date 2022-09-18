f = open('config.json', 'r')
config = json.loads(f.read())['logger']
f.close()



class Logger:
    __config = config

    def debug(text):
        if Logger.__config['debug']:
            print(text)

    def log(text):
        if Logger.__config['log']:
            print(text)
