import tkinter


class Homepage:

	def __init__(self, root, theTitle):
		self.root = root
		self.theTitle = theTitle

	def setInterface(self):
		self.root.title(self.theTitle)
		self.root.geometry('480x250')
		self.root.resizable(0,0)

	def getNewButton(self, btnName, r, c, s = "nw", w =7, h = 2):
		btn = tkinter.Button(self.root, text = btnName, width = w, height=h)
		btn.grid(row = r, column = c, sticky = s)
		return btn

	def moveItem(self, name, r, c, s = "nw"):
		name.grid(row = r, column = c, sticky = s)

	def getNewLabel(self, labelName, r, c, s = "nw", w =7, h = 2):
		label = tkinter.Label(self.root, text = labelName, width = w, height=h, justify = "left")
		label.grid(row = r, column = c, sticky = s)
		return label

	def hide(self,B):
		if(B['state'] == tkinter.NORMAL):
			B['state'] = tkinter.DISABLED

	def appear(self,B):
		if(B['state'] == tkinter.DISABLED):
			B['state'] = tkinter.NORMAL

	def getNewEntry(self, r, c, entryName = "", s = "ns"):
		e = tkinter.Entry(self.root)
		e.grid(row=r, column=c, sticky=s)
		e.insert(0,entryName)
		return e

	def getScrollbar(self, r, c, s = 'ns'):
		sb = tkinter.Scrollbar(self.root)
		sb.grid(row = r, column = c, sticky='ns')
		return sb

	def getListbox(self, r, c, list, sb, s = 'nw'):
		lb = tkinter.Listbox(self.root, yscrollcommand=sb.set, selectmode=tkinter.SINGLE)
		for item in list:
			lb.insert("end", item)
		lb.grid(row = r, column = c, sticky=s)
		return lb
