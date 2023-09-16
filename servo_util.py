def degrees_to_duty_cycle(degrees):
    return ((degrees / 180) * 10)+2

if __name__ == '__main__':
    for degree in range(0,181):
        print(f"{degree} - {degrees_to_duty_cycle(degree)}")
