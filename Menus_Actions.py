from time import sleep
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup

class Operations_Menus():

    def __init__(self) -> None:
        
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--mute-audio")
        
        
            
        from webdriver_manager.chrome import ChromeDriverManager
        self.driver = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=chrome_options)
        print("Opened with Dynamic Webdriver")
        self.driver.maximize_window()
        self.driver.get("https://lt.elmenus.com/lt/login")
        self.user = "------"   #enter user of el menus
        self.password = "-------"    #enter password of el menus
        self.order_status = False
        self.driver.find_element(by=By.NAME,value="username").send_keys(self.user)
        self.driver.find_element(by=By.NAME,value="password").send_keys(self.password)
        self.driver.find_element(by=By.XPATH,value="/html/body/div/div/article/article/section[2]/section/form/button").click()
        sleep(10)
        #self.driver.find_element(by=By.CLASS_NAME,value="elmenus-textbox elmenus-textbox--large elmenus-textbox--end-padding")
        self.driver.get("https://lt.elmenus.com/lt/orders/new/")
        
    def wait_m(self,sec):
        self.driver.implicitly_wait(sec)

         
    def search_Accepted(self,phone_num):
        self.driver.get("https://lt.elmenus.com/lt/orders/active/")
        self.driver.implicitly_wait(3)
        self.driver.find_element(by=By.XPATH,value="/html/body/div/div/section/article/section[2]/section/section[3]/article[1]/div/section/input").send_keys(phone_num)
        self.driver.implicitly_wait(5)
        try :
            accepted_orders = self.driver.find_elements(by=By.CLASS_NAME,value="ACCEPTED")
            if len(accepted_orders) == 1 :
                accepted_orders[0].click()
                print("he have order")
            else:
                print("have more than one order")    
        except NoSuchElementException:
            print("no order in this number")
            return False





    def accept_new_order (self):
        try:
            self.driver.find_element(by=By.CLASS_NAME,value="ordercard-container__data").click() # order body to click
            self.wait_m(10)
            self.driver.find_element(by=By.XPATH,value="/html/body/div/div/section/article/section[2]/section/section[3]/article[2]/div/div/div[6]/div[2]/div/button[1]").click() # accept btn
            self.wait_m(10)
            self.driver.find_element(by=By.XPATH,value="/html/body/div[2]/div/div[2]/button[2]").click() # confirm btn
            self.wait_m(10)
            sleep(3)  # --> 10
            statu = self.driver.find_element(by=By.XPATH,value="/html/body/div/div/section/article/section[2]/section/section[3]/article[2]/div/div/div[2]/div/button").text
            self.order_new = True
            if statu == "ACCEPTED" :
                self.order_status = True
            else :
                self.order_status = False
        except NoSuchElementException:
            self.order_status = False
            self.order_new = False
        except Exception :
            self.order_status = False
            self.order_new = False
            print(Exception)
        return self.order_new , self.order_status
        


