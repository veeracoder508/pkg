from src.pkg.down import Downloader


def main():
    downloader = Downloader(base_url="http://localhost:5000")
    version_list = downloader.list_versions("pkg++")
    print(version_list)


if __name__ == "__main__":
    main()
