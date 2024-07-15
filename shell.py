import newbasic

while True:
    text = input('new basic > ')
    result, error = newbasic.run('<stdin>', text)

    if error == 'NOERROR':
        print(result)
    else:
        print(error.asString())