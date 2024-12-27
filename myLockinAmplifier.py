import numpy as np
import matplotlib.pyplot as plt
from mySignalGeneration import signalGeneration

class lockinAmplifier:

    @staticmethod
    def lockIn(reference, input):
        multiplied = input * reference
        output = np.mean(multiplied)
        return output

    @staticmethod
    def timeAverage(data):
        return np.mean(data)


class examples:

    '''
    here the first signal is centred on zero.
    the second graph shows 2 signals with 2 different offsets.
    the third graph shows that once we multiply both offsets by
    the reference the time average is the same for all output signals.
    this shows that offset on the incoming signal does not affect the time average
    once multiplied by a reference signal centered on zero.
    '''
    @staticmethod
    def offsetSignalAveragingDemo(offset1, offset2, sampleRate, frequency, amplitude):
        x, yOffset = signalGeneration.squareWave(amplitude, frequency, sampleRate, 2)
        x, yCentred = signalGeneration.squareWave(1, frequency, sampleRate, 2)

        yOffset1 = signalGeneration.addOffset(yOffset, offset1)
        yOffset2 = signalGeneration.addOffset(yOffset, offset2)

        yOutOffset1 = yCentred * yOffset1
        yOutOffset2 = yCentred * yOffset2
        mean = np.mean(yOutOffset2)

        fig, (ax1, ax2, ax3) = plt.subplots(3, figsize=(8, 8))

        ax1.plot(x, yCentred, color='black', linewidth=0.5)
        ax1.set_title('Reference Signal')

        ax2.plot(x, yOffset1, color='green', linewidth=0.5)
        ax2.plot(x, yOffset2, color='blue', linewidth=0.5)
        ax2.set_title('Two Signals with Offsets')

        ax3.plot(x, yOutOffset1, color='green', linewidth=0.5)
        ax3.plot(x, yOutOffset2, color='blue', linewidth=0.5)
        ax3.plot(x, [mean] * len(x), color='red', linewidth=0.5)
        ax3.set_title('Signals Multiplied by Reference and Average shown in red')

        plt.tight_layout()
        plt.show()

    '''
    shows a sine wave can be found within noise by a lock in amplifier 
    '''
    @staticmethod
    def sineWave(sampleRate, frequency, sineAmplitude,noiseStandardDeviation):

        xAxis,y = signalGeneration.sineWave(amplitude=sineAmplitude, freq=frequency, sample_rate=sampleRate, duration=1)
        xAxis,yReference = signalGeneration.sineWave(amplitude=1, freq=frequency, sample_rate=sampleRate, duration=1)
        noise = signalGeneration.noise(0,noiseStandardDeviation, sample_rate=sampleRate, duration=1)

        yAxis = noise + y

        lockinOutput = lockinAmplifier.lockIn(reference=yReference, input=yAxis)
        print(f"Sine lock-in output = {lockinOutput}")
        print(f"Sine predicted signal amplitude = {lockinOutput * 2}")

        fig, (ax1, ax2) = plt.subplots(2, figsize=(8, 8))
        ax1.plot(xAxis, y, color='green', linewidth=0.5)
        ax1.set_xlabel('Time')
        ax1.set_ylabel('Amplitude')
        ax1.set_title('Plot 1: Target Signal')
        ax2.plot(xAxis, yAxis, color='green', linewidth=0.5)
        ax2.set_xlabel('Time')
        ax2.set_ylabel('Amplitude')
        ax2.set_title(f'Plot 2: Target Hidden in Noise, predicted initial amplitude {lockinOutput * 2}')
        plt.tight_layout()
        plt.show()

        return lockinOutput

    '''
    shows a square wave can be found within noise by a lock in amplifier 
    '''
    @staticmethod
    def squareWave(sampleRate,frequency,squareAmplitude,noiseStandardDeviation):

        xAxis, y = signalGeneration.squareWave(amplitude=squareAmplitude, freq=frequency, sample_rate=sampleRate, duration=1)
        xAxis, yReference = signalGeneration.squareWave(amplitude=1, freq=frequency, sample_rate=sampleRate, duration=1)
        noise = signalGeneration.noise(0,noiseStandardDeviation, sample_rate=sampleRate, duration=1)

        yAxis = noise + y

        lockinOutput = lockinAmplifier.lockIn(reference=yReference, input=yAxis)
        print(f"Square wave lock-in output = {lockinOutput}")
        print(f"Square wave predicted signal amplitude = {lockinOutput}")

        fig, (ax1, ax2) = plt.subplots(2, figsize=(8, 8))
        ax1.plot(xAxis, y, color='green', linewidth=0.5)
        ax1.set_xlabel('Time')
        ax1.set_ylabel('Amplitude')
        ax1.set_title('Plot 1: Target Signal')
        ax2.plot(xAxis, yAxis, color='green', linewidth=0.5)
        ax2.set_xlabel('Time')
        ax2.set_ylabel('Amplitude')
        ax2.set_title(f'Plot 2: Target Hidden in Noise, predicted initial amplitude {lockinOutput}')
        plt.tight_layout()
        plt.show()

        return lockinOutput

    '''
    expands and shows that if the square wave signal in modulated we 
    can recover the modulation signal
    '''
    @staticmethod
    def modulatedSquareWave(sampleRate, frequency, squareAmplitude, noiseStandardDeviation):

        readOut, xAxis, yAxis, yModulated, noise = [],[],[],[],[]
        xModulator, yModulator = signalGeneration.sineWave(amplitude=squareAmplitude, freq=1, sample_rate=50, duration=1)
        yModulator = signalGeneration.makePosative(yModulator)

        counter = 0
        for i in yModulator:
            xLoop, yLoop = signalGeneration.squareWave(amplitude=i, freq=frequency, sample_rate=sampleRate, duration=1)
            noiseLoop = signalGeneration.noise(0,noiseStandardDeviation, sample_rate=sampleRate, duration=1)
            xLoop = xLoop[:-1]
            yLoop = yLoop[:-1]
            noiseLoop = noiseLoop[:-1]
            noise.extend(noiseLoop)
            yModulated.extend(yLoop)
            xLoop = xLoop+counter
            xAxis.extend(xLoop)
            counter = np.max(xAxis)

        yAxis = [a + b for a, b in zip(noise, yModulated)]

        xReference, yReference = signalGeneration.squareWave(amplitude=i, freq=frequency, sample_rate=sampleRate, duration=1)
        yReference = yReference[:-1]

        subArrayCuts = [0]
        for i in xModulator:
            subArrayCuts.append(max(subArrayCuts)+sampleRate-1)

        for i in range(len(xModulator)-1):
            subarray = yAxis[subArrayCuts[i]:subArrayCuts[i+1]]
            locked = lockinAmplifier.lockIn(yReference, subarray)
            readOut.append(locked)

        fig, (ax1, ax2, ax3, ax4) = plt.subplots(4,figsize=(8, 8))

        ax1.plot(xModulator, yModulator, color='green', linewidth=0.5)
        ax1.set_xlabel('Time')
        ax1.set_ylabel('Amplitude')
        ax1.set_title('Modulation Signal')

        ax2.plot(xAxis, yModulated, color='blue', linewidth=0.5)
        ax2.set_xlabel('Time')
        ax2.set_ylabel('Amplitude')
        ax2.set_title('Modulated Square wave Signal')

        ax3.plot(xAxis, yAxis, color='blue', linewidth=0.5)
        ax3.set_xlabel('Time')
        ax3.set_ylabel('Amplitude')
        ax3.set_title('Signal plus Noise')

        ax4.plot(readOut, color='red', linewidth=0.5)
        ax4.set_xlabel('Time')
        ax4.set_ylabel('Amplitude')
        ax4.set_title('Predicted Modulation Signal')

        plt.tight_layout()
        plt.show()

    '''
    expands on previous example
    - more 'real world' as signal is positive only
    - ability to control modulation signal
    '''
    @staticmethod
    def modulatedPosativeSquareWave(sampleRate, frequency, amplitude, noiseStandardDeviation, modulationFrequency, modulationSampleRate):

        readOut, xAxis, yAxis, yModulated, noise = [], [], [], [], []
        xModulator, yModulator = signalGeneration.sineWave(amplitude=amplitude, freq=modulationFrequency/2,sample_rate=modulationSampleRate, duration=1)
        yModulator = signalGeneration.makePosative(yModulator)

        counter = 0
        for i in yModulator:
            xLoop, yLoop = signalGeneration.squareWave(amplitude=i, freq=frequency, sample_rate=sampleRate, duration=1)
            noiseLoop = signalGeneration.noise(0, noiseStandardDeviation, sample_rate=sampleRate, duration=1)
            noiseLoop = signalGeneration.makePosative(noiseLoop)
            yLoop = signalGeneration.addOffset(yLoop, i)
            xLoop = xLoop[:-1]
            yLoop = yLoop[:-1]
            noiseLoop = noiseLoop[:-1]
            noise.extend(noiseLoop)
            yModulated.extend(yLoop)
            xLoop = xLoop + counter
            xAxis.extend(xLoop)
            counter = np.max(xAxis)

        yAxis = [a + b for a, b in zip(noise, yModulated)]

        xReference, yReference = signalGeneration.squareWave(amplitude=i, freq=frequency, sample_rate=sampleRate,duration=1)
        yReference = yReference[:-1]

        subArrayCuts = [0]
        for i in xModulator:
            subArrayCuts.append(max(subArrayCuts) + sampleRate - 1)

        for i in range(len(xModulator) - 1):
            subarray = yAxis[subArrayCuts[i]:subArrayCuts[i + 1]]
            locked = lockinAmplifier.lockIn(yReference, subarray)
            readOut.append(locked)

        fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, figsize=(8, 8))

        ax1.plot(xModulator, yModulator, color='green', linewidth=0.5)
        ax1.set_xlabel('Time (/50)')
        ax1.set_ylabel('Amplitude')
        ax1.set_title('Modulation Signal')

        ax2.plot(xAxis, yModulated, color='blue', linewidth=0.5)
        ax2.set_xlabel('Time')
        ax2.set_ylabel('Amplitude')
        ax2.set_title('Modulated Square wave Signal')

        ax3.plot(xAxis, yAxis, color='blue', linewidth=0.5)
        ax3.set_xlabel('Time')
        ax3.set_ylabel('Amplitude')
        ax3.set_title('Signal plus Noise')

        ax4.plot(readOut, color='red', linewidth=0.5)
        ax4.set_xlabel('Time')
        ax4.set_ylabel('Amplitude')
        ax4.set_title('Predicted Modulation Signal')

        plt.tight_layout()
        plt.show()