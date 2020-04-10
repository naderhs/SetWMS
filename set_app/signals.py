from django.db.models.signals import post_save

from set_app.models import Transaction, Inventory
from django.dispatch import receiver

@receiver(post_save, sender=Transaction)
def create_inventory(sender, instance, created, **kwargs):

# warehouse, customer, product, count
	t = instance
	o = t.order
	order_type = o.order_type
	warehouse = o.warehouse
	customer = o.customer
	product = t.product
	receiving_cust_id = o.receiving_customer_id
	n = 0
	n = t.count
	print(t.count)
	existing_row = Inventory.objects.filter(warehouse_id=warehouse.id, customer_id=customer.id,product_id=product.id)

	inv = Inventory()
	if existing_row.count() < 1:
		inv = Inventory(warehouse_id=warehouse.id, customer_id=customer.id,product_id=product.id, count=n)
		inv.save()
	elif existing_row.count() == 1:
		inv = existing_row.first()
		if order_type == 'IN':
			inv.count += n
		elif order_type == 'OU':
			inv.count -= n
		elif order_type == 'TR':
			existing_row2 = Inventory.objects.filter(warehouse_id=warehouse.id, customer_id=receiving_cust_id,
			                                         product_id=product.id)
			inv2 = existing_row2.first()
			inv.count -= n
			inv2.count += n
			inv2.save(update_fields=['count'])
		else:
			ValueError('Order type should only match be IN, OU and TR!')
		inv.save(update_fields=['count'])
	else:
		ValueError('Inventory filter should only match zero OR one row!')

# post_save.connect(create_inventory, sender=Transaction)


@receiver(post_save, sender=Transaction)
def update_inventory(sender, instance, created, **kwargs):
	if created == False:
		print('update_inventory called! ===========')

# post_save.connect(update_inventory, sender=Transaction)
