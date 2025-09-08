from backend.extensions import db
from sqlalchemy.orm import mapped_column, Mapped
from datetime import date
from backend.enums import FavoriteColor

class UserProfile(db.Model):
    __tablename__ = 'user_profile'

    uid: Mapped[str] = mapped_column(db.String(128), primary_key=True)
    display_name: Mapped[str] = mapped_column(db.String(50))
    is_admin: Mapped[bool] = mapped_column(db.Boolean(), default=False)
    email: Mapped[str] = mapped_column(db.String(256), unique=True)
    birthday: Mapped[date|None] =mapped_column(db.Date())
    favorite_color: Mapped[FavoriteColor|None] = mapped_column(db.Enum(
        # 以下の設定は全て、SQLAlchemyのEnum型に特有の設定
        FavoriteColor,
        native_enum=False, # DB側でVARCHAR + CHECK制約でバリデーション
        constraint_name='ck_user_profile_favorite_color',
        validate_strings=True  # Python側でもバリデーションを有効にする特別な設定
    ))

    def __repr__(self):
        return f'<UserProfile uid:{self.uid} display_name:"{self.display_name}" is_admin:{self.is_admin} email:{self.email} birthday:{self.birthday} favorite_color:{self.favorite_color} >'
