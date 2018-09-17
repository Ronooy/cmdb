from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager,AbstractUser

def reset_user_image(instance, filename):
    end = filename.rsplit('.', 1)[1]
    return 'image/userImage/{}.{}'.format(instance.username, end)

class PermissionList(models.Model):
    """
        权限表
    """
    name = models.CharField('权限名称',max_length=64)
    url = models.CharField('URL',max_length=255)

    def __str__(self):
        return '%s(%s)' % (self.name, self.url)

    class Meta:
        verbose_name='权限管理'
        verbose_name_plural='权限管理'
        unique_together=('name','url')


class RoleList(models.Model):
    """
        角色表
    """
    name = models.CharField('角色名称',max_length=64,unique=True)
    permissions = models.ManyToManyField(PermissionList,verbose_name='权限', blank=True)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name='角色管理'
        verbose_name_plural='角色管理'


class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(email,
                                username=username,
                                password=password,
                                )

        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class UserInfo(AbstractBaseUser):
    """
        用户表
    """
    username = models.CharField('用户名',max_length=40, unique=True, db_index=True,
                                error_messages={'unique':'该用户名已经存在'})
    image=models.ImageField('图像',upload_to=reset_user_image,default='img/default_user.jpg')
    email = models.EmailField('邮箱',max_length=255,unique=True,
                              error_messages={'unique': '该邮箱已经存在'})
    is_active = models.BooleanField('状态',default=False)
    is_superuser = models.BooleanField('管理员',default=False)
    nickname = models.CharField('昵称',max_length=64, blank=True,null=True)
    role=models.ForeignKey('RoleList',verbose_name='角色',blank=True,null=True,on_delete=models.SET_NULL)
    objects = UserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def has_perm(self, perm, obj=None):
        if self.is_active and self.is_superuser:
            return True

    def has_module_perms(self, app_label):
        return True

    def get_all_permissions(self):
        return True

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_superuser

    class Meta:
        verbose_name='用户管理'
        verbose_name_plural='用户管理'
