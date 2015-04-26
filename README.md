django-notify
=============

Trigger notification emails via HTTP. Useful for hosts that can't send
mail on their own.


Protocol example
----------------

1. client requests challenge: `GET /notify/<username>`
2. server responds with challenge
3. client posts notification:
   
   ```
   POST /notify/<challenge>
   {
       "message": "<message>",
       "subject". "<subject>",
       "mac": hmac_sha512(subject + message, challenge + key)
   }
   ```

The key is used to prevent spam, the challenge to prevent replay attacks.


Deployment and Configuration
----------------------------

* Place `notify`, but not `notify.py` (the client), in your Django project directory.
* Django settings: add `notify` to `INSTALLED_APPS`, set `NOTIFY_FROM` to your preferred sender email address
* Run `syncdb` etc.
* In the admin backend, add a destination (and thus key) for each client
* On the client side, run client once to create a config file, then paste username, key and URL prefix into it.


Client usage
------------

```
$ echo "Message content" | python notify.py This is the subject
```


Warning
-------

The client explicitly ignores SSL certificates, see `make_sslctx()`.
