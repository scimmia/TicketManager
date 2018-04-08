from django.db import models

# Create your models here.

class Card(models.Model):
    name = models.CharField(u'银行卡', max_length=50)
    money = models.FloatField(u'金额', default=0)
    beizhu = models.CharField(u'备注', max_length=100)
    pub_date = models.DateField(u'添加日期', auto_now_add=True)

    def __str__(self):
        return self.name


class Ticket(models.Model):
    goumairiqi = models.DateField(u'购买日期', auto_now_add=True)
    qianpaipiaohao = models.CharField(u'前排票号', max_length=100)
    piaohao = models.CharField(u'票号', max_length=100)
    chupiaohang = models.CharField(u'出票行', max_length=100)
    chupiaoriqi = models.DateField(u'出票日期', )
    daoqiriqi = models.DateField(u'到期日期', )
    piaomianjiage = models.FloatField(u'票面价格', default=0)
    gouruhuilv = models.FloatField(u'购入利率', default=0)
    gourujiage = models.FloatField(u'购入价格', default=0)
    # gourucard = models.ForeignKey( Card, related_name='buy_card', verbose_name=u'购入卡' ,  blank=True,null=True)
    gongyingshang = models.CharField(u'供应商', max_length=100)
    maichuriqi = models.DateField(u'卖出日期', blank=True,null=True)
    maichulilv = models.FloatField(u'卖出利率', default=0)
    maichujiage = models.FloatField(u'卖出价格', default=0)
    # maichucard = models.ForeignKey( Card, related_name='sold_card',  verbose_name=u'卖出卡' ,  blank=True,null=True)
    maipiaoren = models.CharField(u'买票人', max_length=100, blank=True,null=True)
    lirun = models.IntegerField(u'利润', default=0)
    TICKET_STATUS= (
        (1,u'已购入'),
        # (2,u'已付款'),
        (3,u'已卖出'),
        # (4,u'已收款'),
        (5,u'入池'),
    )
    t_status = models.IntegerField(
        u'状态',
        choices=TICKET_STATUS,
        default=1,
    )


class Fee(models.Model):
    ticket = models.ForeignKey( Ticket,  verbose_name=u'票据' ,  blank=False,null=False)
    name = models.CharField(u'费用内容', max_length=50)
    money = models.FloatField(u'金额', default=0)
    pub_date = models.DateField(u'添加日期', auto_now_add=True)

    def __str__(self):
        return self.name

class Transfer(models.Model):
    yinhangka = models.ForeignKey( Card, related_name='transfer_card', verbose_name=u'银行卡' ,  blank=False,null=False)
    money = models.FloatField(u'金额', default=0)
    beizhu = models.CharField(u'备注', max_length=100)
    pub_date = models.DateField(u'添加日期', auto_now_add=True)

    def __str__(self):
        return self.beizhu

