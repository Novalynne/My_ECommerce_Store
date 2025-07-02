# My-E-Commerce-Store
This project is for PPM Course.<br>
A complete web application must be developed. Take care
of the dynamic aspect of a website.

The backend must contain at least: <br>
<ul>
<li> 2 different app</li>
<li> 2 relations between model tables</li>
<li> 1 view must use Class-generics</li>
<li> 2 different permission for two groups of users</li>
<li> User class must be extended and customized</li>
</ul>


**E-commerce Store:** Build an ecommerce store with product listings, shopping cart
functionality, and order management. The model complexity can include defining relationships
between products, categories, and user orders. The view logic can involve handling product
searches, adding items to the cart, and processing orders. The template complexity can be
reduced by using CSS frameworks like Bootstrap to style the store. Store managers (a
second user group) will be able to manage products, categories, and orders.

## Link to the project
[My-E-Commerce-Store](https://myecommercestore-production.up.railway.app/)

Manager account: 
- **Username:** manager 
- **Password:** managerthegratest<br>

Admin account: 
- **Username:** admin 
- **Password:** admin<br>

## Features
This project is a complete e-commerce website that allows users to browse products, manage their accounts, and place orders. It includes functionalities for both customers and store managers, ensuring a comprehensive shopping experience.

There are three types of users: customers, store managers and admin. 

Customers can manage their accounts, manage their cart, and place orders. They can also view their order history and favorite products.
Store managers can manage products, categories, and view all orders placed by customers.
Admin is like a manager with the ability to make more managers, he can do everything a manager can plus manage users.

MyStore is a button that will take you to the front page if you are not loggen in, or will take you to the home page if you are loggen in.

Here I'll go more into the details of the features and functionalities of the e-commerce store.

## Features Overview
- **User Management**: Users can register, log in, and manage their profiles. Such as updating personal information and changing passwords. If a user deletes their account, all their data will be deleted, including their cart, but not their orders. If a user forgets their password they can reset it using their email and username.

- **Product Management**: Store managers can add, edit, and delete products. They can also manage product categories, deleting or adding categories as needed. Every product has a stock quantity and a price/sale price that can be changed by the manager at all times. If a product is deleted, all carts that contain that product will have it removed from the cart, orders will not be deleted. If a product is out of stock, it will not be available for purchase, and the manager can update the stock quantity when new stock arrives.

- **Product Browsing**: Customers and Managers can browse products by category, search for specific products, and view product details. Products are displayed with their images, descriptions, prices, and stock availability.

- **Shopping Cart**: Customers can add products to their shopping cart, view the cart, and update quantities or remove items. In the cart you can then check out and place an order. The checkout button will check if all the products in the cart have available stock for the order. The cart itself will display if an item is out of stock.

- **Wishlist**: Customers can add products to their wishlist for future reference. They can view and manage their wishlist items.

- **Payment Processing**: Customers can place orders and make payments. The payment process is for the sake of this project just a form, it doesn't do any bank transactions. To simulate a payment I made it so everytime the client tries to pay (clicking the "Make Order" button) a random number will be generated and checked with the total of the order, if the money generated is sufficient the order will go through, otherwise the operation will be cancelled and an error message will pop up in the cart view. NOTE: This button also checks for the stock of each item and quantity in the order ensuring that at the time of the order there is enough stock to cover the order.

- **Order Management**: Customers can view their order history, and Managers can view all orders placed by customers. Orders have 4 different state "in the making", "shipped", "arrived", "returned". While the order is in the making state the Customer can cancel the order. The Manager can change the state of the order from "in the making" to "shipped". A shipped order automatically changes to "arrived" after 5 minutes from its shipping date, and the Customer can return it for 5 minutes after it has arrived. Managers can view the details and reasons for returned orders. NOTE: 5 minutes is just a simulation of time,.

- **Admin Features**: Admin can promote users to store managers, allowing them to manage products and orders. He can also demote managers back to customers. He can also do anything a manager can do, such as managing products, categories, and orders.