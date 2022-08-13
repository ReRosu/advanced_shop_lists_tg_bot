from source.db.base import metadata, engine
import sqlalchemy as sa

users = sa.Table(
    'users',
    metadata,
    sa.Column('id', sa.BIGINT, primary_key=True),
    sa.Column('user_name', sa.TEXT)
)

shop_lists = sa.Table(
    'shop_lists',
    metadata,
    sa.Column('shop_list', sa.JSON, nullable=False),
    sa.Column('creator_user_id', sa.BIGINT, sa.ForeignKey(users.columns.id, ondelete='CASCADE'), nullable=False),
    sa.Column('is_over', sa.BOOLEAN, nullable=False),
    sa.Column('id', sa.BIGINT, primary_key=True),
    sa.Column('name', sa.TEXT, nullable=False)
)

friends = sa.Table(
    'friends',
    metadata,
    sa.Column('user_id', sa.BIGINT, sa.ForeignKey(users.columns.id, ondelete='CASCADE'), nullable=False),
    sa.Column('friend_id', sa.BIGINT, sa.ForeignKey(users.columns.id, ondelete='CASCADE'), nullable=False)
)

shop_lists_to_users = sa.Table(
    'shop_lists_to_users',
    metadata,
    sa.Column('shop_list_id', sa.BIGINT, sa.ForeignKey(shop_lists.columns.id, ondelete='CASCADE'), nullable=False),
    sa.Column('user_id', sa.BIGINT, sa.ForeignKey(users.columns.id, ondelete='CASCADE'), nullable=False)
)

bug_reports = sa.Table(
    'bug_reports',
    metadata,
    sa.Column('id', sa.BIGINT, nullable=False),
    sa.Column('message', sa.TEXT, nullable=False),
    sa.Column('user_id', sa.BIGINT, sa.ForeignKey(users.columns.id, ondelete='CASCADE'), nullable=False),
    sa.Column('is_done', sa.BOOLEAN, nullable=False)
)

wishes = sa.Table(
    'wishes',
    metadata,
    sa.Column('id', sa.BIGINT, nullable=False),
    sa.Column('message', sa.TEXT, nullable=False),
    sa.Column('user_id', sa.BIGINT, sa.ForeignKey(users.columns.id, ondelete='CASCADE'), nullable=False),
    sa.Column('is_done', sa.BOOLEAN, nullable=False)
)


def create_tables():
    metadata.create_all(engine, checkfirst=True)


def drop_tables():
    friends.drop(engine, checkfirst=False)
    shop_lists_to_users.drop(engine, checkfirst=False)
    shop_lists.drop(engine, checkfirst=False)
    users.drop(engine, checkfirst=False)
    #metadata.drop_all(engine, checkfirst=True)


def recreate_tables():
    drop_tables()
    create_tables()
