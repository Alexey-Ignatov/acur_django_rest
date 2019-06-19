from rest_framework import serializers
from acur_research.models import CheckPosition, CheckHead


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

        new_check = CheckHead.objects.create(**validated_data)
        for param_d in check_pos:
            param_d['check_head'] = new_check
            CheckPosition.objects.create(**param_d)


        return  new_check


