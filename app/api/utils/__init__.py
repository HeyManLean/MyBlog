from flask_restful import reqparse


def get_params(arguments, strict=True):
    parser = reqparse.RequestParser()
    for arg in arguments:
        parser.add_argument(arg)
    values_dict = parser.parse_args(strict=strict)
    return [values_dict[arg.name] for arg in arguments]
