import wx
from controller import Controller

def main():
    app = wx.App(False)
    frame = Controller()
    frame.Show(True)
    app.MainLoop()

if __name__ == "__main__":
    main()