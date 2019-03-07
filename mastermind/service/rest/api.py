from flask_restful import Api
import mastermind.service.rest.v1 as v1

API_PREFIX = "mastermind"


def get_version(version_module):
    name = version_module.__name__
    return name.split(".")[-1]


def gen_resource_url(api_prefix, version_module, resource_name):
    url_parts = [api_prefix, get_version(version_module), resource_name]
    print "/"+"/".join(url_parts)
    return "/"+"/".join(url_parts)


def setup_rest_api(flask_app):
    api = Api(flask_app)

    version = v1

    api.add_resource(version.Game,
                     gen_resource_url(API_PREFIX, version, "game/<game_id>"),
                     gen_resource_url(API_PREFIX, version, "game"))


