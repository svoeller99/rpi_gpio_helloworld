def degrees_to_duty_cycle(degrees):
    if degrees < 0:
        degrees = 0
    if degrees > 180:
        degrees = 180
    return ((degrees / 180) * 10)+2

if __name__ == '__main__':
    for degree in range(0,181):
        print(f"{degree} - {degrees_to_duty_cycle(degree)}")
