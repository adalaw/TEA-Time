# Description

This is a customer-use and staff-use website for a tea shop “TEA Time”.

There is an order page for both customers and staff to order teas. Customers not only can make orders in the store, but also can pre-order their drinks by smartphones before they arrive. After they ordered online, they can either show the confirmation page or confirm email to finish payment and take their ordered items.

For management, there is an admin system including order management, product management and sales report. Staff can only be added to be user by superuser(s) instead of register themselves. After their account is activated, they can make order for walk-in customers, help pre-ordered customers checking their orders by scanning their order QR code, and sales summary.

# Content of each file

App name: main

urls.py – All paths in the app.

models.py – All models in the app: User, Category, Product, Customer, Order, OrderItem. 

filters.py – This is for easier searching from a brunch of information from database. There are ProductFilter for searching product, OrderFilter for searching store and its related orders, and ReportFilter for searching sales summary of each store and different period.

forms.py – There are CategoryForm for adding new category to Category, ProductForm for adding new product to Product, OrderForm for customers add store to Order and customers’ info to Customer, StaffOrderForm for staff to add walked-in orders’ info to Order.

admin.py – All settings about displaying models’ fields.

Folder: templates

Sub-folder: main

layout.html – For overall pages design. In staff account, there is a navbar, which is different from customers’ view.

index.html – This is the ordering page.

checkout.html – After adding order, users will be able to double check their order on this page by clicking checkout button on the ordering page.

confirm.html – By clicking confirm button on the checkout page, users will be taken to this page to see the confirmation.

email.html – This is the template of system-generated email sending to the customers who ordered online. It will show the order number, order timestamp, each ordered item, total items and total amount for checking and finishing payment.

Sub-folder: staff

login.html – Staff need to type the exact path to this page to login.

category.html – Staff can see all categories and add a new one on this page.

edit_category.html – By clicking edit button of the category in “category.html”, staff will be taken to the related category page to update its pre-filled form.

new_product.html – Staff can add new product on this page.

manage_products.html – All products are displayed here. Staff can also do filter searching here.

edit_product.html – By clicking edit button of the product in “manage_products.html”, staff will be taken to the related product page to update its pre-filled form.

manage_orders.html – Staff can check orders here and do some changes about them.

report.html – This is for checking sales quantity and amount for the company and each store. Staff can check for monthly and yearly statistics by adjusting the filter.

Folder: static

Sub-folder: css
main.css – Styling for templates inside “main” folder.
staff.css – Styling for templates inside “staff” folder.

Sub-folder: images
Company’s logo and images uploaded by staff are put inside this folder.

Sub-folder: js
main.js – Interacted functions for templates inside “main” folder, including toggle the series panels and counting the total items and amount.
staff.js – Interacted functions for templates inside “staff” folder, including changing the status of orders.

# Distinctiveness

Food-ordering is something that I haven’t created so I choose this type of website. This project is distinct from Project 2 as following reasons:

(a)	This system is also for staff to run and manage the business at the store, not only for online buyers. And therefore, customers do not have to register an online account. They can also shop at store.
(b)	In this project, customers can choose more than one item at the same order, which is make sense for ordering drinks, instead of get only one product item in one auction.
(c)	And therefore, in this project, we have to count total items and amount of each orders.
(d)	Rather than just getting success messages on the website, in this project, customers who order online, will get a system-generated email with a QR code of the order number for confirmation.
(e)	At the back-end of this project, staff have to manage orders. If order items are ready and delivered to customers, they have to change the order status by themselves. Besides, there is sales report for staff to manage the store accounting. On the other hand, there is no management site in Project 2.

# Complexity

This project contains front-end and back-end functions, which has more than one Django model and JavaScript on the both sites, as required. Customers are be able to order online and check their orders by system-generated emails. As staff, they can also use the order page to run business at the store. They can also manipulate categories, products and orders with the system, and review business of the store(s). To conclude, it is a full-stack development.

# Additional information

For security reason, the “EMAIL_HOST_PASSWORD” which in .env is replaced by “***”.
