import tkinter, tkinter.font as tkfont
from url import URL

WIDTH, HEIGHT = 800, 600
HSTEP, VSTEP = 13, 18
SCROLL_STEP = 100
FONT_SIZE = 12

class Tag:
  def __init__(self, tag):
    self.tag = tag

class Text:
  def __init__(self, text):
    self.text = text

class Layout:
  def __init__(self, tokens):
    self.display_list = []
    self.size = FONT_SIZE
    self.cursor_x, self.cursor_y = HSTEP, VSTEP
    self.weight, self.style = "normal", "roman"

    for tok in tokens:
      self.token(tok)

  def token(self, tok: Tag):
    if isinstance(tok, Text):
      for word in tok.text.split():
        self.word(word)
    elif tok.tag == "small":
        self.size -= 2
    elif tok.tag == "/small":
        self.size += 2
    elif tok.tag == "big":
        self.size += 4
    elif tok.tag == "/big":
        self.size -= 4
    elif tok.tag == "i":
      self.style = "italic"
    elif tok.tag == "/i":
      self.style = "roman"
    elif tok.tag == "b":
      self.weight = "bold"
    elif tok.tag == "/b":
      self.weight = "normal"

  def word(self, word):
    font = tkfont.Font(
          size=self.size,
          weight=self.weight,
          slant=self.style
        )
    w = font.measure(word)
    self.display_list.append((self.cursor_x, self.cursor_y, word, font))
    self.cursor_x += w + font.measure(" ")

    if self.cursor_x + w >= WIDTH - HSTEP:
      self.cursor_y += font.metrics("linespace") * 1.25
      self.cursor_x = HSTEP


def lex(body):
  out = []
  buffer = ""
  in_tag = False

  for c in body:
    if c == "<":
      in_tag = True
      if buffer:
        out.append(Text(buffer))
      buffer = ""
    elif c == ">":
      in_tag = False
      out.append(Tag(buffer))
      buffer = ""
    else:
      buffer += c

  if not in_tag and buffer:
    out.append(Text(buffer))

  return out

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
    for x, y, c, f in self.display_list:
      # 跳过屏幕外的字符绘制
      if y > self.scroll + HEIGHT: continue
      if y + VSTEP < self.scroll: continue

      self.canvas.create_text(x, y - self.scroll, text=c, font=f, anchor="nw")

  def load(self, url: URL):
    body = url.request()
    tokens = lex(body)
    self.display_list = Layout(tokens).display_list
    self.draw()


if __name__ == "__main__":
  import sys

  Browser().load(URL(sys.argv[1]))
  tkinter.mainloop()
