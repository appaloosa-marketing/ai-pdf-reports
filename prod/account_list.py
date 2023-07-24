"""
Master file for accessing account names, data, info.
"""


class Account:
    def __init__(self, name, env, cloudfronturl, distribution, fb_amazon_ads):
        self.name = name
        self.env = env # Path to .env file which contains links to data
        self.cloudfronturl = cloudfronturl
        self.distribution = distribution
        self.fb_amazon_ads = fb_amazon_ads


global client_list
client_list = []

                    #------------------#
                    #  CLIENT ACOUNTS  #
                    #------------------#


shoc = {
    "name": "SHOC",
    "env": "env/shoc.env",
    "cloudfronturl": "https://d3ofvee3mvq26s.cloudfront.net",
    "distribution": "E21RN14Y6OXFKP",
    "fb_amazon_ads": False
}

client_list.append(Account(**shoc))

doodlegnome = {
    "name": "Doodle Gnome",
    "env": "env/doodlegnome.env",
    "cloudfronturl": "https://d3gdwmfbv9x98x.cloudfront.net",
    "distribution": "E2ATBDXK9KCOPM",
    "fb_amazon_ads": True
}
client_list.append(Account(**doodlegnome))


splash = {
    "name": "Splash",
    "env": "env/splash.env",
    "cloudfronturl": "https://d3m56nydho1zwc.cloudfront.net",
    "distribution": "E26RP64T1ZNC14",
    "fb_amazon_ads": False
}
client_list.append(Account(**splash))

def printClients():
    for account in client_list:
        print(u'\u2500' * 50)
        for key, value in vars(account).items():
            print(f"{key}: {value}")
        print(u'\u2500' * 50)

def printAmazonFBClients():
    for account in client_list:
        if account.fb_amazon_ads == True:
            print('yea')
        else:
            print('no')

if __name__ == '__main__':
    printClients()
    printAmazonFBClients()