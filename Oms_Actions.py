########################################
from time import sleep
import requests
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select
import pandas as pd
import sqlite3 as sq
########################################


#
#
#
#                
#
#            
#
#

class Operations_Oms():
    def __init__(self,relative_path) -> None:
        global con
        con = sq.connect(relative_path)
        
       
        from webdriver_manager.chrome import ChromeDriverManager
        self.driver_oms = webdriver.Chrome(ChromeDriverManager().install())
            
        print("Opened with Dynamic Webdriver")
        self.driver_oms.maximize_window()
        self.user = "------"   #enter User name of oms
        self.password = "--------"  #enter password name of oms
        self.driver_oms.get("http://oms.nbegypt.com/Bk/General/Login.aspx")
        self.driver_oms.find_element(by=By.ID ,value="tbUsername").send_keys(self.user)
        self.driver_oms.find_element(by=By.ID,value="tbPassword").send_keys(self.password)
        self.driver_oms.find_element(by=By.ID,value="btnSubmit").click()
        self.wait_o(3)
        self.driver_oms.find_element(by=By.ID,value="xlblMainMenu")
        self.driver_oms.get("http://oms.nbegypt.com/Bk/Accounts/AllAccounts.aspx")
        super().__init__()

    def wait_o(self,sec):
        self.driver_oms.implicitly_wait(sec)

    def handling(self,to="main" or "sec"):
        if to == "main":
            handles = list(self.driver_oms.window_handles)
            handle_secondary  = self.driver_oms.current_window_handle
            if handle_secondary == handles[1]:
                handle_main = handles[0]
            elif handle_secondary == handles[0]:
                handle_main = handles[1]
            self.driver_oms.switch_to.window(handle_main)
        elif to == "sec":
            handles = list(self.driver_oms.window_handles)
            handle_main  = self.driver_oms.current_window_handle
            handle_secondary = handles[1]
            self.driver_oms.switch_to.window(handle_secondary)
        

        
        pass

    def new_data_input (self, info): ############## Done
        self.address = info[5]
        self.phone_num = info[0]
        self.name_of_castomer = info[1]
        self.discount = info[2]
        self.payment_method =info[3]
        self.total_order = info[4]
        
    
        
    def add_phone_num_in_contact (self): ########## Done
        self.driver_oms.find_element(by=By.ID,value="btnAddPhones").click()
        self.handling("sec")
        type_phone = self.driver_oms.find_element(by=By.ID,value="dlType")
        slct_type = Select(type_phone)
        slct_type.select_by_index(2)
        self.driver_oms.find_element(by=By.ID,value="tbNumber").send_keys(self.phone_num)
        self.driver_oms.find_element(by=By.ID,value="btnSave").click()
        self.handling("main")

    def other_drops(self):
        self.driver_oms.find_element(by=By.ID, value="xlblNotes").click()
        self.driver_oms.find_element(by=By.ID,value="tbArea").send_keys(self.address[1] + " "+ self.address[2]) ######### Area
        self.driver_oms.find_element(by=By.ID,value="tbStreet").send_keys(self.address[3]) ######### street
        self.driver_oms.find_element(by=By.ID,value="tbBuilding").send_keys(self.address[6])######### Building number
        self.driver_oms.find_element(by=By.ID,value="tbFloor").send_keys(self.address[5])############# Floor
        self.driver_oms.find_element(by=By.ID,value="tbFlat").send_keys(self.address[4])############# Flat


    def creat_acc(self):################### Done
        self.driver_oms.find_element(by=By.ID, value="btnAdd").click()
        home_sel = self.driver_oms.find_element(by=By.ID,value="dlType")
        selection = Select(home_sel)
        selection.select_by_index(2)
        self.driver_oms.find_element(by=By.ID,value="tbName").send_keys(self.name_of_castomer)
        self.driver_oms.find_element(by=By.ID,value="xlblNotes").click()
        try:
            self.drop_sub_dist(self.address[2])
        except :
            try:
                self.drop_sub_dist(self.address[1])
            except:
                try:
                    self.drop_sub_dist(self.address[1].replace("ي","ى"))
                except:
                    print(" $$$$  Error in Address ")
                    input("Please enter the correct address -----  After complete please Press Enter Key ->  ")
                    
        num_type = self.driver_oms.find_element(by=By.ID , value="dlPType")
        selection3= Select(num_type)
        selection3.select_by_index(1)
        self.other_drops()
        self.driver_oms.find_element(by=By.ID,value="tbNumber").send_keys(self.phone_num)############# phone number
        self.driver_oms.find_element(by=By.ID,value="xdlBrands_ctl00_btnBrand").click()


    def check_adrs_in_acc (self): ################# Done
        try:
            parent = self.driver_oms.find_element(by=By.ID,value="xdgAddresses")
            f_address = parent.find_elements(by=By.CLASS_NAME,value="aspDGLine1")
            if len(f_address) == 1 :
                
                building_num = self.driver_oms.find_element(by=By.XPATH,value="/html/body/form/table/tbody/tr[4]/td[2]/table[5]/tbody/tr/td[2]/div/table/tbody/tr[2]/td[9]").text
                
                if building_num == self.address[6]:
                    
                    self.address_id = 0
                else:
                    try:
                        sec_address = parent.find_elements(by=By.CLASS_NAME,value="aspDGLine2")
                        len_adrs = len(f_address) + len(sec_address)
                        for i in range(len_adrs):
                            building_num = self.driver_oms.find_element(by=By.XPATH,value="/html/body/form/table/tbody/tr[4]/td[2]/table[5]/tbody/tr/td[2]/div/table/tbody/tr["+str(i+1)+"]/td[9]").text
                            if building_num == self.address[6]:
                                self.address_id = i-1
                                return self.address_id
                    except NoSuchElementException:
                        self.add_address_in_acc()
                        self.address_id = 0
        except NoSuchElementException :
            self.add_address_in_acc()
            self.address_id = 0
        self.cast_status = "address is already exist in account"
        return self.address_id 


    def drop_sub_dist (self,sub): ################# Done
        self.driver_oms.find_element(by=By.ID,value="xtbSearch").clear()
        self.driver_oms.find_element(by=By.ID,value="xtbSearch").send_keys(sub)#######  sub district
        self.driver_oms.find_element(by=By.ID,value="btnSearchStreetStart").click()
        city_elm = self.driver_oms.find_element(by=By.ID , value="dlCity")
        selection1 = Select(city_elm)
        try:
            selection1.select_by_visible_text(self.address[0])
        except:
            selection1.select_by_index(1)
        self.driver_oms.find_element(by=By.ID, value="xlblNotes").click()
        sleep(3)
        dist_elm = self.driver_oms.find_element(by=By.ID ,value="dlDistrict")
        selection2 = Select(dist_elm)
        try:
            selection2.select_by_value(self.address[1])
        except:
            selection2.select_by_index(1)
        pass
               


    def add_address_in_acc (self): ################ Done
        try:
            self.driver_oms.find_element(by=By.ID,value="btnAddAddresses").click()
            self.handling("sec")
            try:
                self.drop_sub_dist(self.address[2])
            except :
                try:
                    self.drop_sub_dist(self.address[1])
                except:
                    try:
                        self.drop_sub_dist(self.address[1].replace("ي","ى"))
                    except:
                        print(" $$$$  Error in Address ")
                        input("Please enter the correct address -----  After complete please Press Enter Key ->  ")
            self.other_drops()
            self.driver_oms.find_element(by=By.ID,value="btnSave").click()
            self.handling("main")
        except NoSuchElementException :
            print("there are error in add address in account")    
    
    def search (self):  ########################## Done
        self.driver_oms.find_element(by=By.ID,value="tbPhone").send_keys(self.phone_num)
        self.driver_oms.find_element(by=By.ID,value="btnSearchStart").click()
        self.driver_oms.implicitly_wait(3)
        try :
            self.driver_oms.find_element(by=By.CLASS_NAME,value="aspDGLine1")
            self.user_status = True 
        except NoSuchElementException :
            self.user_status = False
        return self.user_status



    def acounting(self):  ####################### Done
        if self.user_status == False :
            self.creat_acc()
            self.address_id = 0
            self.cast_status = "created new account"
            
        else :
            self.driver_oms.find_element(by=By.ID,value="xdgAccounts_ctl03_xdgAccountsEdit").click()
            self.check_adrs_in_acc()
            self.address_id = self.address_id
            self.driver_oms.find_element(by=By.ID,value="xdgContacts_ctl03_xdgContactsEdit").click()
            try :
                elms = self.driver_oms.find_element(by=By.ID , value="xdgPhones")
                elms.find_element(by=By.CLASS_NAME , value="aspDGLine1")
            except NoSuchElementException :
                self.add_phone_num_in_contact()
                self.cast_status = self.cast_status + " and add phone number in contact"
                
            brand_elm = self.driver_oms.find_element(by=By.ID,value="xdlBrands")
            selection = Select(brand_elm).select_by_visible_text("Burger King")
            self.driver_oms.find_element(by=By.ID,value="btnAddOrders").click()
            return "user already exist"
        

    

    def prepare_order (self):  ################## done
        try:
            self.driver_oms.find_element(by=By.ID,value="rlAddresses_ID_"+str(self.address_id)).click()
        except NoSuchElementException :
            print("there are Error on address_id ")
        source_elm = self.driver_oms.find_element(by=By.ID,value="dlOrderSource")
        selct_source = Select(source_elm)
        selct_source.select_by_visible_text("EL MENUES")
        self.driver_oms.find_element(by=By.ID,value="cbDiscountOtlob").click()
        fixed_elm = self.driver_oms.find_element(by=By.ID,value="dlOtlobType")
        selct_dis = Select(fixed_elm).select_by_visible_text("Fixed")
        try :
            self.driver_oms.find_element(by=By.ID,value="tbOtlobNumber").send_keys(int(self.discount)*(14/100)+int(self.discount))
        except NoSuchElementException :
            print("error discount")

        note = self.driver_oms.find_element(by=By.NAME,value="tbNotes")
        note.send_keys(f"Discount(-{self.discount})LE \n") # discount in note
        
        self.df = pd.read_sql_query("SELECT * from items", con)
        self.driver_oms.find_element(by=By.NAME,value="tbHiddenComment").send_keys("مينيوز") # category in hidden comment
        if self.payment_method == "CREDIT CARD":
            note.send_keys("Credit")
            print("credit")
            self.driver_oms.find_element(by=By.ID,value="cbCredit").click()
        elif self.payment_method == "CASH ON DELIVERY" :
            note.send_keys("Cash")
            print("cash")
        self.driver_oms.find_element(by=By.ID,value="btnAddItems").click()
        self.handling("sec")
        
        
    def send_order (self):  ################## done
        self.wait_o(10)
        self.driver_oms.close()
        self.driver_oms.switch_to.window(self.driver_oms.window_handles[0])
        self.driver_oms.find_element(by=By.ID,value="btnSave").click()       #save order
        #self.driver_oms.find_element(by=By.ID,value="btnActivate").click()       #send order
        #self.driver_oms.switch_to.alert.accept()
        print("done")
        

    def add_item(self,item): ################# done
        """
        item must be list
        item = [name,type,comment,qty,[all modefire with length 2]]
        """
        df = self.df
        if item[1] == "مع لعبة":
            item_type = item[1]
        else :
            item_type = str(item[1]).split(" ")[0]
        df1 = df[(df["item_menus"]==item[0]) & (df["type_ar"]==item_type)]
        if item[2] == "no comment":
            pass
        else :
            self.driver_oms.find_element(by=By.NAME,value="tbMainComments").send_keys(item[2]) #comment
        qty = self.driver_oms.find_element(by=By.NAME,value="tbMainQuantity")
        qty.send_keys(Keys.BACK_SPACE)
        qty.send_keys(int(item[3]))  
        type_elm = self.driver_oms.find_element(by=By.NAME,value="dlSection_ID")
        type_sel = Select(type_elm)
        print(df1.iloc[:,2].values[0])
        type_sel.select_by_visible_text(df1.iloc[0,2])
        print("category selected")
        self.wait_o(5)
        #   selection Item
        item_elm = self.driver_oms.find_element(by=By.NAME,value="dlItem_ID")   
        item_sel = Select(item_elm)
        print(df1.iloc[:,3].values[0])
        try:
            item_sel.select_by_visible_text(df1.iloc[0,3])
        except :
            item_sel.select_by_value(int(df1.iloc[0,5]))
        print("item selected")
        if len(item) > 4 :
            print("modefireing")
            modefire = item[4]
            for i in modefire :
                print(i)
                if i[1] == "وجبة وسط" :
                    df2 = df[(df["item_menus"]==i[0])&(df["type_en"]=="Drink")]
                    print(df2)
                    self.driver_oms.find_element(by=By.ID,value=df2.iloc[0,6]).click() # drink with meal

                elif i[1] == "وجبة كبيرة" :
                    df2 = df[(df["item_menus"]==i[0])&(df["type_en"]=="Drink")]
                    print(df2)
                    self.driver_oms.find_element(by=By.ID,value=df2.iloc[0,6]).click() # drink with meal
                    self.driver_oms.find_element(by=By.ID,value="xrpMainMenu_ctl02_xdgSubMenu_ctl02_xbtnAddQuantitySub").click() # large
                
                else :
                    df2 = df[(df["item_menus"]==i[0])&(df["type_ar"]==i[1])]
                    print(df2)
                    if item_type == "مع لعبة":
                        self.driver_oms.find_element(by=By.ID,value=df2.iloc[0,7]).click() # drink with kids meal
                    else:
                        self.driver_oms.find_element(by=By.ID,value=df2.iloc[0,6]).click() # go items or extra  
        else :
            print("no modefire")
        self.driver_oms.find_element(by=By.ID,value="btnSave").click() #save item
        self.wait_o(5)
        self.driver_oms.switch_to.alert.accept()
        self.wait_o(5)
        
        
        
            
    
        



    def non_complete_order (self):
        self.driver_oms.find_element(by=By.ID,value="btnCancel").click()
            
        




    def exit(self):
        self.driver_oms.get("http://oms.nbegypt.com/Bk/General/Logout.aspx")
        con.close()
        sleep(2)
        self.driver_oms.close()
        self.driver_oms.quit()
        return "Logged out"



def check_connection(host='http://google.com'):
        try:
            requests.get(host)
            status = True
        except Exception as e:
            print(e)
            status = False
        return status

"""
def tt():

    maker = Operations_Oms("Data/DB.db")
    data = input("--------> ")
    items = input("-------->")
    maker.new_data_input(info=data)
    maker.search()
    maker.acounting()
    maker.prepare_order()

    for item in items :
        print(item)
        maker.add_item(item=item)
    maker.send_order()
    sleep(10)
    maker.exit()

"""

