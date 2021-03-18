from rest_framework import serializers
from apps.worktable.models import WorkOrder, WorkOrderLog


class WorkOrderListSerializer(serializers.ModelSerializer):
    created_log = serializers.SerializerMethodField('get_created_log')
    process_log = serializers.SerializerMethodField('get_process_log')
    content = serializers.SerializerMethodField('get_len_content')
    state = serializers.ReadOnlyField(source='get_state_display')
    type = serializers.ReadOnlyField(source='get_type_display')

    class Meta:
        model = WorkOrder
        fields = ('id', 'num', 'content', 'created_log', 'process_log', 'state', 'type')

    def get_len_content(self, obj):
        content = obj.content
        if len(str(content)) > 16:
            return '{}...'.format(str(content)[0:16])
        else:
            return str(content)

    def get_created_log(self, obj):
        log = WorkOrderLog.objects.get(record_obj=obj, record_type='create')
        serializer = WorkOrderLogForListSerializer(log)
        return serializer.data

    def get_process_log(self, obj):
        try:
            log = WorkOrderLog.objects.get(record_obj=obj, record_type='process')
            serializer = WorkOrderLogForListSerializer(log)
            return serializer.data
        except Exception as e:
            return None


class WorkOrderLogForListSerializer(serializers.ModelSerializer):
    recorder = serializers.ReadOnlyField(source='recorder.__str__')

    class Meta:
        model = WorkOrderLog
        fields = ('record_time', 'recorder')


class WorkOrderLogSerializer(serializers.ModelSerializer):
    # record_obj = WorkOrderSerializer(read_only=True)
    record_obj = serializers.ReadOnlyField(source='record_obj.num')
    recorder = serializers.ReadOnlyField(source='recorder.__str__')
    full_record_type = serializers.ReadOnlyField(source='get_record_type_display')
    # cn_record_type = serializers.SerializerMethodField()    # 用于显示模型中不存在的字段，不可反序列化

    class Meta:
        model = WorkOrderLog
        fields = '__all__'
        read_only_fields = ('id', 'record_obj', 'recorder', 'record_time')
        # depth = 1    # 设置关联模型的深度，会展示所有字段


class WorkOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkOrder
        fields = '__all__'
        read_only_fields = ('id', 'num', 'proposer')
