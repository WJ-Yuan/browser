import tkinter, tkinter.font as tkfont
from url import URL

WIDTH, HEIGHT = 800, 600
HSTEP, VSTEP = 13, 18
SCROLL_STEP = 100

def layout(text):
  font = tkfont.Font()
  display_text = []
  cursor_x, cursor_y = HSTEP, VSTEP

  for word in text.split():
    w = font.measure(word)
    display_text.append((cursor_x, cursor_y, word))
    cursor_x += w + font.measure(" ")

    if cursor_x + w >= WIDTH - HSTEP:
      cursor_y += font.metrics("linespace") * 1.25
      cursor_x = HSTEP

  return display_text

def lex(body):
  in_tag = False
  text = ""

  for c in body:
    if c == "<":
      in_tag = True
    elif c == ">":
      in_tag = False
    elif not in_tag:
      text += c

  return text

class Browser:
  def __init__(self):
    self.window = tkinter.Tk()
    self.canvas = tkinter.Canvas(self.window, width=WIDTH, height=HEIGHT)
    self.canvas.pack()

    self.scroll = 0
    self.window.bind("<Down>", self.scroll_down)
    self.window.bind("<Up>", self.scroll_up)

  def scroll_down(self, e):
    self.scroll += SCROLL_STEP
    self.draw()

  def scroll_up(self, e):
    self.scroll -= SCROLL_STEP
    self.draw()

  def draw(self):
    self.canvas.delete("all")
    for x, y, c, in self.display_text:
      # 跳过屏幕外的字符绘制
      if y > self.scroll + HEIGHT: continue
      if y + VSTEP < self.scroll: continue

      self.canvas.create_text(x, y - self.scroll, text=c, anchor="nw")

  def load(self, url):
    body = url.request()
    text = lex(body)
    self.display_text = layout(text)
    self.draw()


if __name__ == "__main__":
  import sys

  Browser().load(URL(sys.argv[1]))
  tkinter.mainloop()
