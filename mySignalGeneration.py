import numpy as np
from scipy import signal
import math


class signalGeneration:

    def sineWave(amplitude, freq, sample_rate, duration):
        x = np.linspace(0, duration, int(sample_rate * duration))
        frequencies = x * freq
        y = np.sin((2 * np.pi) * frequencies) * amplitude
        return x, y

    def line(m,k,numberOfSamples):
        x = np.linspace(0, numberOfSamples, int(numberOfSamples))
        y = [m*x + k for x in x]
        return x, y

    def squareWave(amplitude, freq, sample_rate, duration):
        x = np.linspace(0, duration, int(sample_rate * duration))
        frequencies = x * freq
        y = signal.square((2 * np.pi) * frequencies) * amplitude
        return x, y

    def noise(offset, standardDeviation, sample_rate, duration):
        total_samples = sample_rate * duration
        noise = np.random.normal(offset, standardDeviation, total_samples)
        return noise

    def posativeNoise(offset, standardDeviation, sample_rate, duration):
        total_samples = sample_rate * duration
        noise = np.random.normal(offset, standardDeviation, total_samples)
        signalGeneration.makePosative(noise)
        return noise

    def makePosative(data):
        for i in range(len(data)):
            if data[i] < 0:
                data[i] = -data[i]
        return data

    def addOffset(y,offset):
        y = y + offset
        return y

    def variableSquareWave(amplitude, highDuration, lowDuration, sampleRate, duration):

        numberOfSamples = int(sampleRate * duration)
        timePerSample = duration/int(numberOfSamples-1)
        xBase = np.linspace(0, duration, int(numberOfSamples)).tolist()
        x,y = [],[]

        signalY = [amplitude] * (highDuration+1)
        signalY.extend([0]*(lowDuration+1))
        signalX = [0]
        signalX.extend(xBase[1:highDuration+1])
        signalX.extend(xBase[highDuration:highDuration+lowDuration])
        signalX.append(max(signalX)+timePerSample)

        for i in range(int(math.ceil((numberOfSamples/(highDuration+lowDuration))))):
            y.extend(signalY)
            x.extend([x + i*((highDuration+lowDuration)*timePerSample) for x in signalX])

        time = duration
        numberOfJumps = 0
        while time>0:
            time -= highDuration * timePerSample
            if time > 0:
                numberOfJumps += 1
            time -= lowDuration * timePerSample
            if time > 0:
                numberOfJumps += 1

        y = y[:numberOfSamples+numberOfJumps]
        x = x[:numberOfSamples+numberOfJumps]

        return x, y