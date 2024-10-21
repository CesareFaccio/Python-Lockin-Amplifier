from myLockinAmplifier import examples

def main():

    examples.offsetSignalAveragingDemo(1,2,100,3,4)
    examples.sineWave(1000, 20, 4,5)
    examples.squareWave(1000, 20, 4,5)
    examples.modulatedSquareWave(1000,30,4,10)
    examples.modulatedPosativeSquareWave(1000,30,4,10,5,100)

if __name__ == "__main__":
    main()