from src.driver_obj import Driver

if __name__ == "__main__":
    driver = Driver()
    driver.get_driver("Windows")
    driver.d.get("https://www.baidu.com")
    driver.save_pdf('demo.pdf')
    driver.close()
    print("SUCCESS")

