import sys
import cv2
from PyQt5.QtCore import Qt, QTimer,QSize
from PyQt5.QtGui import QImage, QPixmap,QIcon,QFont,QColor
from PyQt5 import QtGui 
from ultralytics import YOLO
from PyQt5.QtWidgets import QApplication, QLabel, QWidget,QPushButton,QHBoxLayout, QListWidget,QGridLayout,QGraphicsDropShadowEffect


trial="t1.jpg"
Icon_reset= "delete.png"        
icon_check="checked.png"


class Self_app(QWidget):
    def __init__(self):
        self.num_chocobread = 0
        self.num_sweet_potato = 0
        self.num_croissant = 0
        self.total_value = 0
        self.total_value2 = 0
        self.total_value3 = 0
        self.total_amount = 0

        # $ Dollar value per product
        self.choco_value =            1.50              
        self.sweet_potato_value=      2
        self.croissant_value=         1.25

        self.detected_chocobread = 0
        self.total_value = 0

        self.detected_Sweet_potato = 0
        self.total_value2 = 0

        self.detected_croissant = 0
        self.total_value3 = 0

        super().__init__()
        self.setWindowTitle("Item Checkout")
        self.setWindowIcon(QtGui.QIcon('checkout.png'))           
        self.setGeometry(100, 100, 1500, 800)
        

        layout = QGridLayout()
        layout.setContentsMargins(60, 75, 0, 0)
        self.setLayout(layout)        

        self.paddin=QLabel(self)  
        self.paddin.setObjectName("pad") 
        self.paddin.setFixedSize(700, 400)
        self.paddin.move(35,75)
        self.paddin.lower()
        
        shadow_effect = QGraphicsDropShadowEffect()
        shadow_effect.setOffset(0, 4)  
        shadow_effect.setBlurRadius(10)  
        shadow_effect.setColor(QColor(0, 0, 0, 64))  
        self.paddin.setGraphicsEffect(shadow_effect)
       
       
        #video feed
        self.video_label = QLabel(self)   
        self.video_label.setObjectName("videoList")                     
        self.video_label.setFixedSize(675, 400)                      
        layout.addWidget(self.video_label, 0, 0, Qt.AlignTop | Qt.AlignLeft)

       
        shadow_effect = QGraphicsDropShadowEffect()
        shadow_effect.setOffset(5, 0)  
        shadow_effect.setBlurRadius(10)  
        shadow_effect.setColor(QColor(0, 0, 0, 64))  
        self.video_label.setGraphicsEffect(shadow_effect)


    
        self.grad=QWidget(self)
        self.grad.setObjectName("grad")     
        
        self.grad.setFixedSize(1500, 500)
        self.grad.move(0,0)
        self.grad.lower()
                    

        self.result_label = QLabel("ITEM" + " "* 18 + "QT" , self)   
        self.result_label.setObjectName("Title")             
        self.result_label.setFixedSize(500, 50)        
        self.result_label.move(880,25)
        
                      
        #show list
        self.product_list = QListWidget(self)
        self.product_list.setObjectName("productList")        
        self.product_list.setFixedSize(680, 486)
        self.product_list.setContentsMargins(0, 0, 0, 100)                           
        layout.addWidget(self.product_list, 0, 1, Qt.AlignLeft)

        shadow_effect = QGraphicsDropShadowEffect()
        shadow_effect.setOffset(0, 4)  
        shadow_effect.setBlurRadius(10)  
        shadow_effect.setColor(QColor(0, 0, 0, 64))  
        self.product_list.setGraphicsEffect(shadow_effect)
        

        container_widget_2 = QWidget(self)
        layout_3 = QHBoxLayout(container_widget_2)
        layout_3.setSpacing(85)
        layout_3.setContentsMargins(195, 0, 0, 20)


        #scan Buttom
        self.centerBtn = QPushButton(text="Scan", parent=self)
        font = QFont("Arial", 15)  
        self.centerBtn.setFont(font)
        self.centerBtn.setFixedSize(300, 100)       
        self.centerBtn.clicked.connect(self.capture_snapshot)
        layout_3.addWidget(self.centerBtn) 
        layout.addWidget(container_widget_2, 1, 1, Qt.AlignLeft)

        shadow_effect = QGraphicsDropShadowEffect()
        shadow_effect.setOffset(0, 4)  
        shadow_effect.setBlurRadius(10)  
        shadow_effect.setColor(QColor(0, 0, 0, 64))  
        self.centerBtn.setGraphicsEffect(shadow_effect)
       

        #reset
        icon = QIcon(Icon_reset)        
        self.deleteBtn = QPushButton( parent=self)
        self.deleteBtn.setFixedSize(100, 80)       
        self.deleteBtn.clicked.connect(self.reset_session)
        self.deleteBtn.setIcon(icon)
        self.deleteBtn.setIconSize(QSize(50, 50))
        layout_3.addWidget(self.deleteBtn) 

        shadow_effect = QGraphicsDropShadowEffect()
        shadow_effect.setOffset(0, 4)  
        shadow_effect.setBlurRadius(10)  
        shadow_effect.setColor(QColor(0, 0, 0, 64))  
        self.deleteBtn.setGraphicsEffect(shadow_effect)            

        

        #Total Dolar Value
        self.checkout_total = QLabel("Total: ", self) 
        font = QFont("Arial", 32)  
        self.checkout_total.setFont(font)
        self.checkout_total.move(50, 510)
        self.checkout_total.adjustSize() 
        self.checkout_total.raise_()



        self.checkout_total2 = QLabel(f"${self.total_amount}            ", self) 
        font = QFont("Arial", 45)  
        self.checkout_total2.setFont(font)
        self.checkout_total2.move(150, 610)
        self.checkout_total2.adjustSize() 
        self.checkout_total2.raise_()

        #Check out
        icon = QIcon(icon_check)      
        self.checkBtn = QPushButton( parent=self)
        self.checkBtn.clicked.connect(self.check_items)
        self.checkBtn.setFixedSize(400, 150)       
        self.checkBtn.move(475, 600)
        self.checkBtn.setIcon(icon)
        self.checkBtn.setIconSize(QSize(200, 200))

        shadow_effect = QGraphicsDropShadowEffect()
        shadow_effect.setOffset(0, 4)  
        shadow_effect.setBlurRadius(10)  
        shadow_effect.setColor(QColor(0, 0, 0, 64))  
        self.checkBtn.setGraphicsEffect(shadow_effect)

        #Insert payment
        self.payment= QLabel("Please insert any payment method   ",parent=self)
        self.payment.setObjectName("payment")   
        self.payment.setFixedSize(400, 200)
        self.payment.setAlignment(Qt.AlignCenter)
        self.payment.move(180,170)
        self.payment.setHidden(True)       
                
        self.product_list.itemClicked.connect(self.delete_item)  
        self.cap = cv2.VideoCapture(1)   
               
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(5)       
        
        self.set_styles()                  

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:           
            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)           
            h, w, ch = rgb_image.shape            
            new_w = int(w * 0.8)  
            new_h = int(h * 0.8)  

            resized_image = cv2.resize(rgb_image, (new_w, new_h), interpolation=cv2.INTER_AREA)
            label_width = self.video_label.width()
            label_height = self.video_label.height()

            if new_w > label_width or new_h > label_height:
                resized_image = cv2.resize(resized_image, (label_width, label_height), interpolation=cv2.INTER_AREA)           
            h, w, ch = resized_image.shape
            bytes_per_line = ch * w
            qt_image = QImage(resized_image.data, 650, 350, bytes_per_line, QImage.Format_RGB888)           
            self.video_label.setPixmap(QPixmap.fromImage(qt_image))

    def capture_snapshot(self):
        ret, frame = self.cap.read()
        if ret:
            filename = "snapshot.jpg"
            cv2.imwrite(filename, frame)
            print(f"Snapshot saved as {filename}")

            model_path = r'runs/detect/train14/weights/best.pt'
            model = YOLO(model_path)

            result = model(filename, conf=0.4)  

            if result:
                detections = result[0].boxes
                num_chocobread = sum([1 for label in detections.cls if label == 0])
                num_sweet_potato = sum([1 for label in detections.cls if label == 1]) 
                num_croissant= sum([1 for label in detections.cls if label == 2])                 
                total_value = num_chocobread * self.choco_value
                total_value2= num_sweet_potato*self.sweet_potato_value
                total_value3= num_croissant*self.croissant_value

                self.detected_chocobread += num_chocobread
                self.total_value += total_value

                self.detected_Sweet_potato += num_sweet_potato
                self.total_value2 += total_value2

                self.detected_croissant += num_croissant
                self.total_value3 += total_value3
                self.product_list.clear()
                if num_chocobread != 0:
                    self.product_list.addItem("\n"+" "*5+"Chocolate Bread     "+" "*10+f"{num_chocobread}"+" "*15+f"$ {total_value}")
                if num_sweet_potato != 0:
                    self.product_list.addItem("\n"+" "*5+"Sweet Bread         "+" "*10+f"{num_sweet_potato}"+" "*15+f"$ {total_value2}")       
                if num_croissant!= 0:
                    self.product_list.addItem("\n"+" "*5+"Croissant             "+" "*10+f"{num_croissant}"+" "*15+f"$ {total_value3}")                 
            else:
                self.result_label.setText("No Items detected. Please try again")
        
            self.total_amount = self.total_value + self.total_value2 + self.total_value3            
            self.checkout_total2.setText(f"${self.total_amount}  ")
            self.num_chocobread+=num_chocobread
            self.num_sweet_potato+=num_sweet_potato
            self.num_croissant+=num_croissant
          

    def reset_session(self):
        self.detected_chocobread = 0
        self.total_value = 0        
        self.detected_Sweet_potato = 0
        self.total_value2 = 0
        self.detected_croissant = 0
        self.total_value3 = 0
        total_amount=0
        self.num_chocobread = 0
        self.num_sweet_potato = 0
        self.num_croissant = 0
        self.checkout_total2.setText(f"${total_amount}  ")
        self.product_list.clear()        
        self.centerBtn.setEnabled(True)
        self.video_label.setEnabled(True)
        self.payment.setHidden(True)
    
    def delete_item(self, item):
        item_text = item.text()
        self.product_list.takeItem(self.product_list.row(item))  
        if "Chocolate Bread" in item_text:
            self.num_chocobread -= 1  
            self.total_value -= self.choco_value  
        elif "Sweet Bread" in item_text:
            self.num_sweet_potato -= 1
            self.total_value2 -= self.sweet_potato_value
        elif "Croissant" in item_text:
            self.num_croissant -= 1
            self.total_value3 -= self.croissant_value
        self.checkout_total2.setText(f"${self.total_amount}  ")                 

        if self.num_chocobread == 0 and "Chocolate Bread" in item_text:
            self.product_list.takeItem(self.product_list.row(item))
        elif self.num_sweet_potato == 0 and "Sweet Bread" in item_text:
            self.product_list.takeItem(self.product_list.row(item))
        elif self.num_croissant == 0 and "Croissant" in item_text:
            self.product_list.takeItem(self.product_list.row(item))               

        self.total_amount = self.total_value + self.total_value2 + self.total_value3     
        self.checkout_total2.setText(f"${self.total_amount}  ")            
        self.update_product_list()

    def update_product_list(self):
        self.product_list.clear()                
        if self.num_chocobread > 0:
            self.product_list.addItem("\n"+" "*5+"Chocolate Bread     "+" "*10+f"{self.num_chocobread}"+" "*15+f"$ {self.total_value}")
        if self.num_sweet_potato > 0:
            self.product_list.addItem("\n"+" "*5+"Sweet Bread         "+" "*10+f"{self.num_sweet_potato}"+" "*15+f"$ {self.total_value2}") 
        if self.num_croissant > 0:
            self.product_list.addItem("\n"+" "*5+"Croissant             "+" "*10+f"{self.num_croissant}"+" "*15+f"$ {self.total_value3}") 
    

    def check_items(self):
        self.product_list.clear()
        if self.num_chocobread > 0:
            self.product_list.addItem("\n"+" "*5+"Chocolate Bread     "+" "*10+f"{self.num_chocobread}"+" "*15+f"$ {self.total_value}")
        if self.num_sweet_potato > 0:
            self.product_list.addItem("\n"+" "*5+"Sweet Bread         "+" "*10+f"{self.num_sweet_potato}"+" "*15+f"$ {self.total_value2}") 
        if self.num_croissant > 0:
            self.product_list.addItem("\n"+" "*5+"Croissant             "+" "*10+f"{self.num_croissant}"+" "*15+f"$ {self.total_value3}") 
        self.checkout_total2.setText(f"${self.total_amount}  ")        
           
        self.video_label.setEnabled(False)
        self.payment.setHidden(False)      
             
    
    def set_styles(self):
        self.setStyleSheet("""
            QWidget {
                font-family: "Architects Daughter", cursive;             
            }
                           
            #grad {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, 
                                            stop: 0    #005FA7,       
                                            stop: 0.8  #82B5DC,       
                                            stop: 1    rgba(130, 181, 220, 0));  
            }                                   

            #Title {
                font-family:  "Architects Daughter", cursive;      
                color: white;
                font-size: 30px;      
            }
            
            QPushButton{                       
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, 
                                stop: 0    #005FA7,       
                                stop: 0.8  #82B5DC,       
                                stop: 1    rgba(130, 181, 220));          
                border-radius: 25px;   
                color: white;  
                font-size: 50px;
                text-align: center;                               
            }
                           
            QPushButton:pressed {
                background-color: #4281B2;                          
            }

           #videoList {                           
                border: 1px solid #FFFFFF;
                border-radius: 25px;
                background-color: #FFFFFF;
                box-shadow: 2px 2px 4px rgba(0, 0, 0, 0.25);      
            }                
            #pad{
                border: 1px solid #FFFFFF;
                border-radius: 25px;
                background-color: #FFFFFF;
                box-shadow: 2px 2px 4px rgba(0, 0, 0, 0.25);
            }    
            
            #productList {                           
                font-family:  "Architects Daughter", cursive;  
                font-size: 24px;
                background-color: #FFFFFF;
                border: 1px solid #FFFFFF;
                border-radius: 25px;
                box-shadow: 4px 4px 10px #000000;                    
            }
                           
            #payment{                           
            background-color: #FFFFFF;
            font-size: 20px;                           
            border-radius: 25px;                           
            }            
        """)


    def closeEvent(self, event):
        self.cap.release()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Self_app()
    window.show()
    sys.exit(app.exec_())