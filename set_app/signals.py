from django.db.models.signals import post_save

from set_app.models import Order, OrderItem, Inventory, Kardex
from django.dispatch import receiver


@receiver(post_save, sender=OrderItem)
def create_inventory(sender, instance, created, **kwargs):
	print('create_inventory called! ===========')
	if created:
		oi = instance
		o = oi.order
		order_type = o.order_type
		warehouse = o.warehouse
		customer = o.customer
		product = oi.product
		receiving_cust_id = o.receiving_customer_id
		n = 0
		n = oi.count
		print(oi.count)
		existing_row = Inventory.objects.filter(warehouse_id=warehouse.id, customer_id=customer.id, product_id=product.id)

		inv = Inventory()
		if existing_row.count() < 1:
			inv = Inventory(warehouse_id=warehouse.id, customer_id=customer.id, product_id=product.id, total=n)
			inv.save()
		elif existing_row.count() == 1:
			inv = existing_row.first()
			if order_type == 'IN':
				inv.total += n
			elif order_type == 'OU':
				inv.total -= n
			elif order_type == 'TR':
				existing_row2 = Inventory.objects.filter(warehouse_id=warehouse.id, customer_id=receiving_cust_id,
				                                         product_id=product.id)
				if existing_row2.count() < 1:
					inv2 = Inventory(warehouse_id=warehouse.id, customer_id=receiving_cust_id, product_id=product.id,
					                 count=n)
					inv2.save()
				elif existing_row.count() == 1:
					inv2 = existing_row2.first()
					inv2.total += n
					inv2.save(update_fields=['total'])
				else:
					ValueError('Inventory filter for existing_row2 should only match zero OR one row!')
				inv.total -= n
			else:
				ValueError('Order type should only match be IN, OU and TR!')
			inv.save(update_fields=['total'])
		else:
			ValueError('Inventory filter for existing_row should only match zero OR one row!')
		create_kardex(oi)


# post_save.connect(create_inventory, sender=Transaction)


@receiver(post_save, sender=Order)
def update_inventory(sender, instance, created, **kwargs):
	print('update_inventory called! ===========')
	if created == False:
		order = instance
		inv_list = Inventory.objects.all()
		if order.status == 'OFF':
			for order_item in order.orderitem_set.all():
				inv = inv_list.filter(warehouse=order.warehouse, customer=order.customer,
				                      product=order_item.product).first()
				print((inv))
				n = order_item.count
				if order.order_type == 'IN':
					inv.total -= n
				elif order.order_type == 'OU':
					inv.total += n
				elif order.order_type == 'TR':
					inv.total += n
					inv2 = inv_list.filter(warehouse=order.warehouse, customer=order.receiving_customer,
					                       product=order_item.product).first()
					inv2.total -= n
					inv2.save()
				inv.save()
				update_kardex(order_item)


def create_kardex(order_item):
	print('create_kardex called! ===========')
	if order_item.order.status == 'ON':
		kardex = Kardex()
		kardex.customer = order_item.order.customer
		kardex.product = order_item.product
		kardex.order_item = order_item
		if order_item.order.order_type == 'IN':
			kardex.change = order_item.count
		elif order_item.order.order_type == 'OU':
			kardex.change = -order_item.count
		elif order_item.order.order_type == 'TR':
			kardex.change = -order_item.count
			kardex2 = Kardex()
			kardex2.customer = order_item.order.receiving_customer
			kardex2.product = order_item.product
			kardex2.order_item = order_item
			kardex2.change = order_item.count
			kardex2.total = Inventory.objects.filter(warehouse=order_item.order.warehouse,
			                                         customer=order_item.order.receiving_customer,
			                                         product=order_item.product).first().total
			kardex2.save()
		kardex.total = Inventory.objects.filter(warehouse=order_item.order.warehouse,
		                                        customer=order_item.order.customer,
		                                        product=order_item.product).first().total
		kardex.save()

def update_kardex(order_item):
	print('update_kardex called! ===========')
	if order_item.order.status == 'OFF':
		kardex_list = Kardex.objects.filter(order_item=order_item)
		for kardex in kardex_list:
			print(kardex)
			print(order_item.order.invalidated)
			kardex.invalidated = order_item.order.invalidated
			print(kardex.invalidated)
			kardex.save(update_fields=['invalidated'])
			print(kardex)

