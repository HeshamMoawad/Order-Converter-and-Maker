from time import sleep
import Oms_Actions as oms
import Menus_Actions as mn
from Styles import style
import logging , time, requests



logging.basicConfig(level=logging.INFO,filename="Logs\logger.log",filemode="a",format="%(asctime)s:%(levelname)s:%(message)s",datefmt='%Y-%m-%d %H:%M:%S')
logging.basicConfig(level=logging.ERROR,filename="Logs\logger.log",filemode="a",format="%(asctime)s:%(levelname)s:%(message)s",datefmt='%Y-%m-%d %H:%M:%S')
style("","cls",5)
style("openning"," ", 5)

if oms.check_connection() == False:
    logging.warning("No Internet connection available")
else :
    logging.info("connected with internet")


logging.info("openinng browsers")


try:
    style("menus")
    order = mn.Operations_Menus()
    logging.info("Menus opened succesful")
    n = "y"
except Exception as e:
    logging.error(f"Menus : {e}")
    n = "n"
    style("error","cls" , 5)
    
if n =="y":
    try:
        style("oms")
        maker = oms.Operations_Oms("Data/DB.db")
        logging.info("Oms opened succesful")
        sleep(3)
        n = "y"    
    except Exception as e:
        logging.error(f"Oms : user already exist or Error in network connection : {e}")
        print("user already exist or Error in network connection")
        n = "n"
        style("error","cls",5)

try:   
    while n == "y" :
        order.order_new = False
        style("waiting"," ")
        while order.order_new == False :               
            order.accept_new_order()
        print(" while loop ended ------>")
        logging.info("Accept order")
        if order.order_status == True:
            t1 = time.time()
            style("collecting", " ")
            logging.info(f"Menus : collecting data")
            order.get_info()
            order.get_items()
            t2 = time.time()
            print(order.info)
            print(order.items)
            print(f"time of collecting data --> {t2-t1}")
            style("making" , " ")
            logging.info(f"Castumer Information : {order.info} Making order")
            maker.new_data_input(info=order.info)
            maker.search()
            maker.acounting()
            maker.prepare_order()
            logging.info(f"Oms : Preparing order")
            try:
                for item in order.items :
                    print(item)
                    maker.add_item(item=item)
                print("items done =====")
                style("sending")
                maker.send_order()
                t3 = time.time()
            except Exception as e:
                print(f"item add or Send order : {e}")
                logging.error(f"item add or Send order : {e}")
                maker.non_complete_order()

            print(f"{order.phone_number} : Order Completed --> take {t2-t1} to collect and {t3-t2} to making total time {t3-t1}")
            logging.info(f"{order.phone_number} : Order Completed --> take {t2-t1} to collect and {t3-t2} to making total time {t3-t1}")

            style("done", 3)
            print(f"time of making order --> {t3-t2}")
            print(f"total time --> {t3-t1}")
            
            sleep(5)
            maker.driver_oms.get("http://oms.nbegypt.com/Bk/Accounts/AllAccounts.aspx")
        print("----------------------------------------------------- main loop ----------------------------------------------")
        sleep(10)
except Exception as e:
    if oms.check_connection() == False:
        logging.warning("No Internet connection available")
    else :
        logging.info("connected with internet")
    logging.error(f"Main While loop : {e}")
    print(e)
    maker.exit()
    logging.error(f"succesful logged out ")
    


"""

def Installer():
    import os
    from time import sleep 
    os.system("cls")
    print("Start Install Requierments ")
    try :
        os.system("pip install -r Data/Requierments.txt")
        sleep(5)
        os.system("cls")
        print(" ----------------------------------> Done Installing ")
    except Exception as e:
        os.system("cls")
        print(e)
        print("--------------------------------------------------------------------------------------------")
        print("Error in Installer.py please back to Devoloper to solve this problem ")
        sleep(100)

"""



"""
['01114621650', 'aml menus', ' 30 ', 'CASH ON DELIVERY', ' 62.51', ['القاهرة', 'فيصل', 'المساحة', 'امتداد فلسطين - من خاتم المرسلين', '٩', '٥', '٣٣']

[['برجر مع الجبنة', 'ساندوتش', 'من غير خس', '1', []], ['تاور بيج كينج', 'وجبة وسط', 'من غير خس وبطاطس فريش وصوص الجبنة الزيادة من برا', '1']]

"""




