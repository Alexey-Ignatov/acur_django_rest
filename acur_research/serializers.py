from rest_framework import serializers
from acur_research.models import CheckPosition, CheckHead


#from snippets.models import S

class CheckPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckPosition
        fields = ('check_head', 'check_uuid', 'pos_uuid', 'product_uuid', 'product_name', 'quantity', 'price')


class CheckHeadSerializer(serializers.ModelSerializer):
    check_pos = serializers.StringRelatedField(many=True)
    class Meta:
        model = CheckHead
        fields = ('device_id', 'uuid', 'check_data', 'check_number', 'check_pos')

#CheckHead(1, 'uuid', '2019-01-01 01:01', 'check_number')



#inDate = "29-Apr-2013-15:59:02"
#d= datetime.strptime(inDate, "%d-%b-%Y-%H:%M:%S")




