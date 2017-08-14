# SPAforum

SPAforum is a forum application built in Single-page application approach. It uses Python 3.4.x with Django REST framework in back-end and AngularJS in front-end.

Frameworks used in the project:
- [Django] (1.11)
- [Django REST framework] (3.6.2)
- [AngularJS] (1.5.8)
- [Bootstrap 3] (3.3.7)

Other Python/Django libraries used in the project:
- [REST framework JWT Auth] (1.10.0)
- [django-modeladmin-reorder] (0.2)
- [django-admin-sortable2] (0.6.10)

Other external AngularJS  libraries used in the project:
- [dirPagination.js] (0.11.1)
- [angular-elastic] (2.5.1)

***

## Installation
<p>To run SPAforum locally, first setup and activate virtual environment for it and then:</p>
<br />

__1. Install requirements using pip:__
```shell
pip3 install -r requirements.txt
```
<br />

__2. Make migrations:__
```shell
python3 manage.py makemigrations
```
__Warning:__ If you are planning to make changes to the forum model (`SPAforum/forum/models.py`) before the first `makemigrations` command, you need to:
- Remove the `0001_initial.py` file (`SPAforum/forum/migrations/0001_initial.py`).
- Cut the `0002_auto_load_settings.py` file (`SPAforum/forum/migrations/0002_auto_load_settings.py`).
- Make changes to the forum model.
- Execute the `makemigrations` command.
- Paste `0002_auto_load_settings.py` again.

Or

- Remove the `0001_initial.py` and `0002_auto_load_settings.py` files.
- Make changes to the forum model.
- Execute `the makemigrations` and `migrate` commands.
- Insert new SINGLE record of the ForumSettings model into the database manually.
<br />

__3. Create the tables in the database by__ `migrate` __command:__
```shell
python3 manage.py migrate
```
<br />

__4.  Create a user who can login to the admin site:__
```shell
python3 manage.py createsuperuser
```
<br />

__5. To handle password reset action you need to edit e-mail configuration in__ `settings.py` (`SPAforum/spaforum/settings.py`):
```python
EMAIL_HOST = 'smtp.example.com'
EMAIL_HOST_USER = 'example@example.com'
EMAIL_HOST_PASSWORD = 'password'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'example@example.com'
```
<br />

__6. Run the server:__
```shell
python3 manage.py runserver
```
<br />

__7. Go to__ `"/admin/"` __on your local domain – e.g.,__ `http://127.0.0.1:8000/admin/` __and sign in. Then you need to:__
- Edit Forum Settings, by passing new forum name and description (optionaly).
- Create Categories.
- Create SubForums.
<br />

__Now the SPAforum application is ready for use by users.__

<br />
<p align="center">
<img src="https://lh3.googleusercontent.com/2-a1O09mWj3dpA35YtzO_G8-Er_wy2-jJyyI4IFPVojxNroGoL5E6s3o60t3weYxcMbljNFuFunM0WGT69evZ5Wc2Lj1zxGLg_Y_P5DW8enkp4P9KBjqo_tbSZuNRY1MjGdmOT7Pv37bJq2hnxG5WeMkT7k-KHv6miR_3SExlyKobgLZ0N7ttv597DthzOhoozKH8kQIej7BlFc-Zw_GJjCwmGm1hJtxhtDQOSWoFyU-1AI-DUuegn0opObppK61cQD-l48KfVFq84RoVsbi_8Fg9waC3NwLOR-SuRW920RVVELX1MvmIv7KV-n4dgBgE3QI11Lc7PEis6U7jQEGCycEgf133vkey5cvNWFxSoWdYeE_gjY16T8bPwYKucosNKf6vJybRpoQA7l_DA7CzhbLRm8ulNpSkXnGPvfkNzEO1I4zB_W4HYSsz6VKVAaFPDg1POGM7t2dr0RJA7bEmdfHxDCHlrpSXd7sF_FXchNJhK2MkIO0dtw5FyZ4WzlR4KdtztDtey3YGEX9DfsNFf5QlN151nulDSm7UxED4Wtdo_AAiwadVEBd_gk8eulXUcCKJXPfeVikm8wtUxI1fp3EjzPMMqv6OzEsU5wzxdnhvnJ3_7LbHVc9eUHTUHnjCr3J0YCoxcxeCHBZPWWkS-YJza1pYB3KEidPbxFhZGf3lQ=w1191-h672-no" alt="SPAforum">
</p>

[Django]: <https://www.djangoproject.com/>
[Django REST framework]: <http://www.django-rest-framework.org/>
[AngularJS]: <https://angularjs.org/>
[Bootstrap 3]: <http://getbootstrap.com/>

[REST framework JWT Auth]: <http://getblimp.github.io/django-rest-framework-jwt/>
[django-modeladmin-reorder]: <https://django-modeladmin-reorder.readthedocs.io/>
[django-admin-sortable2]: <http://django-admin-sortable2.readthedocs.io/>

[dirPagination.js]: <https://github.com/michaelbromley/angularUtils/tree/master/src/directives/pagination>
[angular-elastic]: <https://github.com/monospaced/angular-elastic>
