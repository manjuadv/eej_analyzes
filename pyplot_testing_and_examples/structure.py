def main():
    #basicStructureOneFigure()
    #basicStructureOneFigureWithSubPlot()
    basicStructureTwoPlots()
    #basicStructureTwoGraphs()
    #basicStructureOfFigures()
    #basicStructureOfFigures2()
    #basicStructureOfFigures3()

def basicStructureOneFigure():
    import matplotlib.pyplot as plt
    import numpy as np

    f1 = plt.figure()
    ax1 = f1.add_axes([0.1,0.1,0.8,0.8])
    ax1.plot(range(0,10))
    plt.show()

def basicStructureOneFigureWithSubPlot():
    import matplotlib.pyplot as plt
    import numpy as np

    x = np.arange(0, 10, 0.2)
    y = np.sin(x)
    fig, ax = plt.subplots()
    ax.plot(x, y)
    plt.show()

def basicStructureTwoGraphs():
    import matplotlib.pyplot as plt
    import numpy as np

    x = np.arange(0, 10, 0.2)
    y = np.sin(x)
    z = np.cos(x)

    fig, ax = plt.subplots()
    ax.plot(x, y, label='sin')
    ax.plot(x, z, label='cos')

    plt.xlabel('Time (hours)')
    plt.xticks( rotation= 90 )
    plt.ylabel('Component ')
    plt.xlim(0, 7.07)
    plt.legend()
    plt.show()

def basicStructureTwoPlots():
    import matplotlib.pyplot as plt
    import numpy as np

    x = np.arange(0, 10, 0.2)
    y = np.sin(x)
    z = np.sin(x)

    fig, (ax1, ax2) = plt.subplots(2, 1)
    ax1.set(xlim=[0, 7.07], ylabel='Sin Value', title='Sin')
    ax2.set(xlim=[0, 7.07], xlabel='Angle', ylabel='Cos Value')
    ax1.plot(x, y, label='sin')
    ax2.plot(x, z, label='cos')
    ax1.legend()
    ax2.legend()
    plt.show()

def basicStructureOfFigures():
    import matplotlib.pyplot as plt
    import numpy as np

    f1 = plt.figure()
    f2 = plt.figure()
    ax1 = f1.add_subplot(111)
    ax1.plot(range(0,10))
    ax2 = f2.add_subplot(111)
    ax2.plot(range(10,20))
    f1.show()

def basicStructureOfFigures2():
    import matplotlib.pyplot as plt
    import numpy as np

    f1 = plt.figure()
    #f2 = plt.figure()
    ax1 = f1.add_axes([0.1,0.1,0.8,0.8])
    ax1.plot(range(0,10))
    #ax2 = f2.add_axes([0.1,0.1,0.8,0.8])
    #ax2.plot(range(10,20))
    plt.show()

def basicStructureOfFigures3():
    import matplotlib.pyplot as plt
    import numpy as np

    f1 = plt.figure()
    f2 = plt.figure()
    ax1 = f1.add_axes([0.1,0.1,0.8,0.8])
    ax1.plot(range(0,10))
    ax2 = f2.add_axes([0.1,0.1,0.8,0.8])
    ax2.plot(range(10,20))
    plt.show()

if __name__ == "__main__":
    main()