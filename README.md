# Test tasks made by @heaviss

### The bookstore

> Implement a simple bookstore.
> If the user has an active subscription, he can view the book.
There is a two-week trial period on registration. 
> Then the user can buy a subscription for a month or a year. 
> 
> API methods:
> - POST create new user (the simplest manual creation, no need to bother with registration)
> - GET list of users
> - GET retrieve user
> - POST pass the payment to the user (incoming data is `{'user_id': '', status: 'ok', 'period': 'month/year'}` or `{'user_id': '', status: 'error', 'msg': ''}`)
> - GET list of books to the user (subscription is not needed for that)
> - GET retrieve detailed information about a certain book (subscription is required)
>
> Stack: python 3, django, drf
