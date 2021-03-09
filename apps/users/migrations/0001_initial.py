# Generated by Django 2.1 on 2021-01-20 08:05

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
        ('system', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('en_name', models.CharField(default='', max_length=20, verbose_name='英文姓名')),
                ('cn_name', models.CharField(blank=True, default='', max_length=20, verbose_name='中文姓名')),
                ('gender', models.CharField(blank=True, choices=[('male', '男'), ('female', '女')], max_length=16, null=True, verbose_name='性别')),
                ('birthday', models.DateField(blank=True, null=True, verbose_name='出生日期')),
                ('is_hk', models.BooleanField(choices=[(True, '是'), (False, '否')], default=False, verbose_name='是否港职')),
                ('work_card', models.CharField(blank=True, max_length=6, null=True, verbose_name='工号')),
                ('ext_num', models.CharField(max_length=4, verbose_name='座机')),
                ('mobile', models.CharField(blank=True, default='', max_length=11, null=True, verbose_name='电话')),
                ('email_password', models.CharField(blank=True, max_length=16, null=True, verbose_name='邮箱密码')),
            ],
            options={
                'verbose_name': '用户信息',
                'verbose_name_plural': '用户信息',
                'ordering': ['id'],
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_number', models.FloatField(blank=True, null=True, verbose_name='编号')),
                ('title', models.CharField(blank=True, max_length=32, null=True, verbose_name='名称')),
                ('simple_title', models.CharField(max_length=32, unique=True, verbose_name='简写')),
                ('asset_owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='asset_owner', to=settings.AUTH_USER_MODEL, verbose_name='资产责任人')),
                ('clerk', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='clerk', to=settings.AUTH_USER_MODEL, verbose_name='文员')),
                ('leader', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='leader', to=settings.AUTH_USER_MODEL, verbose_name='主管')),
            ],
            options={
                'verbose_name': '部门信息',
                'verbose_name_plural': '部门信息',
                'ordering': ['sort_number'],
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_number', models.FloatField(blank=True, null=True, verbose_name='编号')),
                ('area', models.CharField(max_length=32, unique=True, verbose_name='区域')),
            ],
            options={
                'verbose_name': '位置信息',
                'verbose_name_plural': '位置信息',
                'ordering': ['sort_number'],
            },
        ),
        migrations.CreateModel(
            name='Permit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_number', models.FloatField(blank=True, null=True, verbose_name='编号')),
                ('title', models.CharField(max_length=32, unique=True, verbose_name='名称')),
                ('mean', models.TextField(blank=True, default='', null=True, verbose_name='备注')),
            ],
            options={
                'verbose_name': '授权列表',
                'verbose_name_plural': '授权列表',
                'ordering': ['sort_number'],
            },
        ),
        migrations.CreateModel(
            name='PermitLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('record_type', models.CharField(choices=[('update', '修改'), ('upload', '上传')], max_length=16, verbose_name='记录类型')),
                ('record_time', models.DateTimeField(auto_now_add=True, verbose_name='记录时间')),
                ('remark', models.TextField(default='', verbose_name='备注')),
                ('record_obj', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='permit_proposer', to=settings.AUTH_USER_MODEL, verbose_name='申请人')),
                ('recorder', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='permit_recorder', to=settings.AUTH_USER_MODEL, verbose_name='记录人')),
            ],
            options={
                'verbose_name': '授权记录',
                'verbose_name_plural': '授权记录',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_number', models.FloatField(blank=True, null=True, verbose_name='编号')),
                ('title', models.CharField(max_length=32, unique=True, verbose_name='名称')),
            ],
            options={
                'verbose_name': '职位信息',
                'verbose_name_plural': '职位信息',
                'ordering': ['sort_number'],
            },
        ),
        migrations.AddField(
            model_name='userprofile',
            name='department',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.Department', verbose_name='部门'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='location',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.Location', verbose_name='位置'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='permits',
            field=models.ManyToManyField(blank=True, to='users.Permit', verbose_name='权限'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='position',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.Position', verbose_name='职位'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='roles',
            field=models.ManyToManyField(blank=True, to='system.Role', verbose_name='角色'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
    ]
