# InventoryManagementSystem
A software developed using Java SE which provides as easy way to track the products, suppliers, customers as well as purchase and
sales information. It also records the stock currently available in the store. 
  There are basically two users, Administrator and Normal User. Both the users can manage suppliers, products, customers and purchase and sell products.
  The only difference between the two users is that the administrator can also view sales report and can also manage other users.

Download .sql file for this application: https://drive.google.com/file/d/0Bw-qNYNSGhdCN09YZDV6SmtRN00/view?usp=sharing&resourcekey=0-g98Gi5ErSgzV-Jit-4Ow6Q

Download required third party plugins (includes JCalender, JTattoo and SQLConnector) : https://drive.google.com/file/d/0Bw-qNYNSGhdCMU1mekN4SmRCb1E/view?usp=sharing&resourcekey=0-mynFCWwHM0l7oUuBwDIVbw

Download the software only: https://drive.google.com/file/d/0Bw-qNYNSGhdCbVdSdzZHX0pZOFE/view?usp=sharing&resourcekey=0-Q9wY-we5-vgs26YpPMrYaQ

Download full documentation for free: 
- https://www.scribd.com/doc/296989740/InventoryManagementSystem-Sajan-Rajbhandari  
- [Inventory-Management-System-Sajan-Rajbhandari.pdf](https://github.com/sazanrjb/InventoryManagementSystem/blob/master/docs/Inventory-Management-System-Sajan-Rajbhandari.pdf)

Credentials:

After importing the above sql file and adding the plugins, try using the credential username: `user4` and password: `test123`

Also make sure your mysql is username: `root` and password: `root`. If not change the credential in `../ims/src/com/inventory/database/ConnectionFactory.java` line no. 36 and 44.
