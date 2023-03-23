import os


def generate_project_tree():
    os.system("tree -I '__pycache__|migrations|migrations1'")


if __name__ == "__main__":
    generate_project_tree()
