from django.contrib import admin

# Register your models here.
from django.forms import ModelForm
from suit.widgets import SuitDateWidget
from ticket.models import Ticket,Card,Fee,Transfer


# Register your models here.

class FeeInline(admin.TabularInline):
    model = Fee
    extra = 1

class TranserInline(admin.TabularInline):
    model = Transfer
    extra = 1
    fields = ('money', 'beizhu', 'pub_date')
    readonly_fields = ('pub_date',)
    # def has_change_permission(self, request, obj=None):
    #     return request.user.is_superuser

    # def get_readonly_fields(self, request, obj=None):
    #     fields = []
    #     if request.user.is_superuser:
    #         self.readonly_fields = []
    #     else:
    #         fields = ('money', 'beizhu', 'pub_date')
    #     return fields

# class TicketForm(ModelForm):
#     class Meta:
#         model = Ticket
#         widgets = {
#             'chupiaoriqi': SuitDateWidget,
#             'daoqiriqi': SuitDateWidget,
#             'maichuriqi': SuitDateWidget,
#         }
class TicketAdmin(admin.ModelAdmin):
    # form = TicketForm
    fieldsets = (
        ("状态", {'fields':['t_status']}),
        ("买入信息", {'fields': (('qianpaipiaohao', 'piaohao'), 'chupiaohang','chupiaoriqi','daoqiriqi','piaomianjiage',('gouruhuilv', 'gourujiage',),'gongyingshang',)}),
        ("卖出信息", {'fields':( 'maichuriqi',('maichulilv', 'maichujiage',),'maipiaoren')}),
        ("利润", {'fields':['lirun']}),
    )
    inlines = [FeeInline]
    list_display = ('goumairiqi','qianpaipiaohao','piaohao', 'gourujiage',  'maichuriqi', 'maichujiage','lirun','t_status')
    list_filter =('goumairiqi', 'qianpaipiaohao','piaohao', 't_status') #过滤器
    search_fields = ('qianpaipiaohao','piaohao',)
    date_hierarchy = 'goumairiqi'    # 详细时间分层筛选　
    # list_editable = ['t_status',]
    fk_fields = ('maichucard')
    readonly_fields = ('lirun',)

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super(TicketAdmin, self).get_search_results(request, queryset, search_term)
        try:
            search_term_as_int = int(search_term)
            queryset |= self.model.objects.filter(age=search_term_as_int)
        except:
            pass
        return queryset, use_distinct

    def save_model(self, request, obj, form, change):
        # if change:  # 更改的时候
        #     obj_original = self.model.objects.get(pk=obj.pk)
        # else:  # 新增的时候
        #     obj_original = None

        obj.lirun = obj.maichujiage - obj.gourujiage
        obj.save()

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in formset.deleted_objects:
            if isinstance(instance, Fee):  # Check if it is the correct type of inline
                instance.delete()
                instance.ticket.lirun = instance.ticket.lirun + instance.money
                instance.ticket.save()
        for instance in instances:
            if isinstance(instance, Fee):  # Check if it is the correct type of inline
                if change:  # 更改的时候
                    try:
                        obj_original = Transfer.objects.get(pk=instance.pk)
                        instance.ticket.lirun = instance.ticket.lirun + obj_original.money
                    except:
                        pass
                instance.ticket.lirun = instance.ticket.lirun - instance.money
                instance.ticket.save()
                instance.save()
