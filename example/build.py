from src.pkg.bulid import Builder


def main():
    builder = Builder("pkg++")
    output_file = builder.build()


if __name__ == "__main__":
    main()
