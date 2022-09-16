from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):
    # 일반 user 생성
    def create_user(self, account_id, email, nickname, name, phone_number, password=None):
        if not account_id:
            raise ValueError('must have user ID')
        user = self.model(
            account_id=account_id,
            email=self.normalize_email(email),
            nickname=nickname,
            name=name,
            phone_number=phone_number
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    # 관리자 user 생성
    def create_superuser(self, account_id, email, nickname, name, phone_number, password=None):
        user = self.create_user(
            account_id=account_id,
            email=self.normalize_email(email),
            password=password,
            nickname=nickname,
            name=name,
            phone_number=phone_number
        )
        user.is_superuser = True
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    account_id = models.CharField(primary_key=True, max_length=15, null=False, blank=False, unique=True)
    email = models.EmailField(default='', max_length=100, null=False, blank=False, unique=True)
    nickname = models.CharField(default='', max_length=100, null=False, blank=False, unique=True)
    name = models.CharField(default='', max_length=100, null=False, blank=False)
    phone_number = models.CharField(max_length=15, null=False, blank=False, unique=True)

    # User 모델의 필수 field
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    # 헬퍼 클래스 사용
    objects = UserManager()

    # 사용자의 username field는 account_id으로 설정
    USERNAME_FIELD = 'account_id'
    # 필수로 작성해야하는 field
    REQUIRED_FIELDS = ['email', 'name', 'phone_number', 'nickname']

    def __str__(self):
        return self.account_id

    # True를 반환하여 권한이 있음을 알린다. Object를 반환하는 경우 해당 Object로 사용권한을 확인하는 절차가 필요
    def has_perm(self, perm, obj=None):
        return True

    # True를 반환하여 주어진 모델에 접근가능 하게 한다.
    def has_module_perms(self, app_label):
        return True

    # True가 반환되면 장고의 관리자 화면에 로그인 할 수 있다.
    # 만약 127.0.0.1/admin을 가리고싶다면 해당 부분을 주석처리한다.
    @property
    def is_staff(self):
        return self.is_admin