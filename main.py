from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.slider import Slider
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserListView
from kivy.graphics import Color, Rectangle, Line, Ellipse
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.utils import get_color_from_hex
import os
import shutil
import math
from PIL import Image as PILImage, ImageDraw

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database")
if not os.path.exists(DB_PATH):
    os.makedirs(DB_PATH)

class VisualAlphabetApp(App):
    def build(self):
        Window.clearcolor = get_color_from_hex('#f0f2f5')
        self.drawing_active = False
        self.current_color = (0, 0, 0, 1)
        self.is_eraser = False
        self.pen_size = 3
        self.eraser_size = 10
        self.current_page_size = "A4"
        self.orientation = "vertical"
        self.display_mode = "simple"
        self.current_column_data = []
        self.selected_file = None
        self.last_saved_image = None
        
        main_layout = BoxLayout(orientation='horizontal', padding=10, spacing=10)
        self.canvas_layout = FloatLayout(size_hint_x=0.7)
        self.canvas_widget = FloatLayout()
        self.canvas_layout.add_widget(self.canvas_widget)
        
        right_panel = ScrollView(size_hint_x=0.3)
        control_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=10, padding=10)
        control_layout.bind(minimum_height=control_layout.setter('height'))
        
        register_frame = BoxLayout(orientation='vertical', size_hint_y=None, height=200, spacing=5)
        register_frame.add_widget(Label(text="ثبت عکس جدید", size_hint_y=None, height=30, bold=True))
        self.char_input = TextInput(hint_text="حرف/کلمه", size_hint_y=None, height=40)
        self.sound_input = TextInput(hint_text="تلفظ", size_hint_y=None, height=40)
        register_frame.add_widget(self.char_input)
        register_frame.add_widget(self.sound_input)
        
        btn_select = Button(text="انتخاب عکس", size_hint_y=None, height=40, background_color=get_color_from_hex('#4caf50'))
        btn_select.bind(on_press=self.select_image)
        register_frame.add_widget(btn_select)
        
        btn_register = Button(text="ثبت در دیتابیس", size_hint_y=None, height=40, background_color=get_color_from_hex('#2196f3'))
        btn_register.bind(on_press=self.save_data)
        register_frame.add_widget(btn_register)
        control_layout.add_widget(register_frame)
        
        output_frame = BoxLayout(orientation='vertical', size_hint_y=None, height=450, spacing=5)
        output_frame.add_widget(Label(text="پنل خروجی", size_hint_y=None, height=30, bold=True))
        output_frame.add_widget(Label(text="تعداد ستون‌ها:", size_hint_y=None, height=30))
        self.cols_spinner = Spinner(text='1', values=['1', '2', '3', '4', '5'], size_hint_y=None, height=40)
        output_frame.add_widget(self.cols_spinner)
        
        self.entries_layout = BoxLayout(orientation='vertical', size_hint_y=None, height=200, spacing=5)
        self.update_entry_fields()
        self.cols_spinner.bind(text=lambda instance, value: self.update_entry_fields())
        output_frame.add_widget(self.entries_layout)
        
        btn_row = BoxLayout(size_hint_y=None, height=40, spacing=5)
        btn_triangle = Button(text="مثلث", background_color=get_color_from_hex('#ff9800'))
        btn_triangle.bind(on_press=lambda x: self.display_sentence("triangle"))
        btn_row.add_widget(btn_triangle)
        btn_simple = Button(text="صفحه", background_color=get_color_from_hex('#2196f3'))
        btn_simple.bind(on_press=lambda x: self.display_sentence("simple"))
        btn_row.add_widget(btn_simple)
        btn_clear = Button(text="پاک", background_color=get_color_from_hex('#f44336'))
        btn_clear.bind(on_press=self.clear_canvas)
        btn_row.add_widget(btn_clear)
        output_frame.add_widget(btn_row)
        
        triangle_frame = BoxLayout(orientation='vertical', size_hint_y=None, height=150, spacing=5)
        triangle_frame.add_widget(Label(text="X:", size_hint_y=None, height=20))
        self.slider_x = Slider(min=-200, max=200, value=0)
        self.slider_x.bind(value=self.draw_triangle)
        triangle_frame.add_widget(self.slider_x)
        triangle_frame.add_widget(Label(text="Y:", size_hint_y=None, height=20))
        self.slider_y = Slider(min=-200, max=200, value=0)
        self.slider_y.bind(value=self.draw_triangle)
        triangle_frame.add_widget(self.slider_y)
        btn_reset = Button(text="ریست", size_hint_y=None, height=30)
        btn_reset.bind(on_press=self.reset_xy)
        triangle_frame.add_widget(btn_reset)
        output_frame.add_widget(triangle_frame)
        
        size_frame = BoxLayout(size_hint_y=None, height=40, spacing=5)
        btn_a4 = Button(text="A4")
        btn_a4.bind(on_press=lambda x: self.set_size("A4"))
        size_frame.add_widget(btn_a4)
        btn_a5 = Button(text="A5")
        btn_a5.bind(on_press=lambda x: self.set_size("A5"))
        size_frame.add_widget(btn_a5)
        btn_vertical = Button(text="عمودی")
        btn_vertical.bind(on_press=lambda x: self.set_size(orient="vertical"))
        size_frame.add_widget(btn_vertical)
        btn_horizontal = Button(text="افقی")
        btn_horizontal.bind(on_press=lambda x: self.set_size(orient="horizontal"))
        size_frame.add_widget(btn_horizontal)
        output_frame.add_widget(size_frame)
        
        save_share_frame = BoxLayout(size_hint_y=None, height=80, spacing=5, orientation='vertical')
        btn_save = Button(text="ذخیره عکس", size_hint_y=None, height=40, background_color=get_color_from_hex('#4caf50'))
        btn_save.bind(on_press=lambda x: self.save_final(share=False))
        save_share_frame.add_widget(btn_save)
        btn_share = Button(text="اشتراک‌گذاری عکس", size_hint_y=None, height=40, background_color=get_color_from_hex('#00bcd4'))
        btn_share.bind(on_press=lambda x: self.save_final(share=True))
        save_share_frame.add_widget(btn_share)
        output_frame.add_widget(save_share_frame)
        control_layout.add_widget(output_frame)
        
        paint_frame = BoxLayout(orientation='vertical', size_hint_y=None, height=300, spacing=5)
        paint_frame.add_widget(Label(text="پنل نقاشی", size_hint_y=None, height=30, bold=True))
        btn_toggle = Button(text="شروع/توقف نقاشی", size_hint_y=None, height=40, background_color=get_color_from_hex('#9c27b0'))
        btn_toggle.bind(on_press=self.toggle_drawing)
        paint_frame.add_widget(btn_toggle)
        btn_clear_drawing = Button(text="پاک کردن نقاشی", size_hint_y=None, height=40, background_color=get_color_from_hex('#f44336'))
        btn_clear_drawing.bind(on_press=self.clear_drawing)
        paint_frame.add_widget(btn_clear_drawing)
        
        color_row = BoxLayout(size_hint_y=None, height=40, spacing=5)
        colors = [(1,0,0,1), (0,1,0,1), (0,0,1,1), (1,1,0,1), (0,0,0,1)]
        for color in colors:
            btn = Button(background_color=color)
            btn.bind(on_press=lambda x, c=color: self.set_color(c))
            color_row.add_widget(btn)
        paint_frame.add_widget(color_row)
        
        paint_frame.add_widget(Label(text="سایز قلم:", size_hint_y=None, height=20))
        self.slider_pen = Slider(min=1, max=20, value=3)
        self.slider_pen.bind(value=self.update_pen_size)
        paint_frame.add_widget(self.slider_pen)
        
        btn_eraser = Button(text="پاک‌کن", size_hint_y=None, height=40)
        btn_eraser.bind(on_press=self.toggle_eraser)
        paint_frame.add_widget(btn_eraser)
        control_layout.add_widget(paint_frame)
        
        right_panel.add_widget(control_layout)
        main_layout.add_widget(self.canvas_layout)
        main_layout.add_widget(right_panel)
        
        self.canvas_widget.bind(on_touch_down=self.start_draw)
        self.canvas_widget.bind(on_touch_move=self.drawing)
        Clock.schedule_once(lambda dt: self.set_size("A4"), 0.5)
        return main_layout
          def update_entry_fields(self, *args):
        self.entries_layout.clear_widgets()
        self.entry_list = []
        num_cols = int(self.cols_spinner.text)
        for i in range(num_cols):
            entry = TextInput(hint_text=f"ستون {i+1}", size_hint_y=None, height=40)
            self.entries_layout.add_widget(entry)
            self.entry_list.append(entry)
    
    def select_image(self, instance):
        content = BoxLayout(orientation='vertical')
        file_chooser = FileChooserListView(filters=['*.png', '*.jpg', '*.jpeg'])
        content.add_widget(file_chooser)
        btn_select = Button(text="انتخاب", size_hint_y=None, height=40)
        content.add_widget(btn_select)
        self.popup = Popup(title="انتخاب عکس", content=content, size_hint=(0.9, 0.9))
        def do_select(instance):
            if file_chooser.selection:
                self.selected_file = file_chooser.selection[0]
                self.popup.dismiss()
                self.show_message("موفقیت", "عکس انتخاب شد")
        btn_select.bind(on_press=do_select)
        self.popup.open()
    
    def save_data(self, instance):
        if not self.selected_file:
            self.show_message("خطا", "ابتدا عکس انتخاب کنید")
            return
        char = self.char_input.text.strip()
        sound = self.sound_input.text.strip()
        if char and sound:
            dest = os.path.join(DB_PATH, f"{char}_{sound}.png")
            shutil.copy(self.selected_file, dest)
            self.char_input.text = ""
            self.sound_input.text = ""
            self.selected_file = None
            self.show_message("موفقیت", "ثبت شد")
    
    def toggle_drawing(self, instance):
        self.drawing_active = not self.drawing_active
        status = "فعال" if self.drawing_active else "غیرفعال"
        self.show_message("حالت نقاشی", f"حالت طراحی {status} شد")
    
    def clear_drawing(self, instance):
        self.canvas_widget.canvas.clear()
        self.set_size()
    
    def start_draw(self, instance, touch):
        if not self.drawing_active:
            return
        if self.canvas_widget.collide_point(*touch.pos):
            touch.ud['line'] = Line(points=(touch.x, touch.y), width=self.pen_size if not self.is_eraser else self.eraser_size)
            with self.canvas_widget.canvas:
                if self.is_eraser:
                    Color(1, 1, 1, 1)
                else:
                    Color(*self.current_color)
                self.canvas_widget.canvas.add(touch.ud['line'])
    
    def drawing(self, instance, touch):
        if not self.drawing_active or 'line' not in touch.ud:
            return
        touch.ud['line'].points += (touch.x, touch.y)
    
    def set_color(self, color):
        self.current_color = color
        self.is_eraser = False
    
    def toggle_eraser(self, instance):
        self.is_eraser = not self.is_eraser
    
    def update_pen_size(self, instance, value):
        self.pen_size = value
    
    def reset_xy(self, instance):
        self.slider_x.value = 0
        self.slider_y.value = 0
        self.draw_triangle()
    
    def draw_triangle(self, *args):
        if self.display_mode != "triangle":
            return
        self.canvas_widget.canvas.clear()
        cw = self.canvas_widget.width
        ch = self.canvas_widget.height
        scale_val = 0.5
        padding = 10
        available_w = cw - (padding * 2)
        available_h = ch - (padding * 2)
        side = min(available_w, available_h / (math.sqrt(3)/2)) * scale_val
        height = (math.sqrt(3) / 2) * side
        cx = cw / 2
        cy = ch / 2
        off_x = (self.slider_x.value / 200) * (available_w / 2 - side / 2)
        off_y = (self.slider_y.value / 200) * (available_h / 2 - height / 2)
        tri_cx = cx + off_x
        tri_cy = cy + off_y
        x1 = tri_cx - side/2
        y1 = tri_cy + (1/3 * height)
        x2 = tri_cx + side/2
        y2 = tri_cy + (1/3 * height)
        x3 = tri_cx
        y3 = tri_cy - (2/3 * height)
        with self.canvas_widget.canvas:
            Color(0, 0, 0, 1)
            Line(points=[x1, y1, x2, y2, x3, y3, x1, y1], width=3)
    
    def set_size(self, size=None, orient=None):
        if size:
            self.current_page_size = size
        if orient:
            self.orientation = orient
        self.canvas_widget.canvas.clear()
        cw = self.canvas_widget.width
        ch = self.canvas_widget.height
        margin = 50
        available_w = cw - (margin * 2)
        available_h = ch - (margin * 2)
        ratio = 1.41
        if self.orientation == "horizontal":
            if self.current_page_size == "A4":
                box_w, box_h = available_w, available_w / ratio
            else:
                box_w, box_h = available_w * 0.8, (available_w * 0.8) / ratio
        else:
            if self.current_page_size == "A4":
                box_h, box_w = available_h, available_h / ratio
            else:
                box_h, box_w = available_h * 0.8, (available_h * 0.8) / ratio
        x1 = cw/2 - box_w/2
        y1 = ch/2 - box_h/2
        x2 = cw/2 + box_w/2
        y2 = ch/2 + box_h/2
        with self.canvas_widget.canvas:
            if self.current_page_size == "A4":
                Color(0.08, 0.39, 0.75, 1)
            else:
                Color(0.85, 0.26, 0.08, 1)
            Line(rectangle=(x1, y1, box_w, box_h), width=3)
        self.draw_triangle()
          def display_sentence(self, mode):
        self.display_mode = mode
        self.canvas_widget.canvas.clear()
        if mode == "triangle":
            self.draw_triangle()
            return
        self.current_column_data = []
        cw = self.canvas_widget.width
        ch = self.canvas_widget.height
        start_x = (cw / 2) - (len(self.entry_list) * 40)
        col_x = start_x
        for entry in self.entry_list:
            col_images = []
            y_pos = (ch / 2) - 150
            for part in entry.text.strip().split():
                for filename in os.listdir(DB_PATH):
                    name_without_ext = os.path.splitext(filename)[0]
                    if name_without_ext == part:
                        path = os.path.join(DB_PATH, filename)
                        col_images.append(path)
                        img_widget = Image(source=path, size_hint=(None, None), size=(60, 60))
                        img_widget.pos = (col_x, y_pos)
                        self.canvas_widget.add_widget(img_widget)
                        y_pos += 70
            self.current_column_data.append(col_images)
            col_x += 80
    
    def clear_canvas(self, instance):
        for child in self.canvas_widget.children[:]:
            if isinstance(child, Image):
                self.canvas_widget.remove_widget(child)
        self.canvas_widget.canvas.clear()
        self.set_size()
    
    def save_final(self, share=False):
        if not self.current_column_data:
            self.show_message("خطا", "ابتدا نمایش دهید")
            return
        file_path = os.path.join(BASE_DIR, "share_temp.png")
        w, h = (3508, 2480) if self.orientation == "horizontal" else (2480, 3508)
        final_img = PILImage.new('RGB', (w, h), color='white')
        draw = ImageDraw.Draw(final_img)
        if self.display_mode == "triangle":
            side = 1400 * 0.5
            height = (math.sqrt(3) / 2) * side
            center_x = w/2 + (self.slider_x.value * 10)
            center_y = h/2 + (self.slider_y.value * 10)
            draw.polygon([
                (center_x - side/2, center_y + height/3),
                (center_x + side/2, center_y + height/3),
                (center_x, center_y - 2 * height / 3)
            ], outline="black", width=20)
        col_x = (w / 2) - (len(self.current_column_data) * 250)
        for col_images in self.current_column_data:
            y = 300
            for path in col_images:
                img = PILImage.open(path).resize((500, 500))
                final_img.paste(img, (int(col_x), int(y)))
                y += 550
            col_x += 550
        final_img.save(file_path)
        self.last_saved_image = file_path
        if share:
            self.share_image(file_path)
        else:
            self.show_message("موفقیت", "عکس ذخیره شد")
    
    def share_image(self, image_path):
        try:
            if os.name == 'posix':
                from jnius import autoclass
                Intent = autoclass('android.content.Intent')
                Uri = autoclass('android.net.Uri')
                File = autoclass('java.io.File')
                FileProvider = autoclass('androidx.core.content.FileProvider')
                PythonActivity = autoclass('org.kivy.android.PythonActivity')
                context = PythonActivity.mActivity
                file = File(image_path)
                uri = FileProvider.getUriForFile(
                    context,
                    context.getPackageName() + '.fileprovider',
                    file
                )
                intent = Intent()
                intent.setAction(Intent.ACTION_SEND)
                intent.setType('image/png')
                intent.putExtra(Intent.EXTRA_STREAM, uri)
                intent.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION)
                context.startActivity(Intent.createChooser(intent, 'اشتراک‌گذاری با'))
                self.show_message("موفقیت", "در حال اشتراک‌گذاری...")
            else:
                self.show_message("توجه", "اشتراک‌گذاری فقط در اندروید کار می‌کند")
        except Exception as e:
            self.show_message("خطا", f"خطا در اشتراک‌گذاری: {str(e)}")
    
    def show_message(self, title, message):
        content = BoxLayout(orientation='vertical', padding=10)
        content.add_widget(Label(text=message))
        btn = Button(text="باشه", size_hint_y=None, height=40)
        content.add_widget(btn)
        popup = Popup(title=title, content=content, size_hint=(0.6, 0.3))
        btn.bind(on_press=popup.dismiss)
        popup.open()

if __name__ == '__main__':
    VisualAlphabetApp().run()
