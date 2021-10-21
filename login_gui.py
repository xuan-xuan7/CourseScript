from tkinter import *


class LoginPage(Frame):

    def __init__(self):
        super().__init__()
        self.input_rate = StringVar()
        self.username = StringVar()
        self.password = StringVar()
        self.pack()
        self.createForm()

    def createForm(self):
        Label(self).grid(row=0, stick=W, pady=10)
        Label(self, text='账户: ').grid(row=1, stick=W, pady=10)
        Entry(self, textvariable=self.username).grid(row=1, column=1, stick=E)
        Label(self, text='密码: ').grid(row=2, stick=W, pady=10)
        Entry(self, textvariable=self.password, show='*').grid(row=2, column=1, stick=E)
        Button(self, text='登陆', command=self.loginCheck).grid(row=3, column=1, pady=10, stick=E)

    def loginCheck(self):
        global name
        name = self.username.get()
        global secret
        secret = self.password.get()
        self.quit()


root = Tk()
root.title('融优学堂登陆')
width = 280
height = 200
screenwidth = root.winfo_screenwidth()
screenheight = root.winfo_screenheight()
alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
root.geometry(alignstr)  # 居中对齐
name = ''
secret = ''
page1 = LoginPage()
root.mainloop()
