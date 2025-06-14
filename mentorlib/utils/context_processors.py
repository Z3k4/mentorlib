from mentorlib.settings import BASE_DIR
import json
def site_settings(request):
    settings = []
    with open(f"{BASE_DIR}/config.json", "r") as file:
        settings = json.loads(file.read())
    return {'site_settings': settings}