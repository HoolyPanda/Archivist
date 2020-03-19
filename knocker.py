import vk_api
import LongPollServer


class Knocker:
    def __init__(self):
        # self.login = open('./login.cred', 'r').read()
        # self.password = open('./password.cred', 'r').read()
        self.token = open('./token.cred', 'r').read()
        pass

    def Auth(self):
        self.session = vk_api.VkApi(token=self.token)
        try:
            self.session._auth_token()

        except Exception as e:
            print(str(e))
            quit
        pass

    def RunLPS(self):
        self.lps = LongPollServer.LongPollServer(self.session)
        self.lps.setDaemon(True)
        self.lps.start()
        self.lps.join()
