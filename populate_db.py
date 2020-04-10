import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', "SetWMS.settings")

import django

django.setup()

import random
from set_app.models import *
from faker import Faker

fakegen = Faker()
topics = ['Search', 'Social', 'Marketplace', 'News', 'Games']


def add_warehouse():
	wh = Warehouse()
	wh.name = 'Setayesh Warehouse انبار ستایش'
	wh.email = 'Setayesh.WH@gmail.com'
	wh.postcode = '1816157169'
	wh.address = 'تهران، کهریزک، جاده قدیم قم، نرسیده به سه راه سالمندان، جنب کوچه انبار مخابرات، پلاک ۱۱۶، انبار ستایش'
	wh.tel1 = '02156522996'
	wh.tel2 = '02156539387'
	wh.save()
	return wh


def add_customers(wh, N=10):

	cust_list = []

	st_strings = ['sule', 'yard', 'container 1', 'container 2', 'container 3', 'shop 1', 'shop 2', 'shop 3']

	for n in range(N):
		cust = Customer()
		cust.entity_type = random.choices(['IN', 'CO'],k=1)[0]
		cust.first_name = fakegen.first_name()
		cust.last_name = fakegen.last_name()
		cust.company_name = fakegen.company()
		cust.melli_code = '0071982787'
		cust.tel1 = fakegen.phone_number()
		cust.tel2 = fakegen.phone_number()
		cust.email = fakegen.ascii_company_email()
		cust.address = fakegen.address()
		cust.postcode = fakegen.postcode()
		cust.save()
		for i in range(4):
			st = StorageTag(name=random.choices(st_strings, k=1)[0])
			st.save()
			cust.storage_tags.add(st)
		cust.warehouse = wh
		cust_list.append(cust)

	return cust_list


def add_products(N=10):
	prod_list = []

	name_strings = ['Macbook 13 inch', 'Galaxy S8', 'Golf GTI 2020', 'Gold Mine WA', 'Asprin TM',
	                'Soccer Shoes Model X', 'TV UHD 40 inch', 'Gas water boiler', 'Prius', 'Spray can 500 ml']
	brand_strings = ['Apple', 'Samsung', 'Volkswagon', 'Riotinto', 'Bayer', 'Adidas', 'Sony', 'Butan', 'Toyota', 'WD-40']

	for n in range(N):
		prod = Product()
		prod.code = fakegen.ean(length=8)
		prod.barcode = fakegen.ean13()
		prod.name = name_strings[n]
		prod.description = "some description " + n.__str__()
		prod.brand = brand_strings[n]
		if N%2==0:
			prod.status = 'ON'
		else:
			prod.status = 'OF'
		prod.save()
		prod_list.append(prod)

	return prod_list

