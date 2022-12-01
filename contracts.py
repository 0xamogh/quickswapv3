
import requests
import json
import os
import zipfile
import pathlib

contract = "0xf5b509bb0909a69b1c207e495f687a596c168e12"

api_key = "5BYDKGPGNTPXT2BEKUYZMG5GCMIC86RUW2"

url = f"https://api.polygonscan.com/api?module=contract&action=getsourcecode&address={contract}&apikey={api_key}"

r = requests.get(url=url)

data = r.json()
json_data = json.loads(data['result'][0]["SourceCode"][1:-1])
sources = json_data["sources"]
paths = sources.keys()
repo_name = "/swap_router"


def script():
    for path in paths:
        formatted_path = get_base_path() + \
            "/" + combine_array_to_path(path.split("/")[:-1])

        # recursively create directories
        mkdir_path(formatted_path)
        write_file(formatted_path, path.split("/")[-1], path)

    # zip_that_shit()


def write_file(path, filename, key):
    new_filepath = path + "/" + filename
    f = open(new_filepath, "x")
    f.write(sources[key]['content'])
    f.close()


def combine_array_to_path(array):
    temp = ""
    for i in range(len(array)):
        temp += array[i]
        if i != len(array) - 1:
            temp += "/"
    return temp


def mkdir_path(path):
    if os.path.exists(path) or len(path) == 0:
        return
    elif not os.path.exists(combine_array_to_path(path.split("/")[:-1]).rstrip("/")):
        mkdir_path(combine_array_to_path(path.split("/")[:-1]).rstrip("/"))
    os.mkdir(path)


def zip_that_shit():
    directory = pathlib.Path(get_base_path())

    with zipfile.ZipFile(f"{repo_name}.zip", mode="w") as archive:
        for file_path in directory.rglob("*"):
            archive.write(
                file_path,
                arcname=file_path.relative_to(directory)
            )

    with zipfile.ZipFile(f"{repo_name}.zip", mode="r") as archive:
        archive.printdir()


def get_base_path():
    return os.getcwd() + repo_name


script()
