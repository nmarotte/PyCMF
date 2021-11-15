from Earth.earth import Earth

if __name__ == '__main__':
    earth = Earth((10,10,10))
    print(earth[0])
    for i in range(1000):
        earth.update()