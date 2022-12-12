from flask_admin import Admin, BaseView, expose, AdminIndexView
from flask import request
from flask_admin.contrib.sqla import ModelView
from app.models import Category, UserRole, Tag, Flight, TuyenBay, SanBay, SanBayDung, VeChuyenBay, HangVe
from app import app, db, dao
from flask_login import logout_user, current_user
from flask import redirect
from wtforms import TextAreaField
from wtforms.widgets import TextArea


class AuthenticatedModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


class AuthenticatedView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated


class CKTextAreaWidget(TextArea):
    def __call__(self, field, **kwargs):
        if kwargs.get('class'):
            kwargs['class'] += ' ckeditor'
        else:
            kwargs.setdefault('class', 'ckeditor')
        return super(CKTextAreaWidget, self).__call__(field, **kwargs)


class CKTextAreaField(TextAreaField):
    widget = CKTextAreaWidget()


class ProductModelView(AuthenticatedModelView):
    column_filters = ['name', 'price']
    column_searchable_list = ['name']
    column_exclude_list = ['name']
    can_view_details = True
    can_export = True
    column_labels = {
        'name': 'Hãng Máy Bay',
        'price': 'Giá',
    }
    extra_js = ['//cdn.ckeditor.com/4.6.0/standard/ckeditor.js']
    # form_overrides = {
    #     'description': CKTextAreaField
    # }
    page_size = 6


class StatsView(AuthenticatedView):
    @expose('/')
    def index(self):
        stats = dao.stats_revenue(kw=request.args.get('kw'),
                                  from_date=request.args.get('from_date'),
                                  to_date=request.args.get('to_date'))
        return self.render('admin/stats.html', stats=stats)


class LogoutView(AuthenticatedView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')


class MyAdminView(AdminIndexView):
    @expose('/')
    def index(self):
        stats = dao.stats_revenue
        return self.render('admin/index.html', stats=stats)


class TuyenBayModelView(AuthenticatedModelView):
    column_filters = ['ten', 'sanbaydi', 'sanbayden']
    column_searchable_list = ['ten']
    can_export = True
    column_labels = {
        'ten': 'Tên tuyến bay',
        'sanbaydi': 'Sân bay đi',
        'sanbayden': 'Sân bay đến',
    }
    page_size = 6


class SanBayModelView(AuthenticatedModelView):
    column_filters = ['ten']
    column_searchable_list = ['ten']
    can_export = True
    column_labels = {
        'ten': 'Tên sân bay',
    }
    page_size = 6


class SanBayDungModelView(AuthenticatedModelView):
    column_filters = ['chuyenbay_ma']
    can_export = True
    column_labels = {
        'thoigiandung': 'Thời gian dừng',
        'sanbay': 'Sân bay',
        'chuyenbay': 'Chuyến bay',
    }
    page_size = 6


class VeChuyenBayModelView(AuthenticatedModelView):
    can_export = True
    can_view_details = True
    column_labels = {
        'tennguoidi': 'Tên người đi',
        'cccd': 'Căn cước công dân',
        'Ngaydat': 'Ngày đặt vé',
        'nguoidung': 'Người dùng',
        'bangdongia': 'Chi tiết chuyến đi',
    }
    page_size = 6


class HangVeModelView(AuthenticatedModelView):
    can_export = True
    column_labels = {
        'ten': 'Tên hạng vé'
    }
    page_size = 6


admin = Admin(app=app, name='Quản trị Chuyến Bay',
              template_mode='bootstrap4')
# admin.add_view(AuthenticatedModelView(Category, db.session, name='Danh mục'))
admin.add_view(TuyenBayModelView(TuyenBay,  db.session, name='Tuyến bay'))
admin.add_view(ProductModelView(Flight, db.session, name='Chuyến bay'))
admin.add_view(SanBayModelView(SanBay, db.session, name='Sân bay'))
admin.add_view(SanBayDungModelView(SanBayDung, db.session, name='Sân bay TG'))
# admin.add_view(ProductModelView(Ve, db.session, name='Vé'))
admin.add_view(VeChuyenBayModelView(VeChuyenBay, db.session, name='Vé'))
admin.add_view(HangVeModelView(HangVe, db.session, name='Hạng vé'))
# admin.add_view(AuthenticatedModelView(Tag, db.session, name='Tag'))
admin.add_view(StatsView(name='Thống kê - báo cáo'))
# admin.add_view(AuthenticatedModelView(Tag, db.session, name='Thay đổi sân bay'))
admin.add_view(LogoutView(name='Đăng xuất'))
