import tkinter
from url import URL

WIDTH, HEIGHT = 800, 600

class Browser:
  def __init__(self):
    self.window = tkinter.Tk()
    self.canvas = tkinter.Canvas(self.window, width=WIDTH, height=HEIGHT)
    self.canvas.pack()

  def show(body):
    in_tag = False

    for c in body:
      if c == "<":
        in_tag = True
      elif c == ">":
        in_tag = False
      elif not in_tag:
        print(c, end="")

  def load(self, url):
    # body = url.request()
    # self.show(body)

    self.canvas.create_rectangle(10, 20, 400, 300)
    self.canvas.create_oval(100, 100, 150, 150)
    self.canvas.create_text(200, 150, text="Hi!")


if __name__ == "__main__":
  import sys

  Browser().load(URL(sys.argv[1]))
  tkinter.mainloop()
