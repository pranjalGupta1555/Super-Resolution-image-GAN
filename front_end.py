from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
import sqlite3
import re
from skimage import data, io, filters
import Utils, Utils_model
from keras.models import load_model
from Utils_model import VGG_LOSS

image_shape = (96,96,3)
loss = VGG_LOSS(image_shape)
model = load_model("gen_model3000.h5" , custom_objects={'vgg_loss': loss.vgg_loss})

kv_file=Builder.load_file("design.kv")

conn = sqlite3.connect('Users_database.sqlite')
cur = conn.cursor()
print("Successfully Connected to SQLite database")

cur.execute('''CREATE TABLE IF NOT EXISTS Users
    (id INTEGER PRIMARY KEY AUTOINCREMENT, Name TEXT, Email_id TEXT,
     Username TEXT, Password TEXT)''')

    # Create both screens. Please note the root.manager.current: this is how
    # you can control the ScreenManager from kv. Each screen has by default a
    # property manager that gives you the instance of the ScreenManager used.
    # Declare both screens
class Pop(FloatLayout):
    pass

class Pop2(FloatLayout):
    pass

class Pop3(FloatLayout):
    pass

class Pop4(FloatLayout):
    pass

class MenuScreen(Screen):
    test=ObjectProperty()
    def exit_released(self):
        cur.close()
        exit()

class SignupScreen(Screen):
    def submit_for_signup_released(self):
        flag=0
        cur.execute('SELECT Username from Users')
        row = cur.fetchone()
        while row is not None:
            if(self.ids.username.text==row[0]):
                flag=1
                self.ids.username.text=""
                popup_window2=Popup(title='Pop_Up Window', content=Pop2(), size_hint=(None,None), size=(400,400))
                popup_window2.open()
            row = cur.fetchone()
        if(flag==0 and (re.search('\S+@\S+', self.ids.email_id.text) and ((self.ids.email_id.text).endswith("gmail.com") or (self.ids.email_id.text).endswith("yahoo.in") or (self.ids.email_id.text).endswith("orkut.com")))):
            cur.execute('INSERT INTO Users(Name,Email_id,Username,Password) VALUES(?,?,?,?)',(self.ids.name_of_user.text,self.ids.email_id.text,self.ids.username.text,self.ids.passwd.text))
            conn.commit()
            self.ids.name_of_user.text = ""
            self.ids.email_id.text = ""
            self.ids.username.text = ""
            self.ids.passwd.text = ""
            popup_window3=Popup(title='Pop_Up Window', content=Pop3(), size_hint=(None,None), size=(400,400))
            popup_window3.open()
        elif(flag==0):
            flag=1
            popup_window4=Popup(title='Pop_Up Window', content=Pop4(), size_hint=(None,None), size=(400,400))
            popup_window4.open()
            self.ids.email_id.text=""

flag = 0
class LoginScreen(Screen):
    def submit_for_login_released(self):
        cur.execute('SELECT Username, Password from Users')
        row = cur.fetchone()
        while row is not None:
            if(self.ids.login_username.text==row[0] and self.ids.login_password.text==row[1]):
                print("hello")
                self.ids.login_username.text = ""
                self.ids.login_password.text = ""
                sm.current="work_screen"
                flag = 1
                break
            else:
                flag=0
                row = cur.fetchone()
        if(flag==0):
            popup_window=Popup(title='Pop_Up Window', content=Pop(), size_hint=(None,None), size=(400,400))
            popup_window.open()
class WorkScreen(Screen):
    images=[]
    #files=[]
    filenames=[]
    def selected(self,filename):
        self.ids.image.source = filename[0]
        fname_list=filename[0].split('\\')
        fname=fname_list[len(fname_list)-1]
        self.filenames.append(fname)
        image = data.imread(filename[0])
        self.images.append(image)
        #self.files.append(filename[0])
        print(fname)
    def enhance(self):
        #self.ids.work_console.text="Enhancing..............................."
        self.ids.work_console.text=""
        print(self.filenames)
        x_test_lr = Utils.lr_images(self.images, 4)
        x_test_lr = Utils.normalize(x_test_lr)
        Utils.plot_test_generated_images('./output3/', model, x_test_lr, self.filenames)
        #self.ids.work_console.text="Enhancing..............................."
        flag2=1
        if(flag2==1):
            self.ids.work_console.text="DONE.........Output saved in output3 folder"
            self.images=[]
            self.filenames=[]

class WorkScreen2(Screen):
    def enhance_check(self,filename):
        #print(filename)
        images=[]
        filenames=[]
        fname_list=filename[0].split('\\')
        fname=fname_list[len(fname_list)-1]
        print(fname)
        self.ids.image1.source = filename[0]
        image = data.imread(filename[0])
        images.append(image)
        filenames.append(fname)
        x_test_lr = Utils.lr_images(images, 4)
        x_test_lr = Utils.normalize(x_test_lr)
        Utils.plot_test_generated_images('./output3/', model, x_test_lr,filenames)
        self.ids.image2.source = './output3/'+fname+'-super'+'.jpg'
        self.ids.image3.source = './output3/manually_converted/'+fname+'-manual'+'.jpg'
# Create the screen manager
sm = ScreenManager()
sm.add_widget(MenuScreen(name='menu'))
sm.add_widget(SignupScreen(name='signup_screen'))
sm.add_widget(LoginScreen(name='login_screen'))
sm.add_widget(WorkScreen(name='work_screen'))
sm.add_widget(WorkScreen2(name='work_screen2'))

class Super_Resolution_image_GANApp(App):

    def build(self):
        return sm

if __name__ == '__main__':
    Super_Resolution_image_GANApp().run()
