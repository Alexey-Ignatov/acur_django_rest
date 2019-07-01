from rest_framework import serializers
from acur_research.models import CheckPosition, CheckHead, CheckPhoneNumber,PollResult, EvoUser


from django.http import Http404
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
import acur_research.utils as utils
#from snippets.models import S

class CheckPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckPosition
        fields = ('pos_uuid', 'product_uuid', 'product_name', 'quantity', 'price')




class CheckHeadSerializer(serializers.ModelSerializer):
    check_pos = CheckPositionSerializer(many=True)
    class Meta:
        model = CheckHead
        fields = ('device_id', 'uuid', 'check_date', 'check_number',    'check_pos')


    def create(self, validated_data):

        print(validated_data)
        check_pos = validated_data.pop('check_pos')
        validated_data_upd = validated_data
        #validated_data['device_id'] =


        new_check = CheckHead.objects.create(**validated_data_upd)
        for param_d in check_pos:
            param_d['check_head'] = new_check
            CheckPosition.objects.create(**param_d)


        return  new_check



class CheckPhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckPhoneNumber
        fields = ('tel_str',)


class PollResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = PollResult
        fields = ('id' ,'survey_id', 'revision_id', 'start_date', 'finish_date', 'status')

    def create(self, validated_data):
        validated_data_upd = validated_data

        surv_id = validated_data_upd['survey_id']
        answ_id = validated_data_upd['id']
        check_uuid = utils.get_checkuuid_by_answ_id(surv_id, answ_id)

        try:
            curr_check = CheckHead.objects.get(uuid=check_uuid)
        except CheckHead.DoesNotExist:
            raise Http404

        validated_data_upd['check_head'] = curr_check
        return PollResult.objects.create(**validated_data_upd)



class EvoUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = EvoUser
        fields = ('userId', 'token')




