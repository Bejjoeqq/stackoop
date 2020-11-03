from tkinter.ttk import Label,Button,Entry
from tkinter import Tk,messagebox
from collections import deque
from urllib import parse,request
from lxml import html

class myDek(deque):
	def __init__(self,*initial):
		if initial is not None:
			for x in initial:
				self.append(x)

	def __add__(self,data):
		self.append(data)
		return self
		
	def __str__(self):
		text = ""
		for x in self:
			text += str(x)+"\n"
		return text

	def back(self):
		return self.pop()

	def history(self,data):
		if data not in self:
			self.append(data)
		

class Url:
	def __init__(self, url):
		self.url = url
		self.parse = parse.urlparse(self.url)
		self.obj = list()
		self.obj.append("Scheme: "+self.parse.scheme if self.parse.scheme else "http")
		self.obj.append("Net Location: "+"80" if self.parse.port is None else self.parse.port)
		self.obj.append("Port: "+self.parse.netloc if self.parse.netloc else self.parse.path)
		self.obj.append("Path: "+self.parse.path)
		self.obj.append("Query: "+self.parse.query)

	def __iter__(self):
		self.iterasi = 0
		return self

	def __next__(self):
		x = self.iterasi
		if x>len(self.obj)-1:
			raise StopIteration
		self.iterasi = x + 1
		return self.obj[x]
	def title(self):
		try:
			f = request.urlopen(self.url)
			data = f.read()
			tree = html.fromstring(data)
			title = tree.xpath("//title")[0].text
		except:
			title = self.url
		return title

class Tampil(Tk):
	def __init__(self):
		super().__init__()
		self.dekPrev = myDek()
		self.dekNext = myDek()
		self.dekHistory = myDek()
		self.current = ""

		#Windows
		self.title("Stack Using Deque")
		self.geometry("400x160")


		#Label
		self.lblTitle = Label(self, text="Bejjo Parse Browser", foreground ="blue")
		self.lblTitle.grid(row=0, column=2, pady = 5, padx=2)

		self.lblBody = Label(self, text="Welcome")
		self.lblBody.grid(row=2, column=0, columnspan=4, pady = 5, padx=2)


		#Button
		self.btnPrev = Button(self, text="<", width=5, state="disabled", command = self.prev)
		self.btnPrev.grid(row=1, column=0, pady = 5, padx=2)

		self.btnNext = Button(self, text=">", width=5, state="disabled", command = self.next)
		self.btnNext.grid(row=1, column=1, pady = 5, padx=2)

		self.btnSearch = Button(self, text="Search", width=8, command = self.search)
		self.btnSearch.grid(row=1, column=3, pady = 5, padx=2)

		self.btnHistory = Button(self, text="History", width=12, command = self.history)
		self.btnHistory.grid(row=0, column=0, columnspan=2, pady = 5, padx=2)

		self.btnParse = Button(self, text="Parse", width=8, command = self.parse)
		self.btnParse.grid(row=0, column=3, pady = 5, padx=2)


		#Entry
		self.txtSearch = Entry(self, width=40)
		self.txtSearch.grid(row = 1, column = 2, pady = 5, padx=2)

	def parse(self):
		if self.btnParse["text"] == "Parse":
			teks = "Welcome"
			if self.current != "":
				teks = ""
				url = Url(self.current)
				for x in url:
					teks += x + "\n"
			self.lblBody["text"] = teks
			self.btnParse["text"] = "Close"
			self.btnHistory["text"] = "History"
		else:
			self.btnParse["text"] = "Parse"
			self.switch_attr()

	def history(self):
		if self.btnHistory["text"] == "History":
			self.lblBody["text"] = self.dekHistory
			self.btnHistory["text"] = "Close"
			self.btnParse["text"] = "Parse"
		else:
			self.btnHistory["text"] = "History"
			self.switch_attr()

	def data(self):
		teks = "Welcome"
		if self.current != "":
			url = Url(self.current)
			teks = url.title()
		return teks

	def switch_attr(self):
		if len(self.dekPrev)==0:
			self.btnPrev["state"] = "disabled"
		else:
			self.btnPrev["state"] = "normal"

		if len(self.dekNext)==0:
			self.btnNext["state"] = "disabled"
		else:
			self.btnNext["state"] = "normal"

		self.txtSearch.delete(0,"end")
		self.txtSearch.insert(0,self.current)

		teks = self.data()
		self.lblBody["text"] = teks

	def prev(self):
		self.dekNext+self.current
		self.current = self.dekPrev.back()
		self.btnHistory["text"] = "History"
		self.btnParse["text"] = "Parse"
		self.switch_attr()

	def next(self):
		self.dekPrev+self.current
		self.current = self.dekNext.back()
		self.btnHistory["text"] = "History"
		self.btnParse["text"] = "Parse"
		self.switch_attr()

	def search(self):
		url = self.txtSearch.get().strip()
		if self.current == url and url:
			self.btnHistory["text"] = "History"
			self.btnParse["text"] = "Parse"
			self.switch_attr()
		elif "http" == url[:4] and len(url.replace("http","",1).strip())>5 and "." in url:
			self.dekPrev+self.current
			self.current = url
			self.dekNext = myDek()
			self.dekHistory.history(self.current)
			self.btnHistory["text"] = "History"
			self.btnParse["text"] = "Parse"
			self.switch_attr()
		else:
			messagebox.showinfo("Warning", "Incorrect URL")

if __name__ == '__main__':
	rt = Tampil()
	rt.resizable(width=False, height=True)
	rt.mainloop()
else:
	print("Run the main program.")
		
