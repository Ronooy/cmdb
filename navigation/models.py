from django.db import models


class NavStore(models.Model):
    name=models.CharField('名称',max_length=64)
    url=models.URLField('网址')
    remark=models.CharField('备注',max_length=200,blank=True,null=True)
    c_date=models.DateTimeField('创建时间',auto_now_add=True)

    def __str__(self):
        return '%s<%s>'%(self.name,self.url)

    class Meta:
        verbose_name='站点导航'
        verbose_name_plural='站点导航'
        unique_together=('name','url')