#--------------------------------------------------must in work hour -------------------------------------------------------------
        






    def get_items (self):  
        self.items = []
        num_items = self.driver.find_elements(by=By.CLASS_NAME,value="order-category-item")
        type_ = self.driver.find_elements(by=By.CLASS_NAME, value="order-category-item-body")
        n1 = 2     # item
        n2 = 1     # mod_item
        n = 0
        for i in num_items :
            data_item = i.find_element(by=By.TAG_NAME,value="h3").text
            #type = self.driver.find_element(by=By.XPATH,value="/html/body/div/div/section/article/section[2]/section/section[3]/article[2]/div/div/div[4]/div["+str(n1)+"]/div[2]/div["+str(n2)+"]/div[2]/h5[1]/p").text #type or item
            ps = BeautifulSoup(type_[n].get_attribute("innerHTML"),"html.parser")
            type = ps.find("h5",class_ = "ui left floated header").find("span").text
            n += 1
            item_qty = list(data_item)[0]
            item_comment = data_item[1]
            data_item = data_item.split("X")[1]
            data_item = data_item.split(" - ")
            item_name = data_item[0]
            if len(data_item) > 1:
                item_comment = data_item[1]
            else:
                item_comment = "no comment"
            all_mod = []
            try :
                h = self.driver.find_element(by=By.XPATH,value="/html/body/div/div/section/article/section[2]/section/section[3]/article[2]/div/div/div[4]/div["+str(n1)+"]/div[2]/div/div[2]/h5[1]/div") # check modefire
                order_body = self.driver.find_elements(by=By.CLASS_NAME , value="order-category-item-body")
                soup = BeautifulSoup(order_body[n1-2].get_attribute("innerHTML"),"html.parser")
                mod_elm = soup.find_all("i", class_="icon-container fas fa-utensils")
                
                for k in mod_elm :
                    mod_name = self.driver.find_element(by=By.XPATH,value="/html/body/div/div/section/article/section[2]/section/section[3]/article[2]/div/div/div[4]/div["+str(n1)+"]/div[2]/div/div[2]/h5[1]/div/div["+str(n2)+"]/div[1]").text
                    mod_size = self.driver.find_element(by=By.XPATH,value="/html/body/div/div/section/article/section[2]/section/section[3]/article[2]/div/div/div[4]/div["+str(n1)+"]/div[2]/div/div[2]/h5[1]/div/div["+str(n2)+"]/div[2]").text
                    mod = [mod_name,mod_size]
                    all_mod.append(mod)
                    
                    n2 = n2+1
                n2 = 1
                result = [item_name,type,item_comment,item_qty,all_mod]
            except Exception as e:
                result = [item_name,type,item_comment,item_qty]
            self.items.append(result)
            n1 = n1+1
        return self.items


    def get_info(self):
        
        sleep(5)
        self.order_id = self.driver.find_element(by=By.XPATH,value="/html/body/div/div/section/article/section[2]/section/section[3]/article[2]/div/div/div[2]/div").text.split("#")[1].split(" ")[1]
        #----------------------------------get phone number
        self.phone_number = self.driver.find_element(by=By.XPATH , value="/html/body/div/div/section/article/section[2]/section/section[3]/article[2]/div/div/div[2]/h2/div/div/a[1]").text
        #----------------------------------get name of customer
        self.cust_name = self.driver.find_element(by=By.XPATH,value="/html/body/div/div/section/article/section[2]/section/section[3]/article[2]/div/div/div[2]/h2/div/div/a[2]").text
        #----------------------------------get Adress
        address_elm = self.driver.find_element(by=By.CLASS_NAME,value="current_order_address")
        ui_labels = address_elm.find_elements(by=By.TAG_NAME,value="p")
        self.address = []
        for label in ui_labels :
            self.address.append(label.text)
        ########  discount     ########  payment_method  ########  total of order
        mony_info = self.driver.find_element(by=By.CLASS_NAME , value="lt-current-order-total")
        if len(mony_info.find_elements(by=By.TAG_NAME,value="li")) == 9 :
            discount_ = self.driver.find_element(by=By.XPATH,value="/html/body/div/div/section/article/section[2]/section/section[3]/article[2]/div/div/div[5]/ul/li[5]/span[2]").text  # discount 
            self.discount = discount_.replace("(-", " ").replace(")LE"," ")
            self.payment_method = self.driver.find_element(by=By.XPATH,value="/html/body/div/div/section/article/section[2]/section/section[3]/article[2]/div/div/div[5]/ul/li[8]/span[2]").text  #cash or credit
            #self.total = self.driver.find_element(by=By.XPATH,value="/html/body/div/div/section/article/section[2]/section/section[3]/article[2]/div/div/div[5]/ul/li[8]/span[2]").text.replace("LE","")
            total_ = self.driver.find_element(by=By.CLASS_NAME,value="total")
            ps = BeautifulSoup(total_.get_attribute("innerHTML"),"html.parser")
            self.total = ps.find("span" , class_="right").text.replace("LE","")
        
        else :
            self.discount = "0"
            self.payment_method = self.driver.find_element(by=By.XPATH,value="/html/body/div/div/section/article/section[2]/section/section[3]/article[2]/div/div/div[5]/ul/li[6]/span[2]").text
            #self.total = self.driver.find_element(by=By.XPATH,value="/html/body/div/div/section/article/section[2]/section/section[3]/article[2]/div/div/div[5]/ul/li[7]/span[2]").text.replace("LE","")
            total_ = self.driver.find_element(by=By.CLASS_NAME,value="total")
            ps = BeautifulSoup(total_.get_attribute("innerHTML"),"html.parser")
            self.total = ps.find("span" , class_="right").text.replace("LE","")

            
            


        self.info = [self.phone_number,self.cust_name+" menus",self.discount,self.payment_method,self.total,self.address]
        
        print(self.order_id)
        return self.info



"""
order = Operations_Menus()
input("--->")
order.driver.find_element(by=By.CLASS_NAME,value="ordercard-container__data").click()
order.get_info()
print(order.info)
order.get_items()
print(order.items)
sleep(100)

"""
