import codecs


def main():
    my_string = 'eb85b8eba0a5ec9d8020ebb0b0ec8ba0ed9598eca78020ec958aeb8a94eb8ba42e'  # noqa
    hex_mystring = codecs.decode(my_string, 'hex')
    ans = codecs.decode(hex_mystring, 'utf-8')
    print(ans)


main()
