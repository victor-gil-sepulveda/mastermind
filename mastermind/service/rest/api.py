from flask_restful import Api
import mastermind.service.rest.v1 as v1

API_PREFIX = "mastermind"


def get_version(version_module):
    name = version_module.__name__
    return name.split(".")[-1]


def gen_resource_url(api_prefix, version_module, resource_name):
    url_parts = [api_prefix, get_version(version_module),
                 resource_name[1:] # skip first "/"
                 ]
    return "/"+"/".join(url_parts)


def setup_rest_api(flask_app):
    api = Api(flask_app)
    version = v1

    api.add_resource(version.Game,
                     gen_resource_url(API_PREFIX, version, "/game/<game_id>"),
                     gen_resource_url(API_PREFIX, version, "/game"))

    api.add_resource(version.User,
                     gen_resource_url(API_PREFIX, version, "/user/<user_id>"),
                     gen_resource_url(API_PREFIX, version, "/user"))

    api.add_resource(version.Code,
                     gen_resource_url(API_PREFIX, version, "/code/<code_id>"),
                     gen_resource_url(API_PREFIX, version, "/code"))

    api.add_resource(version.Feedback,
                     gen_resource_url(API_PREFIX, version, "/feedback/<feedback_id>"),
                     gen_resource_url(API_PREFIX, version, "/feedback"))

    api.add_resource(version.Guess,
                     gen_resource_url(API_PREFIX, version, "/guess"))
