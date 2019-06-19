from django.db import models


from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Contragent(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название контрагента')
    status = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['id']


class Poll(models.Model):
    contr_id = models.ForeignKey('Contragent', on_delete=models.CASCADE)
    name_poll = models.CharField(max_length=255)
    comment = models.CharField(max_length=512, null=True, blank=True)
    active = models.BooleanField(default=False)
    count_poll = models.IntegerField(default=0, verbose_name='Количетво прохождений')
    work_poll = models.IntegerField(default=0, blank=True, verbose_name='Осталось')

    def __unicode__(self):
        return self.name_poll

    def save(self, force_insert=False, force_update=False):
        if (self.work_poll == 0 and self.active):
            self.work_poll = self.count_poll
        super(Poll, self).save(force_insert, force_update)


class Question(models.Model):
    poll_id = models.ForeignKey(Poll, on_delete=models.CASCADE)
    question_name = models.CharField(max_length=255, verbose_name='Вопрос')

    def __unicode__(self):
        return self.question_name


class Answer(models.Model):
    question_id = models.ForeignKey(Question, verbose_name='Вопрос', on_delete = models.CASCADE)
    answer_name = models.CharField(max_length=255, verbose_name='Ответ')

    def __unicode__(self):
        return self.answer_name

    class Meta:
        #order_with_respect_to = 'question_id'
        ordering = ['question_id', 'id']


class CheckHead(models.Model):
    device_id = models.CharField(max_length=36)
    uuid = models.CharField(max_length=36, unique=True)
    check_data = models.DateTimeField()
    check_number = models.CharField(max_length=12)

    def decor_data(self):
        return self.check_data.strftime('%d.%m.%Y %H:%M:%S')

    def __unicode__(self):
        return u'%s от %s' % (self.uuid, self.decor_data())

    decor_data.short_description = 'Дата чека'


class CheckPosition(models.Model):
    check_head = models.ForeignKey(CheckHead, on_delete=models.CASCADE,  related_name='check_pos')
    check_uuid = models.CharField('Чек', max_length=36)
    pos_uuid = models.CharField('Позиция', max_length=36)
    product_uuid = models.CharField(max_length=36)
    product_name = models.CharField('Наименование', max_length=255)
    quantity = models.FloatField('Количество')
    price = models.FloatField('Цена')


class QuestionResult(models.Model):
    device_id = models.CharField('Устройство', max_length=36)
    contr_id = models.IntegerField()
    poll_id = models.IntegerField('Опрос')
    question_id = models.IntegerField('Вопрос')
    answer_id = models.IntegerField('Ответ')
    answer_id_list = models.CharField('Ответы', max_length=1000)
    result_date = models.DateTimeField('Дата и время ответа')
    check_uuid = models.CharField('Чек', max_length=36)

    class Meta:
        index_together = [["device_id", "poll_id", "question_id", "answer_id", "answer_id_list"], ]


class UploadFile(models.Model):
    deviceId = models.CharField('ID Устройства', max_length=36, null=True)
    check_uuid = models.CharField('Номер чека', max_length=36, null=True, blank=True)
    file_obj = models.FileField(upload_to='media/', null=True, blank=True)


# для возможного дальнейшего написания нормальной красивой админки
#class ExtUser(models.Model):
#    user = models.OneToOneField(User)
#    is_login = models.BooleanField(default=False)

#    def __unicode__(self):
#        return self.user.username


User.profile = property(lambda u: ExtUser.objects.get_or_create(user=u)[0])





# Create your models here.
