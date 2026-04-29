from src.pkg.bulid.publish import Publisher


def main():
    publisher = Publisher()
    publisher.sendtoserver("pkg++", "0.0.0", "wheels/pkg++.tar.gz")


if __name__ == "__main__":
    main()
