import vk_api
import knocker

def main():
    api = knocker.Knocker()
    api.Auth()
    api.RunLPS()

main()