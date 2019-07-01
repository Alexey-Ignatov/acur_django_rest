from django.contrib import admin

# Register your models here.
#-*- coding: utf-8 -*-
from django.contrib import admin
from acur_research.models import Contragent,Poll,Question,Answer,UploadFile,QuestionResult, CheckHead, CheckPhoneNumber, PollResult
from acur_research.models import CheckPosition

# Register your models here.
class ContragentAdmin(admin.ModelAdmin):
    list_display=('name','status')
    list_filter=['name']
    search_fields=['name']

class PollAdmin(admin.ModelAdmin):
    list_display=('contr_id','name_poll','comment','count_poll','work_poll','active')
    search_fields=['name_poll']
    fields = ('contr_id','name_poll','comment','count_poll','active')

class AnswerInline(admin.TabularInline):
    model = Answer

class QuestionAdmin(admin.ModelAdmin):
    list_display=('id','poll_id','question_name')
    ordering = ('id',)
    inlines = [AnswerInline,]

class AnswerAdmin(admin.ModelAdmin):
    list_display=('question_id','id','answer_name')
    ordering = ('question_id','id',)

class UploadFileAdmin(admin.ModelAdmin):
     list_display=('file_obj','check_uuid','deviceId')

#@admin.register(CheckPosition)
#class CheckPositionAdmin(admin.ModelAdmin):
#     list_display = ('check_head','pos_uuid','product_name','quantity','price')
#     ordering = ('check_head',)

class QuestionResultAdmin(admin.ModelAdmin):
     date_hierarchy = 'result_date'
     list_display = ('device_id','result_date','check_uuid','poll_id','question_id','answer_id_list')
     list_display_links = None



class CheckAdmin(admin.ModelAdmin):
    list_display = ('device_id', 'uuid', 'check_date', 'check_number',  'get_tel_str')

    def get_tel_str(self, obj):
        if obj.tel_no:
            return obj.tel_no.tel_str
        else:
            return '-'

class CheckPosAdmin(admin.ModelAdmin):
    list_display =('pos_uuid', 'product_uuid', 'product_name', 'quantity', 'price', 'get_check_uuid')
    def get_check_uuid(self, obj):
        return obj.check_head.uuid



class PhoneAdmin(admin.ModelAdmin):
    list_display = ('tel_str',)


class PollResultAdmin(admin.ModelAdmin):
    list_display = ('id' ,'survey_id', 'revision_id', 'start_date', 'finish_date', 'status', 'check_uuid')

    def check_uuid(self, obj):
        return obj.check_head.uuid


admin.site.register(Contragent,ContragentAdmin)
admin.site.register(Poll,PollAdmin)
admin.site.register(Question,QuestionAdmin)
admin.site.register(Answer,AnswerAdmin)
admin.site.register(UploadFile,UploadFileAdmin)
admin.site.register(QuestionResult,QuestionResultAdmin)
admin.site.register(CheckHead, CheckAdmin)
admin.site.register(CheckPosition, CheckPosAdmin)
admin.site.register(CheckPhoneNumber,PhoneAdmin)
admin.site.register(PollResult,PollResultAdmin)