def	add_order(wh,cust_list,prod_list,N=10):

	for n in range(N):
		order_in = Order()
		order_in.order_type = 'IN'
		order_in.sys_order_no = n+1
		order_in.warehouse = wh
		order_in.customer = cust_list[n]
		order_in.permit_type = random.choices(['PAP', 'FAX', 'EMA', 'TEL'], k=1)[0]
		order_in.permit_number = random.randrange(500000,950000)
		order_in.notes = fakegen.text(30)
		order_in.origin_destination = random.choices(['Tehran', 'Shiraz', 'Isfahan', 'Yazd', 'Qom', 'Sari', 'Ahvaz', 'Semnan', 'Tabriz', 'Saveh'], k=1)[0]
		order_in.billway_number = random.randrange(10000,50000)
		order_in.transport_company = random.choices(['Neginbar', 'Savadbar', 'Shahinbar', 'Sepehrbar', 'Javid Tarabar'], k=1)[0]
		order_in.sender_receiver = fakegen.company()
		#receiving_customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, related_name='receiving_customer')  # used only for transfer
		order_in.driver = add_driver()
		order_in.save()
		for i in range(5):
			trans = Transaction()
			trans.order = order_in
			trans.product = prod_list[i]
			trans.count = random.randrange(100,200)
			trans.save()

	for n in range(N):
		order_in = Order()
		order_in.order_type = 'OU'
		order_in.sys_order_no = n+1
		order_in.warehouse = wh
		order_in.customer = cust_list[n]
		order_in.permit_type = random.choices(['PAP', 'FAX', 'EMA', 'TEL'], k=1)[0]
		order_in.permit_number = random.randrange(500000, 950000)
		order_in.notes = fakegen.text(30)
		order_in.origin_destination = random.choices(['Tehran', 'Shiraz', 'Isfahan', 'Yazd', 'Qom', 'Sari', 'Ahvaz', 'Semnan', 'Tabriz', 'Saveh'], k=1)[0]
		order_in.billway_number = random.randrange(10000, 50000)
		order_in.transport_company = random.choices(['Neginbar', 'Savadbar', 'Shahinbar', 'Sepehrbar', 'Javid Tarabar'], k=1)[0]
		order_in.sender_receiver = fakegen.company()
		# receiving_customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, related_name='receiving_customer')  # used only for transfer
		order_in.driver = add_driver()
		order_in.save()
		for i in range(5):
			trans = Transaction()
			trans.order = order_in
			trans.product = prod_list[i]
			trans.count = random.randrange(20, 50)
			trans.save()

	for n in range(5):
		order_in = Order()
		order_in.order_type = 'TR'
		order_in.sys_order_no = n+1
		order_in.warehouse = wh
		order_in.customer = cust_list[n]
		order_in.permit_type = random.choices(['PAP', 'FAX', 'EMA', 'TEL'], k=1)[0]
		order_in.permit_number = random.randrange(500000, 950000)
		order_in.notes = fakegen.text(30)
		order_in.origin_destination = random.choices(['Tehran', 'Shiraz', 'Isfahan', 'Yazd', 'Qom', 'Sari', 'Ahvaz', 'Semnan', 'Tabriz', 'Saveh'], k=1)[0]
		order_in.billway_number = random.randrange(10000, 50000)
		order_in.transport_company = random.choices(['Neginbar', 'Savadbar', 'Shahinbar', 'Sepehrbar', 'Javid Tarabar'], k=1)[0]
		order_in.sender_receiver = fakegen.company()
		order_in.receiving_customer = cust_list[n+1]
		print('order_in.receiving_customer_id = ' + order_in.receiving_customer_id.__str__())
		# receiving_customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, related_name='receiving_customer')  # used only for transfer
		order_in.driver = add_driver()
		order_in.save()
		for i in range(2):
			trans = Transaction()
			trans.order = order_in
			trans.product = prod_list[i]
			trans.count = random.randrange(10, 20)
			trans.save()


def add_driver():
	driver = Driver()
	driver.melli_code = '1189144549'
	driver.first_name = fakegen.first_name()
	driver.last_name = fakegen.last_name()
	driver.driver_code = random.randrange(80000,89999)
	driver.tel1 = fakegen.phone_number()
	driver.number_plate_1 = random.randrange(100,999)
	driver.number_plate_letter = random.choices(['ع','غ','ف','ک','گ','ل','م','ن','و','ه','ی'],k=1)[0]
	driver.number_plate_2 = random.randrange(10,99)
	driver.number_plate_iran = random.randrange(10,99)
	driver.truck_size = random.choices(['MOT','CAR','VAN','NIS','ISU','KHA','BUD','TAK','JOF','20F','40F','40H','FBT','SRT','TRT'],k=1)[0]
	driver.save()
	return driver

# def add_topic():
# 	t = Topic.objects.get_or_create(top_name=random.choice(topics))[0]
# 	t.save()
# 	return t


# def populate(N=5):
# 	for entry in range(N):
# 		top = add_topic()
#
# 		fake_url = fakegen.url()
# 		fake_date = fakegen.date()
# 		fake_name = fakegen.company()
#
# 		webpg = Webpage.objects.get_or_create(topic=top, url=fake_url, name=fake_name)[0]
#
# 		acc_rec = AccessRecord.objects.get_or_create(name=webpg, date=fake_date)[0]


if __name__ == '__main__':
	print("populating script started!")
	wh = Warehouse()
	if Warehouse.objects.count() == 0:
		wh = add_warehouse()
	else:
		wh = Warehouse.objects.first()

	cust_list = []
	if Customer.objects.count() == 0:
		cust_list = add_customers(wh,10)
	else:
		cust_list = Customer.objects.all()

	prod_list = []
	if Product.objects.count() == 0:
		prod_list = add_products(10)
	else:
		prod_list = Product.objects.all()

	if Order.objects.count() == 0:
		add_order(wh,cust_list,prod_list,10)

	print("populating complete!")