# class TicketAdmin(admin.ModelAdmin):
#     # form = TicketForm
#     fieldsets = (
#         ("状态", {'fields':['t_status']}),
#         ("买入信息", {'fields': (('qianpaipiaohao', 'piaohao'), 'chupiaohang',('chupiaoriqi', 'daoqiriqi'),'piaomianjiage',('gouruhuilv', 'gourujiage','gourucard'),'gongyingshang',)}),
#         ("卖出信息", {'fields':( 'maichuriqi',('maichulilv', 'maichujiage','maichucard'),'maipiaoren')}),
#         ("利润", {'fields':['lirun']}),
#     )
#     inlines = [FeeInline]
#     list_display = ('goumairiqi','qianpaipiaohao','piaohao','maichucard', 't_status')
#     list_filter =('goumairiqi', 'qianpaipiaohao','piaohao','maichucard', 't_status') #过滤器
#     search_fields = ('qianpaipiaohao','piaohao',)
#     date_hierarchy = 'goumairiqi'    # 详细时间分层筛选　
#     list_editable = ['t_status', 'maichucard']
#     fk_fields = ('maichucard')
#     readonly_fields = ('lirun',)
#
#     def get_search_results(self, request, queryset, search_term):
#         queryset, use_distinct = super(TicketAdmin, self).get_search_results(request, queryset, search_term)
#         try:
#             search_term_as_int = int(search_term)
#             queryset |= self.model.objects.filter(age=search_term_as_int)
#         except:
#             pass
#         return queryset, use_distinct
#
#     def save_model(self, request, obj, form, change):
#         # if change:  # 更改的时候
#         #     obj_original = self.model.objects.get(pk=obj.pk)
#         # else:  # 新增的时候
#         #     obj_original = None
#
#         obj.lirun = obj.maichujiage - obj.gourujiage
#         # obj.lirun = float(request.POST.get('maichujiage'))- float(request.POST.get('gourujiage'))
#         # obj.lirun = request.POST.get('maichujiage')
#         obj.save()

class TransferAdmin(admin.ModelAdmin):
    list_display = ('yinhangka','money','beizhu','pub_date')

    def save_model(self, request, obj, form, change):
        if change:  # 更改的时候
            obj_original = self.model.objects.get(pk=obj.pk)
            obj.yinhangka.money = obj.yinhangka.money +obj.money-obj_original.money
            obj.yinhangka.save()
        else:  # 新增的时候
            obj.yinhangka.money = obj.yinhangka.money +obj.money
            obj.yinhangka.save()
        obj.save()

        # obj.lirun = float(request.POST.get('maichujiage'))- float(request.POST.get('gourujiage'))
        # obj.lirun = request.POST.get('maichujiage')
    def delete_model(self, request, obj):
        obj.yinhangka.money = obj.yinhangka.money - obj.money
        obj.yinhangka.save()
        obj.delete()

    def get_readonly_fields(self, request, obj=None):
        """  重新定义此函数，限制普通用户所能修改的字段  """
        if request.user.is_superuser:
            self.readonly_fields = []
        elif hasattr(obj, 'pub_date'):
            if obj.pub_date:
                self.readonly_fields = ('yinhangka','money','beizhu')
        else:
            self.readonly_fields = []

        return self.readonly_fields

    readonly_fields = ('yinhangka','money','beizhu')



class CardAdmin(admin.ModelAdmin):
    # fields = ('name', 'money')
    list_display = ('name', 'money','pub_date')
    inlines = [TranserInline]
    def get_readonly_fields(self, request, obj=None):
        """  重新定义此函数，限制普通用户所能修改的字段  """
        if request.user.is_superuser:
            self.readonly_fields = []
        return self.readonly_fields

    readonly_fields = ('money','pub_date')

    def save_model(self, request, obj, form, change):
        # if change:  # 更改的时候
        #     obj_original = self.model.objects.get(pk=obj.pk)
        # else:  # 新增的时候
        #     obj_original = None

        obj.save()

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in formset.deleted_objects:
            if isinstance(instance, Transfer):  # Check if it is the correct type of inline
                instance.delete()
                instance.yinhangka.money = instance.yinhangka.money - instance.money
                instance.yinhangka.save()
        for instance in instances:
            if isinstance(instance, Transfer):  # Check if it is the correct type of inline
                if change:  # 更改的时候
                    try:
                        obj_original = Transfer.objects.get(pk=instance.pk)
                        instance.yinhangka.money = instance.yinhangka.money - obj_original.money
                    except:
                        pass
                instance.yinhangka.money = instance.yinhangka.money + instance.money
                instance.yinhangka.save()
                instance.save()

admin.site.register(Ticket, TicketAdmin)
admin.site.register(Card, CardAdmin)
admin.site.register(Transfer, TransferAdmin)